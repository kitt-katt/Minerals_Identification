# -*- coding: utf-8 -*-
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['QT_API'] = 'pyqt6'

# Настройка бэкенда до импорта
import matplotlib
matplotlib.use('Qt5Agg', force=True)

# Импорт и настройка PyQt6
from PyQt6 import QtCore, QtGui, QtWidgets

# Импорт matplotlib после настройки бэкенда
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

# Остальные импорты
import cv2
import numpy as np
from density_design import Ui_MainWindow

def normalize_path(path):
    """Нормализует путь к файлу для корректной работы с кириллицей"""
    return os.path.abspath(os.path.normpath(path))

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # Создаем фигуру и холст для отображения графиков
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        
        # Создаем вертикальный layout для widget
        layout = QtWidgets.QVBoxLayout(self.widget)
        layout.addWidget(self.canvas)
        
        # Добавляем панель навигации
        self.toolbar = NavigationToolbar(self.canvas, self.widget)
        layout.addWidget(self.toolbar)
        
        # Увеличиваем ширину groupBox_2 и groupBoxHistogram
        current_geometry = self.groupBox_2.geometry()
        self.groupBox_2.setGeometry(QtCore.QRect(
            current_geometry.x(),
            current_geometry.y(),
            current_geometry.width() + 50,
            current_geometry.height() + 70  # Увеличиваем высоту для кнопки
        ))
        
        # Смещаем radioButtonMainHistogram и groupBoxHistogram ниже
        current_pos = self.radioButtonMainHistogram.geometry()
        self.radioButtonMainHistogram.setGeometry(QtCore.QRect(
            current_pos.x(),
            current_pos.y() + 40,  # Смещаем на 40 пикселей вниз
            current_pos.width(),
            current_pos.height()
        ))
        
        current_pos = self.groupBoxHistogram.geometry()
        self.groupBoxHistogram.setGeometry(QtCore.QRect(
            current_pos.x(),
            current_pos.y() + 40,  # Смещаем на 40 пикселей вниз
            current_pos.width() + 50,
            current_pos.height() + 70  # Увеличиваем высоту на 70 пикселей
        ))
        
        # Настраиваем шрифт
        font = QtGui.QFont("Times New Roman", 10)
        
        # Создаем группу для главных радиокнопок
        self.main_button_group = QtWidgets.QButtonGroup(self)
        self.main_button_group.addButton(self.radioButtonMainGraph)
        self.main_button_group.addButton(self.radioButtonMainHistogram)
        
        # Устанавливаем шрифт для всех надписей в groupBox_2
        for child in self.groupBox_2.findChildren(QtWidgets.QLabel):
            child.setFont(font)
        for child in self.groupBox_2.findChildren(QtWidgets.QRadioButton):
            child.setFont(font)
            
        # Устанавливаем шрифт для всех надписей в groupBoxHistogram
        for child in self.groupBoxHistogram.findChildren(QtWidgets.QLabel):
            child.setFont(font)
        for child in self.groupBoxHistogram.findChildren(QtWidgets.QRadioButton):
            child.setFont(font)
        for child in self.groupBoxHistogram.findChildren(QtWidgets.QLineEdit):
            child.setFont(font)
        
        # Кнопка для графика плотности
        self.pushButton_3 = QtWidgets.QPushButton("Показать график", self.groupBox_2)
        font_button = QtGui.QFont("Times New Roman", 10)
        self.pushButton_3.setFont(font_button)
        # Позиционируем кнопку после радиокнопок с отступом
        self.pushButton_3.setGeometry(QtCore.QRect(10, 110, 200, 30))
        self.pushButton_3.setStyleSheet("""
            QPushButton {
                border: 2px solid #8f8f91;
                border-radius: 6px;
                background-color: #f0f0f0;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)
        self.pushButton_3.setVisible(True)
        
        # Возвращаем элементы гистограммы на исходные позиции
        self.lineEdit.setGeometry(QtCore.QRect(10, 140, 180, 25))
        self.label.setGeometry(QtCore.QRect(10, 120, self.label.width(), self.label.height()))
        self.radioButton_relatedwithlabel_6_all.setGeometry(QtCore.QRect(10, 60, self.radioButton_relatedwithlabel_6_all.width(), self.radioButton_relatedwithlabel_6_all.height()))
        self.radioButton_relatedwithlabel_7_range.setGeometry(QtCore.QRect(10, 90, self.radioButton_relatedwithlabel_7_range.width(), self.radioButton_relatedwithlabel_7_range.height()))
        
        # Кнопка для гистограммы
        self.pushButton_4 = QtWidgets.QPushButton("Показать гистограмму", self.groupBoxHistogram)
        font_button = QtGui.QFont("Times New Roman", 10)
        self.pushButton_4.setFont(font_button)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 170, 200, 30))
        self.pushButton_4.setStyleSheet("""
            QPushButton {
                border: 2px solid #8f8f91;
                border-radius: 6px;
                background-color: #f0f0f0;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)
        
        # Привязываем радиокнопки к функциям
        self.radioButtonMainGraph.toggled.connect(self.on_main_graph_selected)
        self.radioButtonMainHistogram.toggled.connect(self.on_main_histogram_selected)
        self.radioButton_relatedwithlabel_6_all.toggled.connect(self.on_full_histogram_selected)
        self.radioButton_relatedwithlabel_7_range.toggled.connect(self.on_range_histogram_selected)
        
        # Привязываем кнопки к функциям
        self.pushButton_3.clicked.connect(self.show_density_plot)
        self.pushButton_4.clicked.connect(self.show_density_histogram)
        
        # Устанавливаем начальное состояние
        self.radioButtonMainGraph.setChecked(True)
        self.on_main_graph_selected()
        
        # Скрываем неактивные элементы
        self.groupBoxHistogram.setVisible(False)
        
        # Сохраняем последний активный график
        self.last_plot = None
        
        # Инициализация изображения
        try:
            image_path = normalize_path("firstMineral.png")
            self.set_image_and_mask(image_path)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить изображение: {str(e)}")
            return
        
    def set_image_and_mask(self, image_path, hue_min=0, hue_max=180, 
                          saturation_min=0, saturation_max=255, 
                          value_min=0, value_max=255):
        """Установка изображения и параметров маски"""
        try:
            # Преобразуем путь для корректной работы с кириллицей
            image_path_encoded = np.fromfile(image_path, np.uint8)
            self.image = cv2.imdecode(image_path_encoded, cv2.IMREAD_COLOR)
            if self.image is None:
                raise ValueError(f"Не удалось загрузить изображение: {image_path}")
            self.image_hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
            
            # Сохраняем параметры маски
            self.mask_params = {
                'hue_min': hue_min,
                'hue_max': hue_max,
                'saturation_min': saturation_min,
                'saturation_max': saturation_max,
                'value_min': value_min,
                'value_max': value_max
            }
        except Exception as e:
            raise ValueError(f"Ошибка при загрузке изображения: {str(e)}")
        
    def on_main_graph_selected(self):
        """Обработчик выбора графика плотности"""
        if self.radioButtonMainGraph.isChecked():
            self.labelWidget.setText("График плотности")
            self.groupBox_2.setVisible(True)
            self.groupBoxHistogram.setVisible(False)
            # Восстанавливаем последний график, если он был
            if hasattr(self, 'last_plot') and self.last_plot == 'density':
                self.show_density_plot()
            
    def on_main_histogram_selected(self):
        """Обработчик выбора гистограммы"""
        if self.radioButtonMainHistogram.isChecked():
            self.labelWidget.setText("Гистограмма")
            self.groupBox_2.setVisible(False)
            self.groupBoxHistogram.setVisible(True)
            # Восстанавливаем последнюю гистограмму, если она была
            if hasattr(self, 'last_plot') and self.last_plot == 'histogram':
                self.show_density_histogram()
            
    def on_full_histogram_selected(self):
        """Обработчик выбора полной гистограммы"""
        if self.radioButton_relatedwithlabel_6_all.isChecked():
            self.lineEdit.setEnabled(False)
            self.label.setEnabled(False)
            
    def on_range_histogram_selected(self):
        """Обработчик выбора диапазона гистограммы"""
        if self.radioButton_relatedwithlabel_7_range.isChecked():
            self.lineEdit.setEnabled(True)
            self.label.setEnabled(True)
            
    def show_density_plot(self):
        """Отображение графика плотности"""
        # Проверяем, выбран ли канал
        if not (self.radioButton_hue_graph.isChecked() or 
                self.radioButton_saturation_graph.isChecked() or 
                self.radioButton_value_graph.isChecked()):
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Выберите канал для отображения")
            return
            
        # Очищаем предыдущий график
        self.figure.clear()
        
        # Получаем данные из изображения с текущими параметрами маски
        dictionary = self.applying_mask(self.image_hsv, **self.mask_params)
        
        # Создаем один график
        ax = self.figure.add_subplot(111)
        
        # Получаем данные для графиков
        list_hue, list_saturation, list_value = [], [], []
        for key in dictionary:
            hsv = eval(key)
            list_hue.append(hsv[0])
            list_saturation.append(hsv[1])
            list_value.append(hsv[2])
            
        # Строим график плотности
        count_hue_channel, count_saturation_channel, count_value_channel = [], [], []
        for i in range(0,256):
            count_hue_channel.append(list_hue.count(i))
            count_saturation_channel.append(list_saturation.count(i))
            count_value_channel.append(list_value.count(i))
        x = [i for i in range(0,256)]
        
        # Отображаем выбранный канал
        if self.radioButton_hue_graph.isChecked():
            ax.plot(x, count_hue_channel, color="red", label="Hue")
        elif self.radioButton_saturation_graph.isChecked():
            ax.plot(x, count_saturation_channel, color="black", label="Saturation")
        else:
            ax.plot(x, count_value_channel, color="blue", label="Value")
            
        ax.legend()
        
        # Обновляем холст
        self.figure.tight_layout()
        self.canvas.draw()
        
        # Сохраняем тип последнего графика
        self.last_plot = 'density'
        
    def show_density_histogram(self):
        """Отображение гистограммы плотности"""
        try:
            # Очищаем предыдущий график
            self.figure.clear()
            
            # Получаем данные из изображения с текущими параметрами маски
            dictionary = self.applying_mask(self.image_hsv, **self.mask_params)
            
            # Создаем график
            ax = self.figure.add_subplot(111)
            
            # Получаем данные для гистограммы
            dictionary_count = {}
            for j in range(max(dictionary.values())+1):
                if j in dictionary.values():
                    dictionary_count[j] = list(dictionary.values()).count(j)
            xdata = list(dictionary_count.keys())
            ydata = list(dictionary_count.values())
            
            if self.radioButton_relatedwithlabel_6_all.isChecked():
                # Отображаем полную гистограмму
                ax.bar(xdata, ydata)
            else:
                # Отображаем гистограмму в выбранном диапазоне
                try:
                    range_text = self.lineEdit.text().strip()
                    if not range_text:
                        raise ValueError("Введите диапазон")
                    
                    if '-' not in range_text:
                        raise ValueError("Используйте формат 'начало-конец'")
                        
                    start, end = map(int, range_text.split('-'))
                    if start >= end:
                        raise ValueError("Начальное значение должно быть меньше конечного")
                        
                    filtered_xdata = [x for x in xdata if start <= x <= end]
                    if not filtered_xdata:
                        raise ValueError(f"Нет данных в диапазоне {start}-{end}")
                        
                    filtered_ydata = [ydata[xdata.index(x)] for x in filtered_xdata]
                    ax.bar(filtered_xdata, filtered_ydata)
                except ValueError as e:
                    QtWidgets.QMessageBox.warning(self, "Ошибка", str(e))
                    return
                    
            # Обновляем холст
            self.figure.tight_layout()
            self.canvas.draw()
            
            # Сохраняем тип последнего графика
            self.last_plot = 'histogram'
            
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Ошибка", f"Ошибка при построении гистограммы: {str(e)}")
        
    def applying_mask(self, image_hsv, hue_min, hue_max, saturation_min, saturation_max, value_min, value_max) -> dict:
        """Применение маски к изображению"""
        dictionary_filtered = {}
        width, height, _ = image_hsv.shape
        for i in range(width):
            for j in range(height):
                pixel = image_hsv[i, j]
                hue = int(pixel[0])
                saturation = int(pixel[1])
                value = int(pixel[2])
                if (hue in range(hue_min,hue_max)) and (saturation in range(saturation_min,saturation_max)) and (value in range(value_min,value_max)):
                    if f"{[hue, saturation, value]}" in dictionary_filtered:
                        dictionary_filtered[f"{[hue, saturation, value]}"] += 1
                    else:
                        dictionary_filtered[f"{[hue, saturation, value]}"] = 1
        return dictionary_filtered

if __name__ == "__main__":
    import sys
    from PyQt6 import QtWidgets
    
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    
    # Получаем путь к текущей директории скрипта
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, "firstMineral.png")
    
    # Диагностическая информация
    print(f"Текущая директория: {current_dir}")
    print(f"Путь к изображению: {image_path}")
    print(f"Файл существует: {os.path.exists(image_path)}")
    
    try:
        # Проверяем наличие файла
        if not os.path.exists(image_path):
            raise ValueError(f"Файл не найден: {image_path}")
            
        # Проверяем права доступа
        if not os.access(image_path, os.R_OK):
            raise ValueError(f"Нет прав на чтение файла: {image_path}")
            
        window.set_image_and_mask(
            image_path=image_path,
            hue_min=0,
            hue_max=180,
            saturation_min=0,
            saturation_max=255,
            value_min=0,
            value_max=255
        )
    except Exception as e:
        QtWidgets.QMessageBox.critical(window, "Ошибка", f"Не удалось загрузить изображение: {str(e)}")
        print(f"Ошибка при загрузке изображения: {str(e)}")
        sys.exit(1)
        
    window.show()
    sys.exit(app.exec()) 