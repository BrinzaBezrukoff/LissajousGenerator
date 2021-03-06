import sys
import os
import json

import PyQt5.QtWidgets as qt
from PyQt5 import uic, QtGui
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from lissajousgen import LissajousGenerator


script_dir = os.path.dirname(os.path.realpath(__file__))

# Настройки фигуры по умолчанию
default_settings = {
    "freq_x": 3,
    "freq_y": 2,
    "color": "midnightblue",
    "width": 1
}

# Цвета для matplotlib
default_colors = {
    "Красный": "crimson",
    "Зелёный": "green",
    "Жёлтый": "gold",
    "Синий": "midnightblue"
}

colors_path = os.path.join(script_dir, "mpl.json")

if not os.path.exists(colors_path):
    with open(colors_path, "w", encoding="utf-8") as f:
        json.dump(default_colors, f, indent=4, ensure_ascii=False)

with open(colors_path, encoding="utf-8") as f:
    mpl_color_dict = json.load(f)

with open(os.path.join(script_dir, "version.txt"), "r") as f:
    VERSION = f.readline()


class LissajousWindow(qt.QMainWindow):
    def __init__(self):
        super(LissajousWindow, self).__init__()

        # Загружаем интерфейс из файла
        uic.loadUi(os.path.join(script_dir, "main_window.ui"), self)

        self.setWindowTitle(f"Генератор фигур Лиссажу. Версия {VERSION}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(script_dir, "icon.bmp")), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.setWindowIcon(icon)

        # Создаём холст matplotlib
        self._fig = plt.figure(figsize=(4, 4), dpi=72)
        self._ax = self._fig.add_subplot(1, 1, 1)

        # Создаём qt-виджет холста для встраивания холста
        # matplotlib fig в окно Qt.
        self._fc = FigureCanvas(self._fig)
        self._fc.setParent(self)
        self._fc.resize(400, 400)
        self._fc.move(20, 20)

        plt.axis("off")
        plt.tight_layout()

        # Создание генератора
        self.figure_generator = LissajousGenerator()

        # Первичное построение фигуры
        self.plot_lissajous_figure()

        self.plot_button.clicked.connect(self.plot_button_click_handler)
        self.save_button.clicked.connect(self.save_button_click_handler)

    def plot_button_click_handler(self):
        """
        Обработчик нажатия на кнопку применения настроек
        """
        # Получаем данные из текстовых полей
        settings = dict()
        settings["freq_x"] = float(self.freq_x_lineedit.text())
        settings["freq_y"] = float(self.freq_y_lineedit.text())
        settings["color"] = mpl_color_dict[self.color_combobox.currentText()]
        settings["width"] = int(self.width_combobox.currentText())
        # Перестраиваем график
        self.plot_lissajous_figure(settings)

    def plot_lissajous_figure(self, settings=None):
        """
        Обновление фигуры
        """
        settings = settings or default_settings
        # Удаляем устаревшие данные с графика
        for line in self._ax.lines:
            line.remove()
        # Генерируем сигнал для построения
        figure = self.figure_generator.generate(settings["freq_x"], settings["freq_y"])
        # Строим график
        self._ax.plot(figure.x_arr, figure.y_arr,
                      color=settings["color"],
                      linewidth=settings["width"])
        # Обновляем холст в окне
        self._fc.draw()

    def save_button_click_handler(self):
        """
        Обработчик нажатия на кнопку сохранения настроек
        """
        home_dir = os.path.expanduser("~")
        file_path, _ = qt.QFileDialog.getSaveFileName(self,
                                                      "Сохранение изображения",
                                                      home_dir,
                                                      "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*)")
        if file_path == "":
            return
        self._fig.savefig(file_path)


if __name__ == "__main__":
    # Инициализируем приложение Qt
    app = qt.QApplication(sys.argv)

    # Создаём и настраиваем главное окно
    main_window = LissajousWindow()

    # Показываем окно
    main_window.show()

    # Запуск приложения
    # На этой строке выполнение основной программы блокируется
    # до тех пор, пока пользователь не закроет окно.
    # Вся дальнейшая работа должна вестись либо в отдельных потоках,
    # либо в обработчиках событий Qt.
    sys.exit(app.exec_())
