
from helpers import (
    exit_program,
    list_games,
    new_game
)


def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            new_game()
        elif choice == "2":
            list_games()    
        else:
            print("Invalid choice")


def menu():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. Play new game")
    print("2: List all games")

if __name__ == "__main__":
    main()