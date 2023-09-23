
from helpers import (
    exit_program,
    new_game,
    list_games,
    list_game_by_id,
    list_rounds,
    list_rounds_by_game_id
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
        elif choice == "3":
            list_game_by_id()
        elif choice == "4":
            list_rounds()
        elif choice == "5":
            list_rounds_by_game_id()   
        else:
            print("Invalid choice")


def menu():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. Play new game")
    print("2: List all games")
    print("3: List game by id")
    print("4: List all rounds")
    print("5: List rounds by game id")

if __name__ == "__main__":
    main()