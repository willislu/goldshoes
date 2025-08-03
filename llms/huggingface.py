from transformers import GPT2Tokenizer, GPT2Config, GPT2LMHeadModel, Trainer, TrainingArguments
from datasets import load_dataset
import torch
import os

model_dir = "./tiny_gpt2"

# 1. Load tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token

# 2. Check if model already exists
if not os.path.exists(model_dir):
    print("No trained model found. Training from scratch...")

    # Load a small dataset
    dataset = load_dataset("wikitext", "wikitext-2-raw-v1", split="train[:1%]")

    # Tokenize
    def tokenize_function(example):
        return tokenizer(example['text'], return_special_tokens_mask=True)

    tokenized_dataset = dataset.map(
        tokenize_function,
        batched=True,
        remove_columns=["text"]
    )

    # Group texts into blocks
    block_size = 128
    def group_texts(examples):
        concatenated = {k: sum(examples[k], []) for k in examples.keys()}
        total_length = (len(concatenated["input_ids"]) // block_size) * block_size
        result = {
            k: [concatenated[k][i:i + block_size] for i in range(0, total_length, block_size)]
            for k in concatenated.keys()
        }
        result["labels"] = result["input_ids"].copy()
        return result

    lm_dataset = tokenized_dataset.map(group_texts, batched=True)

    # Define tiny model
    config = GPT2Config(
        vocab_size=tokenizer.vocab_size,
        n_positions=block_size,
        n_embd=128,
        n_layer=2,
        n_head=2
    )
    model = GPT2LMHeadModel(config)

    # Training setup
    training_args = TrainingArguments(
        output_dir=model_dir,
        overwrite_output_dir=True,
        num_train_epochs=1,
        per_device_train_batch_size=4,
        save_steps=500,
        save_total_limit=2,
        logging_steps=10,
        remove_unused_columns=False,
        fp16=torch.cuda.is_available()
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=lm_dataset,
        tokenizer=tokenizer
    )

    # Train the model
    trainer.train()

    # Save it
    model.save_pretrained(model_dir)
    tokenizer.save_pretrained(model_dir)

else:
    print("Model already trained. Skipping training.")

# 3. Load model and tokenizer
model = GPT2LMHeadModel.from_pretrained(model_dir)
tokenizer = GPT2Tokenizer.from_pretrained(model_dir)
model.eval()

# Move to device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# 4. Generate text
prompt = "The meaning of life is"
inputs = tokenizer(prompt, return_tensors="pt").to(device)

output = model.generate(
    **inputs,
    max_length=50,
    num_return_sequences=1,
    do_sample=True,
    top_k=50,
    top_p=0.95,
    temperature=0.8
)

print(tokenizer.decode(output[0], skip_special_tokens=True))
