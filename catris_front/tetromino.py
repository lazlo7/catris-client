from collections.abc import Generator, Callable
from consts import TETROMINO_SHAPES
from enum import Enum
import curses


CoordsPredicate = Callable[[int, int], bool]


class Tetromino:
    class MoveDirection(Enum):
        LEFT = 0
        RIGHT = 1
        DOWN = 2


    def __init__(self, kind: str, ticks_per_drop: int):
        self._kind = kind
        self._y = 0
        self._x = 0
        self._ticks_per_drop = ticks_per_drop
        self._ticks_to_drop = ticks_per_drop
        self._rotation = 0
        self._spawned = False
        self._placed = False


    @property
    def placed(self) -> bool:
        return self._placed


    def _get_shape(self) -> list[list[int]]:
        return TETROMINO_SHAPES[self._kind][self._rotation]
    

    def _is_colliding(self, is_occupied: CoordsPredicate) -> bool:
        return any(is_occupied(y, x) for y, x in self.get_blocks_coords())


    def _can_move(self) -> bool:
        return self._spawned and not self._placed


    def get_blocks_coords(self) -> Generator[tuple[int, int], None, None]:
        shape = self._get_shape()
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    yield self._y + y, self._x + x


    def spawn(self, y: int, x: int):
        if self._spawned:
            raise RuntimeError('Tetromino already spawned')
        
        self._spawned = True
        self._y = y
        self._x = x


    def rotate(self, is_occupied: CoordsPredicate):
        if not self._can_move():
            return
        
        old_rotation = self._rotation
        self._rotation = (self._rotation + 1) % len(TETROMINO_SHAPES[self._kind])
        if self._is_colliding(is_occupied):
            self._rotation = old_rotation


    def move(self, direction: MoveDirection, is_occupied: CoordsPredicate) -> bool:
        if not self._can_move():
            return False
        
        dy, dx = 0, 0    
        match direction:
            case Tetromino.MoveDirection.LEFT:
                dx = -1
            case Tetromino.MoveDirection.RIGHT:
                dx = 1
            case Tetromino.MoveDirection.DOWN:
                dy = 1
        
        self._x += dx
        self._y += dy
        if self._is_colliding(is_occupied):
            self._x -= dx
            self._y -= dy
            return False
        
        return True 
        

    def tick(self, is_occupied: CoordsPredicate):
        if not self._can_move():
            return
        
        self._ticks_to_drop -= 1
        if self._ticks_to_drop == 0:
            self._ticks_to_drop = self._ticks_per_drop
            if not self.move(self.MoveDirection.DOWN, is_occupied):
                self._placed = True

    
    def draw(self, y: int, x: int, block_height: int, block_width: int, window):
        for grid_y, grid_x in self.get_blocks_coords():
            for block_y in range(block_height):
                for block_x in range(block_width):
                    window.addch(y + grid_y*block_height + block_y, x + grid_x*block_width + block_x, '#')
