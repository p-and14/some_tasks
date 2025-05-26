from game import Game

import text


class Command:
    def __init__(self, game: Game):
        self._game = game

    def open(self, x: int, y: int) -> None:
        """Открыть ячейку"""
        self._game.open_box(x, y)
    
    def flag(self, x: int, y: int) -> None:
        """Установить/убрать флаг"""
        self._game.flag(x, y)

    def show(self) -> None:
        """Показать поле"""
        self._game.print_map()
    
    def exit(self) -> None:
        """Закончить игру"""
        self._game.close()


def main():
    game = Game()
    command = Command(game)

    # Map parameters
    while True:
        try:
            width, height, mines_count = map(int, input(text.first).split(" "))
            if mines_count < 1:
                print(text.mines_count_greater_1)
                continue
            elif width < 4 or height < 4:
                print(text.w_h_greater_3)
                continue
            elif width > 30 or height > 30:
                print(text.w_h_less_30)
                continue
            elif (width * height - 9) <= mines_count:
                print(text.too_many_mines)
                continue
            break
        except ValueError:
            print(text.invalid_format)

    game.create_map(width, height)
    command.show()
    print(text.commands)

    # Commands
    while True:
        user_input = input(text.enter).strip().lower().split()

        if not hasattr(command, user_input[0]):
            print(text.unknown_command)
            continue

        if len(user_input) > 2:
            if not user_input[1].isdigit() or not user_input[2].isdigit():
                print(text.must_be_integer)
                continue
            
            x, y = int(user_input[1]), int(user_input[2])
            if x < 0 or x > width - 1 or y < 0 or y > height - 1:
                print(text.must_be_within_a_field)
                continue

            if user_input[0] == "open":
                if not game.mines_puted:
                    mines_puted = game.put_mines(mines_count, x, y)
                    if not mines_puted:
                        print(text.problem_with_mines)
                        break
                command.open(x, y)
                
            elif user_input[0] == "flag":
                game.flag(x, y)
        elif len(user_input) == 1:
            if user_input[0] == "show":
                command.show()
            elif user_input[0] == "exit":
                command.exit()
        else:
            print(text.invalid_format)

        if game.status == game.loss:
            print(text.loss)
            command.show()
            break
        elif game.status == game.win:
            print(text.win)
            command.show()
            break
        elif game.status == game.closed:
            print(text.exit)
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    