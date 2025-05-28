from enum import Enum
import re

import text
from game import Game


pattern = re.compile(r'^\s*(\w+)(?:\s+(\d+))?(?:\s+(\d+))?\s*$')


class Command(Enum):
    OPEN = "open"
    FLAG = "flag"
    SHOW = "show"
    EXIT = "exit"
        
    def execute(
        self,
        game: Game,
        x: int | None = None,
        y: int | None = None
    ) -> None:
        if (
            x is not None
            and y is not None
            and not game.coords_is_valid(x, y)
        ):
            raise ValueError(text.must_be_within_a_field)
        
        if self == Command.OPEN:
            if not game.mines_puted:
                game.put_mines(x, y)
            game.open_cell(x, y)
        elif self == Command.FLAG:
            game.flag(x, y)
        elif self == Command.SHOW:
            game.print_map()
        elif self == Command.EXIT:
            game.close()
    
    @staticmethod
    def from_input(user_input: str) -> tuple['Command', int | None, int | None]:
        match = pattern.match(user_input)
        if not match:
            raise ValueError(text.incorrect_command)

        command, x, y = match.groups()

        if x is not None and y is not None:
            x, y = int(x), int(y)

        for com in Command:
            if com.value == command:
                return com, x, y
        raise ValueError(text.incorrect_command)


def main():
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

    game = Game()
    game.create_map(width, height)
    game.set_mines_count(mines_count)
    print(text.commands)

    # Commands
    while True:
        try:
            user_input = input(text.enter).strip().lower()
            command, x, y = Command.from_input(user_input)
            command.execute(game, x, y)
        except ValueError as e:
            print(e)
        
        match game.status:
            case game.loss:
                print(text.loss)
                Command.SHOW.execute(game)
                break
            case game.win:
                print(text.win)
                Command.SHOW.execute(game)
                break
            case game.closed:
                print(text.exit)
                break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
