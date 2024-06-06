from collections.abc import Generator, Callable
from enum import Enum
import curses
from abc import ABC, abstractmethod
from colors import Colors


CoordsPredicate = Callable[[int, int], bool]


class Tetromino(ABC):
    class MoveDirection(Enum):
        LEFT = 0
        RIGHT = 1
        DOWN = 2


    def __init__(self, color: int, ticks_per_drop: int):
        self._y = 0
        self._x = 0
        self._color = color
        self._ticks_per_drop = ticks_per_drop
        self._ticks_to_drop = ticks_per_drop
        self._rotation = 0
        self._spawned = False
        self._placed = False


    @property
    def placed(self) -> bool:
        return self._placed


    @property
    def color(self) -> int:
        return self._color


    @abstractmethod
    def _get_shape(self) -> list[list[bool]]:
        pass


    @abstractmethod
    def _get_next_rotation(self) -> int:
        pass


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
        self._rotation = self._get_next_rotation()
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
                    window.addch(y + grid_y*block_height + block_y, 
                                 x + grid_x*block_width + block_x, 
                                 curses.ACS_CKBOARD, 
                                 self._color)


class TetrominoO(Tetromino):
    def __init__(self, ticks_per_drop: int):
        super().__init__(
            Colors.make(curses.COLOR_RED, curses.COLOR_RED),
            ticks_per_drop
        )
    

    def _get_shape(self) -> list[list[bool]]:
        T = True
        return [
            [T, T],
            [T, T]
        ]
    

    def _get_next_rotation(self) -> int:
        return 0
    

class TetrominoI(Tetromino):
    def __init__(self, ticks_per_drop: int):
        super().__init__(
            Colors.make(curses.COLOR_CYAN, curses.COLOR_CYAN),
            ticks_per_drop
        )
    

    def _get_shape(self) -> list[list[bool]]:
        T, F = True, False
        match self._rotation:
            case 0:
                return [
                    [F, F, F, F],
                    [F, F, F, F],
                    [T, T, T, T],
                ]
            case 1:
                return [
                    [F, T],
                    [F, T],
                    [F, T],
                    [F, T],
                ]
        raise RuntimeError('Invalid rotation')
    

    def _get_next_rotation(self) -> int:
        return self._rotation ^ 1 
    

class TetrominoS(Tetromino):
    def __init__(self, ticks_per_drop: int):
        super().__init__(
            Colors.make(curses.COLOR_GREEN, curses.COLOR_GREEN),
            ticks_per_drop
        )
    

    def _get_shape(self) -> list[list[bool]]:
        T, F = True, False
        match self._rotation:
            case 0:
                return [
                    [F, T, T],
                    [T, T, F],
                ]
            case 1:
                return [
                    [T, F],
                    [T, T],
                    [F, T],
                ]
        raise RuntimeError('Invalid rotation')
    

    def _get_next_rotation(self) -> int:
        return self._rotation ^ 1
    

class TetrominoZ(Tetromino):
    def __init__(self, ticks_per_drop: int):
        super().__init__(
            Colors.make(curses.COLOR_YELLOW, curses.COLOR_YELLOW),
            ticks_per_drop
        )

    def _get_shape(self) -> list[list[bool]]:
        T, F = True, False
        match self._rotation:
            case 0:
                return [
                    [T, T, F],
                    [F, T, T],
                ]
            case 1:
                return [
                    [F, T],
                    [T, T],
                    [T, F],
                ]
        raise RuntimeError('Invalid rotation')
    

    def _get_next_rotation(self) -> int:
        return self._rotation ^ 1
    

class TetrominoL(Tetromino):
    def __init__(self, ticks_per_drop: int):
        super().__init__(
            Colors.make(curses.COLOR_MAGENTA, curses.COLOR_MAGENTA),
            ticks_per_drop
        )
    

    def _get_shape(self) -> list[list[bool]]:
        T, F = True, False
        match self._rotation:
            case 0:
                return [
                    [T, F],
                    [T, F],
                    [T, T],
                ]
            case 1:
                return [
                    [T, T, T],
                    [T, F, F],
                ]
            case 2:
                return [
                    [T, T],
                    [F, T],
                    [F, T],
                ]
            case 3:
                return [
                    [F, F, T],
                    [T, T, T],
                ]
        raise RuntimeError('Invalid rotation')
    

    def _get_next_rotation(self) -> int:
        return (self._rotation + 1) % 4
    

class TetrominoJ(Tetromino):
    def __init__(self, ticks_per_drop: int):
        super().__init__(
            Colors.make(curses.COLOR_BLUE, curses.COLOR_BLUE),
            ticks_per_drop
        )
    

    def _get_shape(self) -> list[list[bool]]:
        T, F = True, False
        match self._rotation:
            case 0:
                return [
                    [F, T],
                    [F, T],
                    [T, T],
                ]
            case 1:
                return [
                    [T, F, F],
                    [T, T, T],
                ]
            case 2:
                return [
                    [T, T],
                    [T, F],
                    [T, F],
                ]
            case 3:
                return [
                    [T, T, T],
                    [F, F, T],
                ]
        raise RuntimeError('Invalid rotation')
    

    def _get_next_rotation(self) -> int:
        return (self._rotation + 1) % 4
    

class TetrominoT(Tetromino):
    def __init__(self, ticks_per_drop: int):
        super().__init__(
            Colors.make(curses.COLOR_WHITE, curses.COLOR_WHITE),
            ticks_per_drop
        )

    def _get_shape(self) -> list[list[bool]]:
        T, F = True, False
        match self._rotation:
            case 0:
                return [
                    [T, T, T],
                    [F, T, F],
                ]
            case 1:
                return [
                    [F, T],
                    [T, T],
                    [F, T],
                ]
            case 2:
                return [
                    [F, T, F],
                    [T, T, T],
                ]
            case 3:
                return [
                    [F, T, F],
                    [F, T, T],
                    [F, T, F],
                ]
        raise RuntimeError('Invalid rotation')
    

    def _get_next_rotation(self) -> int:
        return (self._rotation + 1) % 4
