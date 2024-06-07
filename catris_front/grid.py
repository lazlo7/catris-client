from enum import Enum
from collections.abc import Callable
from tetromino import Tetromino
import curses


class Grid:
    def __init__(self, size_y: int, size_x: int, piece_provider: Callable[[], Tetromino]):
        """
        Actual widget's size will be size_y + 2 x size_x + 2 to account for the borders.
        """
        self._size_y = size_y
        self._size_x = size_x
        self._cells = [[0] * size_x for _ in range(size_y)]
        self._piece_provider = piece_provider
        self.__spawn_piece()


    def __spawn_piece(self):
        self._piece = self._piece_provider()
        
        center_x = 0
        xs = []
        for _, x in self._piece.get_blocks_coords():
            if x not in xs:
                xs.append(x)
            
        xs.sort()
        xs_len = len(xs)
        center_x = xs[xs_len // 2] + xs_len % 2
        self._piece.spawn(0, self._size_x // 2 - center_x)


    def _place_piece(self):
        ys = []
        current_y = -1
        for y, x in self._piece.get_blocks_coords():
            self._cells[y][x] = self._piece.color
            if current_y < y:
                current_y = y
                ys.append(y)

        # Collapse filled rows.
        idx = len(ys) - 1
        while idx >= 0:
            y = ys[idx]
            if all(s for s in self._cells[y]):
                self._cells.pop(y)
                self._cells.insert(0, [0] * self._size_x)
            else:
                idx -= 1
                

    def _is_occupied(self, y: int, x: int) -> bool:
        return y < 0 \
            or y >= self._size_y \
            or x < 0 \
            or x >= self._size_x \
            or self._cells[y][x] != 0


    def rotate_piece(self):
        self._piece.rotate(self._is_occupied)


    def move_piece(self, direction: Tetromino.MoveDirection):
        self._piece.move(direction, self._is_occupied)


    def tick(self):
        self._piece.tick(self._is_occupied)
        if self._piece.placed:
            self._place_piece()
            self.__spawn_piece()


    def draw(self, y: int, x: int, block_height: int, block_width: int, window):
        # Draw the current piece offsetting coordinates by 1 to account for borders.
        self._piece.draw(y + 1, x + 1, block_height, block_width, window)
        
        # Draw the grid window.
        for grid_y in [0, block_height*self._size_y + 1]:
            for grid_x in range(1, block_width*self._size_x + 1):
                window.addch(y + grid_y, x + grid_x, curses.ACS_HLINE)

        for grid_x in [0, block_width*self._size_x + 1]:
            for grid_y in range(1, block_height*self._size_y + 1):
                window.addch(y + grid_y, x + grid_x, curses.ACS_VLINE)
        
        window.addch(y, x, curses.ACS_ULCORNER)
        window.addch(y, x + block_width*self._size_x + 1, curses.ACS_URCORNER)
        window.addch(y + block_height*self._size_y + 1, x, curses.ACS_LLCORNER)
        window.addch(y + block_height*self._size_y + 1, x + block_width*self._size_x + 1, curses.ACS_LRCORNER)

        # Draw filled cells.
        for grid_y, row in enumerate(self._cells):
            for grid_x, cell in enumerate(row):
                if cell:
                    for block_y in range(block_height):
                        for block_x in range(block_width):
                            window.addch(y + grid_y*block_height + block_y + 1, 
                                         x + grid_x*block_width + block_x + 1, 
                                         '#', 
                                         cell)
        