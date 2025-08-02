import random
import sys
import time

class RouletteWheel:
    def __init__(self):
        self.numbers = [str(i) for i in range(1, 37)] + ['0', '00']
        self.colors = self.assign_colors()

    def assign_colors(self):
        red_numbers = {
            '1', '3', '5', '7', '9', '12', '14', '16', '18',
            '19', '21', '23', '25', '27', '30', '32', '34', '36'
        }
        colors = {}
        for num in self.numbers:
            if num in red_numbers:
                colors[num] = 'red'
            elif num in ['0', '00']:
                colors[num] = 'green'
            else:
                colors[num] = 'black'
        return colors

    def spin(self):
        print("\nSpinning the wheel...\n")
        spin_sequence = random.choices(self.numbers, k=15)  # fewer spins

        for i, number in enumerate(spin_sequence):
            sys.stdout.write(f"\rBall lands on... {number:<3}")
            sys.stdout.flush()
            time.sleep(0.03 + i * 0.01)  # shorter and faster

        final_result = spin_sequence[-1]
        final_color = self.colors[final_result]

        print(f"\n\n🎯 The ball landed on {final_result} ({final_color})\n")
        return final_result, final_color


class Player:
    def __init__(self, name, balance=500):
        self.name = name
        self.balance = balance

    def can_bet(self, amount):
        return amount <= self.balance

    def update_balance(self, amount):
        self.balance += amount

    def __str__(self):
        return f"{self.name}: Balance = ${self.balance}"


class Bet:
    def __init__(self, bet_type, value, amount):
        self.bet_type = bet_type  # 'number', 'color', or 'parity'
        self.value = value        # e.g. '17', 'red', 'even'
        self.amount = amount

    def evaluate(self, result, color):
        """Returns the payout multiplier (0 means lose)."""
        if self.bet_type == 'number':
            if result == self.value:
                return 35  # 35 to 1 payout
        elif self.bet_type == 'color':
            if color == self.value:
                return 1
        elif self.bet_type == 'parity':
            if result in ['0', '00']:
                return 0
            if self.value == 'even' and int(result) % 2 == 0:
                return 1
            if self.value == 'odd' and int(result) % 2 == 1:
                return 1
        return 0


def play_roulette():
    wheel = RouletteWheel()
    player = Player("You")

    print(f"\n🧨 Welcome to Double Zero Roulette! {player}\n")

    while player.balance > 0:
        print(f"\n🎲 {player}")
        print("Bet types:")
        print("1. Number (pays 35:1)")
        print("2. Color (red/black) (pays 1:1)")
        print("3. Parity (even/odd) (pays 1:1)")

        choice = input("Enter bet type (1/2/3 or q to quit): ").strip().lower()

        if choice == 'q':
            print("👋 Leaving the roulette table.\n")
            break

        if choice not in ['1', '2', '3']:
            print("❌ Invalid choice.")
            continue

        if choice == '1':
            value = input("Choose a number (0, 00, 1–36): ")
            if value not in wheel.numbers:
                print("❌ Invalid number.")
                continue
            bet_type = 'number'

        elif choice == '2':
            value = input("Choose color (red/black): ").lower()
            if value not in ['red', 'black']:
                print("❌ Invalid color.")
                continue
            bet_type = 'color'

        elif choice == '3':
            value = input("Choose parity (even/odd): ").lower()
            if value not in ['even', 'odd']:
                print("❌ Invalid parity.")
                continue
            bet_type = 'parity'

        try:
            amount = int(input("Enter bet amount: $"))
        except ValueError:
            print("❌ Enter a valid number.")
            continue

        if not player.can_bet(amount):
            print("❌ Not enough balance.")
            continue

        bet = Bet(bet_type, value, amount)
        player.update_balance(-amount)

        result, color = wheel.spin()
        payout_multiplier = bet.evaluate(result, color)

        if payout_multiplier > 0:
            winnings = amount * payout_multiplier
            print(f"✅ You win ${winnings}!")
            player.update_balance(amount + winnings)
        else:
            print("💀 You lose.")

    print(f"\n🏁 Game over. Final balance: ${player.balance}\n")
