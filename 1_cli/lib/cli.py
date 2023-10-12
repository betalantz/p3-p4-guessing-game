from lib.helpers import (
    exit_program,
    list_game_by_id,
    list_games,
    list_rounds,
    list_rounds_by_game_id,
    new_game,
)


def main():
    while True:
        menu()
        choice = input("> ")
        match choice:
            case "0":
                exit_program()
            case "1":
                new_game()
            case "2":
                list_games()
            case "3":
                list_game_by_id()
            case "4":
                list_rounds()
            case "5":
                list_rounds_by_game_id()
            case _:
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
