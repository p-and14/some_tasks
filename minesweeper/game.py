import random
from typing import Optional


class Box:
    """Ячейка"""
    closed: str = "■"
    opened: str = " "
    detonated: str = "*"
    flagged: str = "■f"

    def __init__(self):
        self.status = self.closed
        self.mined = False
        self.around_mine_count = 0
    
    def open(self) -> None:
        """Открытие ячейки"""
        if self.mined:
            self.status = self.detonated
        else:
            self.status = self.opened

    def put_mine(self) -> None:
        """Установить мину"""
        self.mined = True

    def flag(self) -> None:
        """Установить/убрать флаг"""
        if self.status == self.closed:
            self.status = self.flagged
        elif self.status == self.flagged:
            self.status = self.closed
    
    def __str__(self):
        return f"{self.status}"


class Map:
    def __init__(self) -> None:
        self.width = 0
        self.height = 0
        self._opened_box_count = 0
        self.mines_count = 0
        self.map = {}
    
    def _get_box_by_coords(self, x: int, y: int) -> Box:
        """Получение ячейки по координатам"""
        return self.map[y][x]
    
    def _coords_is_valid(self, x: int, y: int) -> bool:
        """Проверить валидность координат"""
        return not any((x < 0, y < 0, x > self.width - 1, y > self.height - 1))
    
    def get_closed_box_count(self) -> int:
        """Получение количества закрытых ячеек"""
        return self.width * self.height - self._opened_box_count
    
    def create_map(self, width: int, height: int) -> dict[int, Box]:
        """Сгенерировать карту"""
        self.width, self.height = width, height
        self.map = {k: [Box() for _ in range(width)] for k in range(height - 1, -1, -1)}
        return self.map

    def _set_mines_count_around_mine(self, x: int, y: int) -> None:
        """Установить количество мин соседним ячейкам

        :param x: Координата мины по оси X
        :param y: Координата мины по оси Y"""
        for coord_1 in range(x - 1, x + 2):
            for coord_2 in range(y - 1, y + 2):
                if not self._coords_is_valid(coord_1, coord_2):
                    continue
                box = self._get_box_by_coords(coord_1, coord_2)
                box.around_mine_count += 1

    def put_mines(self, count: int, x: int, y: int) -> bool:
        """Поместить мины на карту в случайном месте 
        в зависимости от первой открытой ячейки
        
        :param count: Количество мин
        :param x: Координата первой открытой ячейки по оси X
        :param y: Координата первой открытой ячейки по оси Y
        """
        self.mines_count = count
        if (self.width * self.height - 9) < count:
            return False

        mine_indexes = []

        while len(mine_indexes) < count:
            coords = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))

            if (
                coords[0] in range(x - 1, x + 2)
                and coords[1] in range(y - 1, y + 2)
                or coords in mine_indexes
            ):
                continue
            mine_indexes.append(coords)

        for coord_1, coord_2 in mine_indexes:
            box = self._get_box_by_coords(coord_1, coord_2)
            box.put_mine()
            self._set_mines_count_around_mine(coord_1, coord_2)
        return True
    
    def open_box(self, x: int, y: int) -> Optional[Box]:
        """Открыть ячейку. 
        Если вокруг нет мин — автоматически открываются соседние ячейки"""
        if not self._coords_is_valid(x, y):
            return
        
        box = self._get_box_by_coords(x, y)
        if box.mined:
            box.open()
            return box
        elif box.status == box.opened:
            return box
        
        box.open()
        self._opened_box_count += 1
        
        if box.around_mine_count > 0:
            return box
        
        for coord_1 in range(x - 1, x + 2):
            for coord_2 in range(y - 1, y + 2):
                self.open_box(coord_1, coord_2)
        return box

    def flag(self, x: int, y: int) -> None:
        """Установить/убрать флаг"""
        if not self._coords_is_valid(x, y):
            return
        
        box = self._get_box_by_coords(x, y)
        if box.closed:
            box.flag()

    def __str__(self):
        map_str = {
            k: [val.status for val in v] 
            for k, v in self.map.items()
        }
        return f"{map_str}"


class Game:
    closed: int = 0
    win: int = 1
    loss: int = -1

    def __init__(self) -> None:
        self._map = Map()
        self.status = None
        self.mines_puted = False
    
    def close(self) -> None:
        """Закончить игру"""
        self.status = self.closed

    def create_map(self, width: int, height: int) -> None:
        """Сгенерировать карту"""
        self._map.create_map(width, height)

    def put_mines(self, count: int, x: int, y: int) -> bool:
        """Поместить мины на карту"""
        self.mines_puted = self._map.put_mines(count, x, y)
        return self.mines_puted
    
    def print_map(self) -> None:
        """Вывести карту в консоль"""
        column_width = 5

        if self._map.mines_count > 0:
            print(f"\nКоличество мин: {self._map.mines_count}\n")

        for row, index in zip(self._map.map, range(self._map.height, 0, -1)):
            print("".rjust(column_width), "-----+" * (self._map.width), sep="")
            print(f"{index - 1} ".rjust(column_width), "|", sep="", end="")
            print(*[
                (f"{(box.around_mine_count 
                     if box.status == box.opened and box.around_mine_count > 0
                     else box.status)} |".rjust(column_width))
                for box in self._map.map[row]])
            
        print("".rjust(column_width), "-----+" * (self._map.width), sep="")
        print("".rjust(column_width), end="")
        print(*[f"{index - 1} ".rjust(column_width) for index in range(1, self._map.width + 1)], "\n")

    def open_box(self, x: int, y: int) -> None:
        """Открыть ячейку"""
        box = self._map.open_box(x, y)
        if not box:
            return

        if box.mined:
            self.status = self.loss
            return
        
        count_box_to_win = self._map.get_closed_box_count() - self._map.mines_count
        if count_box_to_win == 0:
            self.status = self.win
    
    def flag(self, x: int, y: int) -> None:
        """Установить/убрать флаг"""
        self._map.flag(x, y)
