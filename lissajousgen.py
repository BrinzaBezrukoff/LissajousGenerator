import numpy as np


class LissajousFigure:
    """
    Фигуры Лиссажу.
    Задаётся набором точек с координатами x и y.
    """
    def __init__(self, x_array, y_array):
        self.x_arr = x_array
        self.y_arr = y_array


class LissajousGenerator:
    """
    Генерирует фигуры Лиссажу с заданными параметрами
    """
    def __init__(self, start=0, end=2*np.pi, resolution=100):
        self.__start = start
        self.__end = end
        self.__resolution = resolution

    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, value):
        self.__start = value

    @property
    def end(self):
        return self.__end

    @end.setter
    def end(self, value):
        self.__end = value

    @property
    def resolution(self):
        return self.__resolution

    @resolution.setter
    def resolution(self, value):
        self.__resolution = value

    def generate(self, freq_x, freq_y):
        """
        Генерирует фигуру (массивы x и y координат точек) с заданными частотами.
        """
        t = np.linspace(self.start, self.end, self.resolution)
        x = np.sin(freq_x * t)
        y = np.sin(freq_y * t)
        return LissajousFigure(x, y)
