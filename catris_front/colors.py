import curses


class Colors:
    __REGISTERED = [True] + [False] * 63


    @staticmethod
    def __register(code: int, foreground: int, background: int):
        # 0-th pair is reserved for the default black-black color pair.
        Colors.__REGISTERED[code] = True
        curses.init_pair(code, foreground, background)


    @staticmethod
    def make(foreground: int, background: int):
        code = foreground*8 + background
        if not Colors.__REGISTERED[code]:
            Colors.__register(code, foreground, background)
        return curses.color_pair(code)
