from grid import Grid
from random import choice
from tetromino import Tetromino, TetrominoI, TetrominoJ, TetrominoL, TetrominoO, TetrominoS, TetrominoT, TetrominoZ
import curses
from collections.abc import Iterable


class Game:
    GRID_SIZE_Y = 20
    GRID_SIZE_X = 10
    NEXT_PIECE_Y_OFFSET = 2
    NEXT_PIECE_X_OFFSET = 2


    def __init__(self):
        self._next_piece = self._generate_piece()
        self._grid = Grid(Game.GRID_SIZE_Y, Game.GRID_SIZE_X, self._get_new_grid_piece)


    def _get_new_grid_piece(self) -> Tetromino:
        next_piece = self._next_piece
        self._next_piece = self._generate_piece()
        return next_piece        


    def _generate_piece(self) -> Tetromino:
        return choice([
            TetrominoI,
            TetrominoJ,
            TetrominoL,
            TetrominoO,
            TetrominoS,
            TetrominoT,
            TetrominoZ
        ])(20)


    def _handle_key(self, key: int):
        match key:
            case curses.KEY_UP:
                self._grid.rotate_piece()
            case curses.KEY_DOWN:
                self._grid.move_piece(Tetromino.MoveDirection.DOWN)
            case curses.KEY_LEFT:
                self._grid.move_piece(Tetromino.MoveDirection.LEFT)
            case curses.KEY_RIGHT:
                self._grid.move_piece(Tetromino.MoveDirection.RIGHT)


    def draw(self, block_height: int, block_width: int, window):
        # Draw the grid in the centre.
        rows, cols = window.getmaxyx()
        grid_y_margin = (rows - Game.GRID_SIZE_Y*block_height) // 2 - 1
        grid_x_margin = (cols - Game.GRID_SIZE_X*block_width) // 2 - 1
        self._grid.draw(grid_y_margin, grid_x_margin, block_height, block_width, window)

        # Draw the next piece to the right of the grid.
        next_piece_y = grid_y_margin + Game.NEXT_PIECE_Y_OFFSET
        next_piece_x = grid_x_margin + Game.GRID_SIZE_X*block_width + Game.NEXT_PIECE_X_OFFSET + 2
        self._next_piece.draw(next_piece_y, next_piece_x, block_height, block_width, window)


    def tick(self, pressed_keys: Iterable[int]):
        for key in pressed_keys:
            self._handle_key(key)
        self._grid.tick()
                