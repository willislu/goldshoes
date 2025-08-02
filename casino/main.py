# main.py

import sys
from roulette import play_roulette

def show_menu():
    print("🎰 Welcome to the Python Casino!")
    print("1. Play Roulette")
    print("0. Exit")

def main():
    while True:
        show_menu()
        choice = input("\nChoose a game (0-1): ")

        if choice == '1':
            play_roulette()
        elif choice == '0':
            print("👋 Thanks for playing. Goodbye!")
            sys.exit()
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
