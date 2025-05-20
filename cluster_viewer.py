import sys
import os
import numpy as np
import cv2
import matplotlib
matplotlib.use('QtAgg')  # Меняем на QtAgg для совместимости с PyQt6
import matplotlib.pyplot as plt
import ast
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from mpl_toolkits.mplot3d import Axes3D
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QSpinBox, QCheckBox, 
                            QComboBox, QGroupBox, QPushButton, QSlider, QFileDialog,
                            QSplitter, QFrame, QSizePolicy, QTabWidget, QDoubleSpinBox,
                            QFormLayout, QScrollArea, QTableWidget, QTableWidgetItem, QColorDialog,
                            QAbstractItemView)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont
import traceback
from sklearn.cluster import KMeans, Birch, OPTICS, DBSCAN

# Импортируем функции из GeneralSolution1stSemester.py
def applying_mask(image_hsv, hue_min, hue_max, saturation_min, saturation_max, value_min, value_max):
    list_red, list_green, list_blue = [], [], []
    width, height, _ = image_hsv.shape
    for i in range(width):
        for j in range(height):
            pixel = image_hsv[i, j]
            hue = int(pixel[0])
            saturation = int(pixel[1])
            value = int(pixel[2])
            if (hue in range(hue_min, hue_max+1)) and (saturation in range(saturation_min, saturation_max+1)) and (value in range(value_min, value_max+1)):
                list_red.append(hue)
                list_green.append(saturation)
                list_blue.append(value)
    return list_red, list_green, list_blue

def applying_maskDictionary(image_hsv, hue_min, hue_max, saturation_min, saturation_max, value_min, value_max):
    dictionary_filtered = {}
    width, height, _ = image_hsv.shape
    for i in range(width):
        for j in range(height):
            pixel = image_hsv[i, j]
            hue = int(pixel[0])
            saturation = int(pixel[1])
            value = int(pixel[2])
            if (hue in range(hue_min, hue_max+1)) and (saturation in range(saturation_min, saturation_max+1)) and (value in range(value_min, value_max+1)):
                if f"{[hue, saturation, value]}" in dictionary_filtered:
                     dictionary_filtered[f"{[hue, saturation, value]}"] += 1
                else:
                     dictionary_filtered[f"{[hue, saturation, value]}"] = 1
    return dictionary_filtered

def threshold_method(dictionary_after_filter, threshold):
    list_hue, list_saturation, list_value = [], [], []
    for key_str, count_value in dictionary_after_filter.items():
        if count_value >= threshold:
            hsv_list = eval(key_str)
            list_hue.append(hsv_list[0])
            list_saturation.append(hsv_list[1])
            list_value.append(hsv_list[2])
    return list_hue, list_saturation, list_value

def threshold_method_with_bins(dictionary_after_filter, h_bins, s_bins, v_bins, threshold):
    h_step = 180.0 / h_bins
    s_step = 256.0 / s_bins
    v_step = 256.0 / v_bins

    bins_count = [[[0 for _ in range(v_bins)] for _ in range(s_bins)] for _ in range(h_bins)]

    # Отладочная информация
    print(f"Количество бинов: H={h_bins}, S={s_bins}, V={v_bins}")
    print(f"Порог: {threshold}")
    print(f"Количество точек в словаре: {len(dictionary_after_filter)}")

    for key_str, count_value in dictionary_after_filter.items():
        # Безопасное преобразование строки в список
        # Удаляем пробелы и квадратные скобки
        hsv_str = key_str.replace(' ', '').strip('[]')
        h, s, v = map(int, hsv_str.split(','))

        h_idx = int(h // h_step)
        s_idx = int(s // s_step)
        v_idx = int(v // v_step)

        h_idx = min(h_idx, h_bins - 1)
        s_idx = min(s_idx, s_bins - 1)
        v_idx = min(v_idx, v_bins - 1)

        bins_count[h_idx][s_idx][v_idx] += count_value

    # Отладочная информация о заполнении бинов
    non_empty_bins = sum(1 for i in range(h_bins) 
                        for j in range(s_bins) 
                        for k in range(v_bins) 
                        if bins_count[i][j][k] > 0)
    print(f"Количество непустых бинов: {non_empty_bins}")
    print(f"Максимальное количество точек в бине: {max(max(max(row) for row in plane) for plane in bins_count)}")

    hue_list, sat_list, val_list = [], [], []

    for key_str, count_value in dictionary_after_filter.items():
        # Безопасное преобразование строки в список
        hsv_str = key_str.replace(' ', '').strip('[]')
        h, s, v = map(int, hsv_str.split(','))

        h_idx = int(h // h_step)
        s_idx = int(s // s_step)
        v_idx = int(v // v_step)
        h_idx = min(h_idx, h_bins - 1)
        s_idx = min(s_idx, s_bins - 1)
        v_idx = min(v_idx, v_bins - 1)

        if bins_count[h_idx][s_idx][v_idx] >= threshold:
            hue_list.append(h)
            sat_list.append(s)
            val_list.append(v)

    # Отладочная информация о результатах
    print(f"Количество точек после фильтрации: {len(hue_list)}")
    return hue_list, sat_list, val_list

def plot_2d_fixed_value_heatmap(hue_list, sat_list, val_list, fixed_axis='H', fixed_value=50, show_axes=('S', 'V'), bins=100, cmap='viridis'):
    arr = {
        'H': np.array(hue_list),
        'S': np.array(sat_list),
        'V': np.array(val_list),
    }

    mask = (arr[fixed_axis] == fixed_value)
    x = arr[show_axes[0]][mask]
    y = arr[show_axes[1]][mask]

    heatmap, xedges, yedges = np.histogram2d(x, y, bins=bins)

    plt.figure(figsize=(6, 5))
    plt.imshow(heatmap.T, origin='lower', aspect='auto',
               extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
               cmap=cmap)
    plt.colorbar(label="Частота")
    plt.xlabel(show_axes[0])
    plt.ylabel(show_axes[1])
    plt.title(f"Тепловая карта: {show_axes[0]} vs {show_axes[1]} при {fixed_axis} = {fixed_value}")
    plt.tight_layout()
    plt.show()

def plot_3d_subspace(hue_list, sat_list, val_list, h_range=(0, 180), s_range=(0, 255), v_range=(0, 255), point_size=5):
    H = np.array(hue_list)
    S = np.array(sat_list)
    V = np.array(val_list)

    mask = ((H >= h_range[0]) & (H <= h_range[1]) &
            (S >= s_range[0]) & (S <= s_range[1]) &
            (V >= v_range[0]) & (V <= v_range[1]))

    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(H[mask], S[mask], V[mask], s=point_size, alpha=0.6)
    ax.set_xlabel('Hue')
    ax.set_ylabel('Saturation')
    ax.set_zlabel('Value')
    title_parts = [f"H∈{h_range}", f"S∈{s_range}", f"V∈{v_range}"]
    ax.set_title("3D‑часть пространства: " + ", ".join(title_parts))
    plt.tight_layout()
    plt.show()

class Segmentator:
    def __init__(self):
        self.clusters = []
        self.counts_in_cluster = []
        self.raw_points = {}
        
    def data_from_image(self, image):
        dictionary_filtered = {}
        width, height, _ = image.shape
        for i in range(width):
            for j in range(height):
                pixel = image[i, j]
                hue = int(pixel[0])
                saturation = int(pixel[1])
                value = int(pixel[2])
                key = f"{[hue, saturation, value]}"
                if key in dictionary_filtered:
                    dictionary_filtered[key] += 1
                else:
                    dictionary_filtered[key] = 1
        return dictionary_filtered

    def euclidean_distance(self, first_point, second_point):
        return ((second_point[0] - first_point[0])**2 + 
                (second_point[1] - first_point[1])**2 + 
                (second_point[2] - first_point[2])**2)**0.5

    def check_difference_channels(self, point, next_point, difference_channels):
        return (abs(point[0] - next_point[0]) + 
                abs(point[1] - next_point[1]) + 
                abs(point[2] - next_point[2])) < difference_channels

    def check_difference_in_density(self, next_point, avg_density, difference_in_density):
        point_density = self.raw_points[next_point]
        if point_density <= avg_density:
            return True
        return ((abs(point_density - avg_density) * 100) / avg_density) <= difference_in_density

    def check_distance(self, point, next_point, radius):
        return self.euclidean_distance(point, next_point) <= radius

    def average_hsv_color(self, cluster):
        cluster_np = np.array(cluster)
        avg_hsv = np.mean(cluster_np, axis=0).astype(int)
        avg_rgb = cv2.cvtColor(np.uint8([[avg_hsv]]), cv2.COLOR_HSV2RGB)[0, 0]
        return avg_rgb / 255

    def merge_small_clusters(self, clusters, counts, min_size=100):
        if not clusters:
            return clusters, counts
        
        # Находим большие кластеры
        large_clusters = [i for i, count in enumerate(counts) if count >= min_size]
        if not large_clusters:
            return clusters, counts
        
        # Создаем массив центроидов больших кластеров
        centroids = []
        for idx in large_clusters:
            cluster = np.array(clusters[idx])
            centroids.append(np.mean(cluster, axis=0))
        centroids = np.array(centroids)
        
        # Объединяем маленькие кластеры с ближайшими большими
        new_clusters = [clusters[i] for i in large_clusters]
        new_counts = [counts[i] for i in large_clusters]
        
        for i, (cluster, count) in enumerate(zip(clusters, counts)):
            if count < min_size:
                # Находим ближайший центроид
                cluster_center = np.mean(np.array(cluster), axis=0)
                distances = [self.euclidean_distance(cluster_center, centroid) 
                           for centroid in centroids]
                nearest_idx = np.argmin(distances)
                # Добавляем точки в ближайший большой кластер
                new_clusters[nearest_idx].extend(cluster)
                new_counts[nearest_idx] += count
        
        return new_clusters, new_counts

    def segment(self, image_hsv, difference_channels, difference_in_density, radius):
        self.raw_points = self.data_from_image(image_hsv)
        clusters = []
        counts_points_in_clusters = []
        checked = []
        for point in self.raw_points:
            if point in checked:
                continue
            point_density = self.raw_points[point]
            checked.append(point)
            cluster = [eval(point)]
            count_points_in_cluster = point_density
            avg_density = count_points_in_cluster / len(cluster)
            for next_point in self.raw_points:
                if (next_point not in checked and
                    self.check_distance(eval(point), eval(next_point), radius) and
                    self.check_difference_channels(eval(point), eval(next_point), difference_channels) and
                    self.check_difference_in_density(next_point, avg_density, difference_in_density)):
                    cluster.append(eval(next_point))
                    checked.append(next_point)
                    count_points_in_cluster += self.raw_points[next_point]
                    avg_density = count_points_in_cluster / len(cluster)
            clusters.append(cluster)
            counts_points_in_clusters.append(count_points_in_cluster)
        self.clusters, self.counts_in_cluster = self.merge_small_clusters(
            clusters, counts_points_in_clusters)
        return self.clusters, self.counts_in_cluster

    def get_cluster_colors(self, mode='hsv'):
        if mode == 'colormap':
            n = len(self.clusters)
            cmap = matplotlib.colormaps.get_cmap('tab20' if n <= 20 else 'hsv')
            colors = [cmap(i / max(1, n-1))[:3] for i in range(n)]
            return colors
        else:
            # Средний HSV -> RGB
            colors = []
            for cluster in self.clusters:
                colors.append(self.average_hsv_color(cluster))
            return colors

class ClusterViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Просмотрщик кластеров HSV")
        self.setMinimumSize(700, 700)  # Минимальный размер окна
        self.resize(1200, 800)         # Стартовый размер окна
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #999999;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #4a86e8;
                color: white;
                border-radius: 4px;
                padding: 5px 10px;
                min-height: 25px;
            }
            QPushButton:hover {
                background-color: #3a76d8;
            }
            QPushButton:pressed {
                background-color: #2a66c8;
            }
            QLabel {
                font-size: 12px;
            }
            QSpinBox, QComboBox {
                min-height: 25px;
                border: 1px solid #999999;
                border-radius: 3px;
                padding: 2px 5px;
            }
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: #cccccc;
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background-color: #4a86e8;
                border: 1px solid #5c5c5c;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
        """)
        
        # Инициализация переменных
        self.image = None
        self.image_hsv = None
        self.hue_list = []
        self.saturation_list = []
        self.value_list = []
        self.dictionary_filtered = {}
        self.filtered_hue_list = []
        self.filtered_saturation_list = []
        self.filtered_value_list = []
        
        # Инициализация сегментатора
        self.segmentator = Segmentator()
        self.clusters = []
        self.counts_in_cluster = []
        self.cluster_colors = []
        
        # Добавляем атрибуты для диапазонов HSV
        self.target_h_range = (0, 180)
        self.target_s_range = (0, 255)
        self.target_v_range = (0, 255)
        
        # Инициализация слайдеров диапазонов для 3D режима
        self.range_sliders = {}
        
        # Настройка слайдеров H
        self.range_sliders['H'] = {'min': QSlider(Qt.Orientation.Horizontal), 'max': QSlider(Qt.Orientation.Horizontal)}
        self.range_sliders['H']['min'].setRange(0, 180)
        self.range_sliders['H']['max'].setRange(0, 180)
        self.range_sliders['H']['min'].setValue(0)
        self.range_sliders['H']['max'].setValue(180)
        
        # Настройка слайдеров S и V
        for channel in ['S', 'V']:
            self.range_sliders[channel] = {'min': QSlider(Qt.Orientation.Horizontal), 'max': QSlider(Qt.Orientation.Horizontal)}
            self.range_sliders[channel]['min'].setRange(0, 255)
            self.range_sliders[channel]['max'].setRange(0, 255)
            self.range_sliders[channel]['min'].setValue(0)
            self.range_sliders[channel]['max'].setValue(255)
        
        # Подключение сигналов
        for channel in ['H', 'S', 'V']:
            self.range_sliders[channel]['min'].valueChanged.connect(self.update_plot)
            self.range_sliders[channel]['max'].valueChanged.connect(self.update_plot)
        
        # Настройка интерфейса
        self.setup_ui()
        
        # Инициализация параметров для самописного метода кластеризации
        self.current_param_controls = None
        self.update_clustering_method()
        
        # Загрузка тестового изображения
        self.load_test_image()
        
        # Инициализация начальных значений осей
        self.update_available_axes()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)
        splitter.setHandleWidth(8)

        # Панель управления с прокруткой
        control_panel = QWidget()
        control_panel.setMinimumWidth(300)
        control_panel.setMaximumWidth(420)
        control_layout = QVBoxLayout(control_panel)
        control_layout.setContentsMargins(10, 10, 10, 10)
        control_layout.setSpacing(12)

        # --- Отступ сверху для блока 'Режим отображения' ---
        control_layout.addSpacing(10)
        # Группа загрузки изображения
        image_group = QGroupBox("Загрузка изображения")
        image_layout = QVBoxLayout(image_group)
        load_image_btn = QPushButton("Загрузить изображение")
        load_image_btn.setIcon(QIcon.fromTheme("document-open"))
        load_image_btn.clicked.connect(self.load_image)
        image_layout.addWidget(load_image_btn)
        self.image_info = QLabel("Изображение не загружено")
        image_layout.addWidget(self.image_info)
        control_layout.addWidget(image_group)

        # Группа режимов отображения
        mode_group = QGroupBox("Режим отображения")
        mode_layout = QVBoxLayout(mode_group)
        self.tab_widget = QTabWidget()

        # --- Базовый режим ---
        base_tab = QWidget()
        base_layout = QVBoxLayout(base_tab)
        base_layout.setContentsMargins(0, 0, 0, 0)
        base_layout.setSpacing(8)

        # Переключатель режима
        mode_row = QHBoxLayout()
        mode_row.addWidget(QLabel("Режим:"))
        self.view_mode = QComboBox()
        self.view_mode.addItems(["2D режим", "3D режим"])
        self.view_mode.currentTextChanged.connect(self.update_display_options)
        mode_row.addWidget(self.view_mode)
        mode_row.addStretch()
        base_layout.addLayout(mode_row)

        # 2D настройки
        self.settings_2d = QGroupBox()
        self.settings_2d.setTitle("")
        settings_2d_layout = QVBoxLayout(self.settings_2d)
        settings_2d_layout.setContentsMargins(8, 8, 8, 8)
        settings_2d_layout.setSpacing(8)
        # Фиксированная ось
        settings_2d_layout.addWidget(QLabel("Фиксированная ось:"))
        self.fixed_axis = QComboBox()
        self.fixed_axis.addItems(["H", "S", "V"])
        self.fixed_axis.currentTextChanged.connect(self.update_available_axes)
        settings_2d_layout.addWidget(self.fixed_axis)
        # Значение
        settings_2d_layout.addWidget(QLabel("Значение:"))
        self.fixed_value = QSpinBox()
        self.fixed_value.setMinimum(0)
        self.fixed_value.setMaximum(255)
        self.fixed_value.setValue(50)
        self.fixed_value.valueChanged.connect(self.update_plot)
        settings_2d_layout.addWidget(self.fixed_value)
        # Оси
        settings_2d_layout.addWidget(QLabel("Оси:"))
        self.x_axis = QComboBox()
        self.y_axis = QComboBox()
        axes_row = QHBoxLayout()
        axes_row.addWidget(self.x_axis)
        axes_row.addWidget(QLabel("и"))
        axes_row.addWidget(self.y_axis)
        axes_widget = QWidget()
        axes_widget.setLayout(axes_row)
        settings_2d_layout.addWidget(axes_widget)
        # Размерность сетки
        settings_2d_layout.addWidget(QLabel("Размерность сетки:"))
        grid_row = QHBoxLayout()
        self.grid_size_x = QSpinBox()
        self.grid_size_x.setMinimum(2)
        self.grid_size_x.setMaximum(50)
        self.grid_size_x.setValue(10)
        self.grid_size_x.valueChanged.connect(self.update_plot)
        self.grid_size_y = QSpinBox()
        self.grid_size_y.setMinimum(2)
        self.grid_size_y.setMaximum(50)
        self.grid_size_y.setValue(10)
        self.grid_size_y.valueChanged.connect(self.update_plot)
        grid_row.addWidget(self.grid_size_x)
        grid_row.addWidget(QLabel("x"))
        grid_row.addWidget(self.grid_size_y)
        grid_widget = QWidget()
        grid_widget.setLayout(grid_row)
        settings_2d_layout.addWidget(grid_widget)
        base_layout.addWidget(self.settings_2d)

        # 3D настройки
        self.settings_3d = QGroupBox("Диапазоны осей")
        settings_3d_layout = QVBoxLayout(self.settings_3d)
        for axis in ['H', 'S', 'V']:
            row = QHBoxLayout()
            label = QLabel(f"{axis}:")
            min_slider = QSlider(Qt.Orientation.Horizontal)
            max_slider = QSlider(Qt.Orientation.Horizontal)
            if axis == 'H':
                min_slider.setRange(0, 180)
                max_slider.setRange(0, 180)
                min_slider.setValue(0)
                max_slider.setValue(180)
            else:
                min_slider.setRange(0, 255)
                max_slider.setRange(0, 255)
                min_slider.setValue(0)
                max_slider.setValue(255)
            min_value_label = QLabel(str(min_slider.value()))
            max_value_label = QLabel(str(max_slider.value()))
            def make_value_updater(label):
                return lambda val: label.setText(str(val))
            min_slider.valueChanged.connect(make_value_updater(min_value_label))
            max_slider.valueChanged.connect(make_value_updater(max_value_label))
            min_slider.valueChanged.connect(self.update_plot)
            max_slider.valueChanged.connect(self.update_plot)
            row.addWidget(label)
            row.addWidget(min_value_label)
            row.addWidget(min_slider)
            row.addWidget(max_slider)
            row.addWidget(max_value_label)
            self.range_sliders[axis] = {'min': min_slider, 'max': max_slider, 'min_label': min_value_label, 'max_label': max_value_label}
            settings_3d_layout.addLayout(row)
        base_layout.addWidget(self.settings_3d)
        self.settings_2d.show()
        self.settings_3d.hide()

        # --- ДОБАВЛЯЕМ: Блок для чекбоксов кластеров на вкладке 'Просмотрщик кластеров' ---
        # Теперь чекбоксы будут добавляться в settings_2d/settings_3d
        # (Удаляем все обращения к self.clusters_checkbox_layout и update_cluster_info до их инициализации)
        # ...
        # --- Режим кластеризации ---
        segment_tab = QWidget()
        segment_layout = QVBoxLayout(segment_tab)
        # Выбор метода кластеризации
        method_layout = QHBoxLayout()
        method_layout.addWidget(QLabel("Метод кластеризации:"))
        self.cluster_method = QComboBox()
        self.cluster_method.addItems([
            "Сегментация по HSV", "KMeans", "Birch", "OPTICS", "DBSCAN"
        ])
        self.cluster_method.currentTextChanged.connect(self.update_clustering_method)
        method_layout.addWidget(self.cluster_method)
        segment_layout.addLayout(method_layout)
        # Параметры метода
        self.method_params_widget = QGroupBox("Параметры сегментации")
        self.method_params_layout = QVBoxLayout(self.method_params_widget)
        segment_layout.addWidget(self.method_params_widget)
        # Чекбоксы кластеров (создаём ДО любых обращений к ним)
        self.clusters_checkbox_widget = QWidget()
        self.clusters_checkbox_layout = QVBoxLayout(self.clusters_checkbox_widget)
        segment_layout.addWidget(self.clusters_checkbox_widget)
        # Теперь можно вызывать update_cluster_info() или обращаться к self.clusters_checkbox_layout
        # Режим отображения сегментации
        display_mode_layout = QHBoxLayout()
        display_mode_layout.addWidget(QLabel("Режим отображения:"))
        self.segment_display_mode = QComboBox()
        self.segment_display_mode.addItems(["3D пространство", "Изображение с кластерами"])
        self.segment_display_mode.currentTextChanged.connect(self.update_segmentation)
        display_mode_layout.addWidget(self.segment_display_mode)
        segment_layout.addLayout(display_mode_layout)
        # Информация о кластерах
        self.cluster_info = QLabel("Кластеры не найдены")
        segment_layout.addWidget(self.cluster_info)
        # Кнопка кластеризации
        self.run_clustering_btn = QPushButton("Провести кластеризацию")
        self.run_clustering_btn.clicked.connect(self.run_clustering)
        segment_layout.addWidget(self.run_clustering_btn)
        
        # Кнопка для отображения диаграммы цель/промах
        self.show_target_diagram_btn = QPushButton("Диаграмма цель/промах")
        self.show_target_diagram_btn.clicked.connect(self.show_target_diagram)
        segment_layout.addWidget(self.show_target_diagram_btn)
        
        # Добавляем вкладки
        print('Добавляю вкладку Просмотрщик кластеров')
        self.tab_widget.addTab(base_tab, "Просмотрщик кластеров")
        print('Добавляю вкладку Режим кластеризации')
        self.tab_widget.addTab(segment_tab, "Режим кластеризации")
        mode_layout.addWidget(self.tab_widget)
        control_layout.addWidget(mode_group)

        # Группа фильтрации
        self.filter_group = QGroupBox("Фильтрация")
        filter_layout = QVBoxLayout(self.filter_group)
        
        # Выбор метода фильтрации
        filter_method_layout = QHBoxLayout()
        filter_method_layout.addWidget(QLabel("Метод фильтрации:"))
        self.filter_method = QComboBox()
        self.filter_method.addItems(["Порог по количеству точек", "Порог по областям"])
        self.filter_method.currentTextChanged.connect(self.update_filter_settings)
        filter_method_layout.addWidget(self.filter_method)
        filter_layout.addLayout(filter_method_layout)
        
        # Кнопка применить фильтрацию
        self.apply_filter_btn = QPushButton("Применить фильтрацию")
        self.apply_filter_btn.clicked.connect(self.on_apply_filter_clicked)
        filter_layout.addWidget(self.apply_filter_btn)
        
        # Настройки порога по количеству точек
        self.weight_settings = QGroupBox("Настройки порога")
        weight_layout = QVBoxLayout(self.weight_settings)
        weight_threshold_layout = QHBoxLayout()
        weight_threshold_layout.addWidget(QLabel("Порог:"))
        self.weight_threshold = QSpinBox()
        self.weight_threshold.setMinimum(1)
        self.weight_threshold.setMaximum(1000)
        self.weight_threshold.setValue(1)
        # self.weight_threshold.valueChanged.connect(self.update_plot)  # Отключено
        weight_threshold_layout.addWidget(self.weight_threshold)
        weight_layout.addLayout(weight_threshold_layout)
        filter_layout.addWidget(self.weight_settings)
        
        # Настройки порога по областям
        self.region_settings = QGroupBox("Настройки областей")
        region_layout = QVBoxLayout(self.region_settings)
        
        # Количество областей для каждой оси
        self.region_bins = {}
        for axis in ['H', 'S', 'V']:
            axis_layout = QHBoxLayout()
            axis_layout.addWidget(QLabel(f"Количество областей по {axis}:"))
            bins_spinbox = QSpinBox()
            bins_spinbox.setMinimum(1)
            bins_spinbox.setMaximum(50)
            bins_spinbox.setValue(1)
            # bins_spinbox.valueChanged.connect(self.update_plot)  # Отключено
            self.region_bins[axis] = bins_spinbox
            axis_layout.addWidget(bins_spinbox)
            region_layout.addLayout(axis_layout)
        
        # Порог для областей
        region_threshold_layout = QHBoxLayout()
        region_threshold_layout.addWidget(QLabel("Порог для областей:"))
        self.region_threshold = QSpinBox()
        self.region_threshold.setMinimum(1)
        self.region_threshold.setMaximum(1000)
        self.region_threshold.setValue(1)
        # self.region_threshold.valueChanged.connect(self.update_plot)  # Отключено
        region_threshold_layout.addWidget(self.region_threshold)
        region_layout.addLayout(region_threshold_layout)
        
        self.region_settings.hide()
        filter_layout.addWidget(self.region_settings)
        
        control_layout.addWidget(self.filter_group)

        # --- Блок управления масками ---
        mask_group = QGroupBox("Маски")
        mask_layout = QVBoxLayout(mask_group)
        # Кнопки управления
        btn_row = QHBoxLayout()
        self.btn_create = QPushButton("Создать")
        self.btn_delete = QPushButton("Удалить")
        self.btn_delete_all = QPushButton("Удалить все")
        self.btn_update = QPushButton("Обновить")
        btn_row.addWidget(self.btn_create)
        btn_row.addWidget(self.btn_delete)
        btn_row.addWidget(self.btn_delete_all)
        btn_row.addWidget(self.btn_update)
        mask_layout.addLayout(btn_row)
        # Таблица масок
        self.mask_table = QTableWidget()
        self.mask_table.setColumnCount(4)
        self.mask_table.setHorizontalHeaderLabels(["Минерал", "Цвет", "%", "Диапазоны"])
        self.mask_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.mask_table.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.mask_table.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        self.mask_table.setMinimumHeight(120)
        self.mask_table.horizontalHeader().setStretchLastSection(True)
        self.mask_table.setColumnWidth(0, 90)
        self.mask_table.setColumnWidth(1, 50)
        self.mask_table.setColumnWidth(2, 50)
        self.mask_table.setColumnWidth(3, 180)
        self.mask_table.itemChanged.connect(self.on_mask_table_item_changed)
        mask_layout.addWidget(self.mask_table)
        control_layout.addWidget(mask_group)
        # --- Логика кнопок (заглушки, можно доработать) ---
        self.btn_create.clicked.connect(self.create_mask)
        self.btn_delete.clicked.connect(self.delete_selected_masks)
        self.btn_delete_all.clicked.connect(self.delete_all_masks)
        self.btn_update.clicked.connect(self.update_selected_masks)
        self.masks = []
        self.add_mask_to_table = self.add_mask_to_table
        self.refresh_mask_table = self.refresh_mask_table
        self.create_mask = self.create_mask
        self.delete_selected_masks = self.delete_selected_masks
        self.delete_all_masks = self.delete_all_masks
        self.update_selected_masks = self.update_selected_masks

        # Обернём control_panel в QScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(control_panel)
        scroll_area.setMinimumWidth(320)
        scroll_area.setMaximumWidth(440)
        splitter.addWidget(scroll_area)

        # График
        plot_widget = QWidget()
        plot_layout = QVBoxLayout(plot_widget)
        plot_layout.setContentsMargins(0, 0, 0, 0)
        plot_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.figure = plt.figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.toolbar = NavigationToolbar(self.canvas, plot_widget)
        plot_layout.addWidget(self.toolbar)
        plot_layout.addWidget(self.canvas)
        splitter.addWidget(plot_widget)
        splitter.setSizes([500, 700])
        main_layout.addWidget(splitter)
        self.update_available_axes()
        # Скрывать/показывать фильтрацию в зависимости от режима
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        self.on_tab_changed(self.tab_widget.currentIndex())
    
    def update_display_options(self):
        """Обновление отображения настроек в зависимости от выбранного режима"""
        is_2d = self.view_mode.currentText() == "2D режим"
        self.settings_2d.setVisible(is_2d)
        self.settings_3d.setVisible(not is_2d)
        self.update_available_axes()
        
        # Сохраняем результаты кластеризации при переключении режимов
        if hasattr(self, 'clusters') and self.clusters:
            self.update_segmentation_display()
        else:
            self.update_plot()

    def update_filter_settings(self):
        """Обновление отображения настроек фильтрации"""
        is_weight = self.filter_method.currentText() == "Порог по количеству точек"
        self.weight_settings.setVisible(is_weight)
        self.region_settings.setVisible(not is_weight)
        self.apply_filtering()
        self.update_plot()

    def apply_filtering(self):
        """Применение фильтрации к данным"""
        if not hasattr(self, 'dictionary_filtered') or not self.dictionary_filtered:
            return

        method = self.filter_method.currentText()
        
        if method == "Порог по количеству точек":
            # Применяем порог по количеству точек
            threshold = self.weight_threshold.value()
            self.filtered_hue_list, self.filtered_saturation_list, self.filtered_value_list = threshold_method(
                self.dictionary_filtered, threshold)
        else:
            # Применяем порог по областям
            h_bins = self.region_bins['H'].value()
            s_bins = self.region_bins['S'].value()
            v_bins = self.region_bins['V'].value()
            threshold = self.region_threshold.value()
            self.filtered_hue_list, self.filtered_saturation_list, self.filtered_value_list = threshold_method_with_bins(
                self.dictionary_filtered, h_bins, s_bins, v_bins, threshold)

    def update_available_axes(self):
        """Обновление доступных осей в зависимости от фиксированной оси"""
        try:
            if not hasattr(self, 'fixed_axis') or self.fixed_axis is None or self.fixed_axis.parent() is None:
                return
            if not hasattr(self, 'x_axis') or self.x_axis is None or self.x_axis.parent() is None:
                return
            if not hasattr(self, 'y_axis') or self.y_axis is None or self.y_axis.parent() is None:
                return
            # Отключаем старые соединения, если они есть
            try:
                self.x_axis.currentTextChanged.disconnect()
            except Exception:
                pass
            try:
                self.y_axis.currentTextChanged.disconnect()
            except Exception:
                pass
            fixed = self.fixed_axis.currentText()
            if not fixed:  # Если текст пустой, используем значение по умолчанию
                fixed = "H"
                self.fixed_axis.setCurrentText(fixed)
            available_axes = [axis for axis in ["H", "S", "V"] if axis != fixed]
            # Сохраняем текущие значения
            current_x = self.x_axis.currentText()
            current_y = self.y_axis.currentText()
            # Обновляем списки
            self.x_axis.clear()
            self.y_axis.clear()
            self.x_axis.addItems(available_axes)
            self.y_axis.addItems(available_axes)
            # Устанавливаем значения по умолчанию, если текущие значения недопустимы
            if not current_x or not current_y or current_x not in available_axes or current_y not in available_axes or current_x == current_y:
                self.x_axis.setCurrentText(available_axes[0])
                self.y_axis.setCurrentText(available_axes[1])
            else:
                self.x_axis.setCurrentText(current_x)
                self.y_axis.setCurrentText(current_y)
            # Обновляем максимальное значение для fixed_value
            if fixed == "H":
                self.fixed_value.setMaximum(180)
            else:
                self.fixed_value.setMaximum(255)
            # Подключаем новые соединения
            self.x_axis.currentTextChanged.connect(self.prevent_same_axes)
            self.y_axis.currentTextChanged.connect(self.prevent_same_axes)
            self.update_plot()
        except Exception as e:
            print(f"Ошибка при обновлении осей: {str(e)}")
    
    def prevent_same_axes(self, text):
        """Предотвращение выбора одинаковых осей"""
        if self.x_axis.currentText() == self.y_axis.currentText():
            sender = self.sender()
            other = self.y_axis if sender == self.x_axis else self.x_axis
            available = [axis for axis in ["H", "S", "V"] 
                        if axis != self.fixed_axis.currentText() 
                        and axis != text]
            if available:
                other.setCurrentText(available[0])
    
    def prepare_data(self):
        """Подготовка данных для визуализации"""
        if self.image_hsv is None:
            return
            
        # Получаем диапазоны HSV из выбранной маски
        h_min, h_max, s_min, s_max, v_min, v_max = 0, 180, 0, 255, 0, 255
        selected = self.mask_table.selectedItems()
        if selected:
            # Берём первую выбранную маску
            row = selected[0].row()
            mask = self.masks[row]
            # Ожидается формат 'H(0,180)S(0,255)V(0,255)'
            import re
            m = re.match(r"H\((\d+),(\d+)\)S\((\d+),(\d+)\)V\((\d+),(\d+)\)", mask['ranges'])
            if m:
                h_min, h_max, s_min, s_max, v_min, v_max = map(int, m.groups())
                # Обновляем диапазоны для всех режимов
                self.target_h_range = (h_min, h_max)
                self.target_s_range = (s_min, s_max)
                self.target_v_range = (v_min, v_max)
                
                # Обновляем слайдеры в 3D режиме
                self.range_sliders['H']['min'].setValue(h_min)
                self.range_sliders['H']['max'].setValue(h_max)
                self.range_sliders['S']['min'].setValue(s_min)
                self.range_sliders['S']['max'].setValue(s_max)
                self.range_sliders['V']['min'].setValue(v_min)
                self.range_sliders['V']['max'].setValue(v_max)
        
        # Получаем точки и словарь
        self.hue_list, self.saturation_list, self.value_list = applying_mask(
            self.image_hsv, h_min, h_max, s_min, s_max, v_min, v_max)
        self.dictionary_filtered = applying_maskDictionary(
            self.image_hsv, h_min, h_max, s_min, s_max, v_min, v_max)
        
        # Инициализируем отфильтрованные данные
        self.filtered_hue_list = self.hue_list.copy()
        self.filtered_saturation_list = self.saturation_list.copy()
        self.filtered_value_list = self.value_list.copy()
        
        # Применяем фильтрацию
        self.apply_filtering()
        
        # Обновляем отображение в зависимости от текущего режима
        if self.tab_widget.currentIndex() == 1:  # Режим сегментации
            if hasattr(self, 'clusters') and self.clusters:
                self.update_segmentation_display()
        else:  # Режим просмотрщика кластеров
            self.update_plot()
    
    def update_plot(self):
        """Обновление графика"""
        if not hasattr(self, 'x_axis') or self.x_axis is None or self.x_axis.parent() is None:
            return
        if not hasattr(self, 'y_axis') or self.y_axis is None or self.y_axis.parent() is None:
            return
        if not hasattr(self, 'fixed_axis') or self.fixed_axis is None or self.fixed_axis.parent() is None:
            return
        if not hasattr(self, 'hue_list') or not self.hue_list:
            return
        try:
            self.figure.clear()
            if self.view_mode.currentText() == "2D режим":
                # 2D режим — только точки маски с фильтрацией
                fixed_axis = self.fixed_axis.currentText()
                fixed_value = self.fixed_value.value()
                if not self.x_axis.currentText() or not self.y_axis.currentText():
                    return
                show_axes = (self.x_axis.currentText(), self.y_axis.currentText())
                bins = (self.grid_size_x.value(), self.grid_size_y.value())
                ax = self.figure.add_subplot(111)
                arr = {
                    'H': np.array(self.filtered_hue_list),
                    'S': np.array(self.filtered_saturation_list),
                    'V': np.array(self.filtered_value_list),
                }
                delta = 2
                mask = np.abs(arr[fixed_axis] - fixed_value) <= delta
                x = arr[show_axes[0]][mask]
                y = arr[show_axes[1]][mask]
                if len(x) > 0 and len(y) > 0:
                    heatmap, xedges, yedges = np.histogram2d(x, y, bins=bins)
                    im = ax.imshow(heatmap.T, origin='lower', aspect='auto',
                             extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
                             cmap='viridis')
                    ax.set_xticks(xedges)
                    ax.set_yticks(yedges)
                    ax.set_xticklabels([f'{x:.0f}' for x in xedges], rotation=45, ha='right')
                    ax.set_yticklabels([f'{y:.0f}' for y in yedges])
                    ax.set_xticks(xedges, minor=True)
                    ax.set_yticks(yedges, minor=True)
                    ax.grid(True, which='minor', color='#b0b0b0', linestyle='-', linewidth=0.7)
                    for xval in xedges:
                        ax.axvline(xval, color='#b0b0b0', linewidth=0.7, linestyle='-')
                    for yval in yedges:
                        ax.axhline(yval, color='#b0b0b0', linewidth=0.7, linestyle='-')
                    self.figure.colorbar(im, label="Частота")
                    ax.set_xlabel(show_axes[0])
                    ax.set_ylabel(show_axes[1])
                    ax.set_title(f"Тепловая карта: {show_axes[0]} vs {show_axes[1]} при {fixed_axis} = {fixed_value}")
            else:
                # 3D режим
                if hasattr(self, 'clusters') and self.clusters:
                    # Получаем диапазоны из слайдеров
                    h_range = (self.range_sliders['H']['min'].value(), self.range_sliders['H']['max'].value())
                    s_range = (self.range_sliders['S']['min'].value(), self.range_sliders['S']['max'].value())
                    v_range = (self.range_sliders['V']['min'].value(), self.range_sliders['V']['max'].value())
                    method = self.filter_method.currentText()
                    ax = self.figure.add_subplot(111, projection='3d')
                    method_title = self.cluster_method.currentText()
                    method_titles = {
                        "Сегментация по HSV": "Сегментация по HSV",
                        "KMeans": "Кластеризация методом KMeans",
                        "Birch": "Кластеризация методом Birch",
                        "OPTICS": "Кластеризация методом OPTICS",
                        "DBSCAN": "Кластеризация методом DBSCAN"
                    }
                    title = method_titles.get(method_title, "Кластеризация")
                    ax.set_title(title)
                    legend_elements = []
                    for i, (cluster, color) in enumerate(zip(self.clusters, self.cluster_colors)):
                        cluster = np.array(cluster)
                        # Фильтрация по диапазонам
                        mask = (
                            (cluster[:, 0] >= h_range[0]) & (cluster[:, 0] <= h_range[1]) &
                            (cluster[:, 1] >= s_range[0]) & (cluster[:, 1] <= s_range[1]) &
                            (cluster[:, 2] >= v_range[0]) & (cluster[:, 2] <= v_range[1])
                        )
                        filtered_cluster = cluster[mask]
                        # Фильтрация по методу
                        if method == "Порог по количеству точек":
                            from collections import Counter
                            points = [tuple(map(int, pt)) for pt in filtered_cluster]
                            counter = Counter(points)
                            threshold = self.weight_threshold.value()
                            filtered_points = [pt for pt, cnt in counter.items() if cnt >= threshold]
                            filtered_cluster = np.array(filtered_points)
                        elif method == "Порог по областям":
                            h_bins = self.region_bins['H'].value()
                            s_bins = self.region_bins['S'].value()
                            v_bins = self.region_bins['V'].value()
                            threshold = self.region_threshold.value()
                            h_step = 180.0 / h_bins
                            s_step = 256.0 / s_bins
                            v_step = 256.0 / v_bins
                            bins_count = [[[0 for _ in range(v_bins)] for _ in range(s_bins)] for _ in range(h_bins)]
                            for pt in filtered_cluster:
                                h, s, v = map(int, pt)
                                h_idx = int(h // h_step)
                                s_idx = int(s // s_step)
                                v_idx = int(v // v_step)
                                h_idx = min(h_idx, h_bins - 1)
                                s_idx = min(s_idx, s_bins - 1)
                                v_idx = min(v_idx, v_bins - 1)
                                bins_count[h_idx][s_idx][v_idx] += 1
                            filtered_points = []
                            for pt in filtered_cluster:
                                h, s, v = map(int, pt)
                                h_idx = int(h // h_step)
                                s_idx = int(s // s_step)
                                v_idx = int(v // v_step)
                                h_idx = min(h_idx, h_bins - 1)
                                s_idx = min(s_idx, s_bins - 1)
                                v_idx = min(v_idx, v_bins - 1)
                                if bins_count[h_idx][s_idx][v_idx] >= threshold:
                                    filtered_points.append(pt)
                            filtered_cluster = np.array(filtered_points)
                        if len(filtered_cluster) > 0:
                            ax.scatter(filtered_cluster[:, 0], filtered_cluster[:, 1], filtered_cluster[:, 2], color=[color], s=5)
                            from matplotlib.lines import Line2D
                            rgb = (np.array(color) * 255).astype(np.uint8)
                            hex_color = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
                            count = len(filtered_cluster)
                            legend_elements.append(Line2D([0], [0], marker='o', color='w', label=f"Кластер {i+1}: {count} точек",
                                                          markerfacecolor=hex_color, markersize=5))
                    ax.set_xlabel("H (Оттенок)")
                    ax.set_ylabel("S (Насыщенность)")
                    ax.set_zlabel("V (Яркость)")
                    if legend_elements:
                        ax.legend(handles=legend_elements, loc='upper right', title="Легенда кластеров", fontsize=8, title_fontsize=9)
                else:
                    ax = self.figure.add_subplot(111, projection='3d')
                    H = np.array(self.hue_list)
                    S = np.array(self.saturation_list)
                    V = np.array(self.value_list)
                    h_range = (self.range_sliders['H']['min'].value(), self.range_sliders['H']['max'].value())
                    s_range = (self.range_sliders['S']['min'].value(), self.range_sliders['S']['max'].value())
                    v_range = (self.range_sliders['V']['min'].value(), self.range_sliders['V']['max'].value())
                    mask = (
                        (H >= h_range[0]) & (H <= h_range[1]) &
                        (S >= s_range[0]) & (S <= s_range[1]) &
                        (V >= v_range[0]) & (V <= v_range[1])
                    )
                    ax.scatter(H[mask], S[mask], V[mask], s=5, alpha=0.6)
                    ax.set_xlabel('Hue')
                    ax.set_ylabel('Saturation')
                    ax.set_zlabel('Value')
                    ax.set_title("3D‑пространство по выбранной маске и диапазонам")
            self.canvas.draw()
        except Exception as e:
            print(f"Ошибка при обновлении графика: {str(e)}")
    
    def update_segmentation(self):
        """Обновление сегментации и отображения"""
        if self.image_hsv is None:
            return
            
        try:
            # Выполняем сегментацию
            self.clusters, self.counts_in_cluster = self.segmentator.segment(
                self.image_hsv,
                self.current_param_controls['difference_channels'].value(),
                self.current_param_controls['difference_density'].value(),
                self.current_param_controls['radius'].value()
            )
            
            # Получаем цвета кластеров
            self.cluster_colors = self.segmentator.get_cluster_colors(mode='hsv')
            
            # Обновляем информацию о кластерах
            self.update_cluster_info()
            
            # Обновляем отображение
            self.update_segmentation_display()
            
        except Exception as e:
            print(f"Ошибка при обновлении сегментации: {str(e)}")
    
    def update_cluster_info(self):
        def clear_layout(layout):
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                elif item.layout() is not None:
                    clear_layout(item.layout())

        clear_layout(self.clusters_checkbox_layout)
        for settings in [self.settings_2d, self.settings_3d]:
            for i in reversed(range(settings.layout().count())):
                item = settings.layout().itemAt(i)
                widget = item.widget()
                if isinstance(widget, QWidget) and widget.layout() is not None:
                    has_checkbox = False
                    for j in range(widget.layout().count()):
                        if isinstance(widget.layout().itemAt(j).widget(), QCheckBox):
                            has_checkbox = True
                            break
                    if has_checkbox:
                        widget.deleteLater()

        if not self.clusters:
            self.clusters_checkbox_layout.addWidget(QLabel("Кластеры не найдены"))
            return

        total_points = sum(self.counts_in_cluster)
        title = QLabel(f"Найдено кластеров: {len(self.clusters)} Всего точек: {total_points}")
        self.clusters_checkbox_layout.addWidget(title)

        self.cluster_checkboxes = []
        self.viewer_cluster_checkboxes_2d = []
        self.viewer_cluster_checkboxes_3d = []

        for i, (count, color) in enumerate(zip(self.counts_in_cluster, self.cluster_colors)):
            # --- Кластеризация ---
            row = QHBoxLayout()
            rgb = (np.array(color) * 255).astype(np.uint8)
            hex_color = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
            color_label = QLabel()
            color_label.setFixedSize(16, 16)
            color_label.setStyleSheet(f"background-color: {hex_color}; border: 1px solid #888;")
            row.addWidget(color_label)
            cb = QCheckBox()
            cb.setChecked(True)
            row.addWidget(cb)
            row.addWidget(QLabel(f"Кластер {i+1}: {count} точек"))
            row.addStretch()
            self.clusters_checkbox_layout.addLayout(row)
            self.cluster_checkboxes.append(cb)

            # --- Просмотрщик 2D ---
            vrow2d = QHBoxLayout()
            vcolor_label2d = QLabel()
            vcolor_label2d.setFixedSize(16, 16)
            vcolor_label2d.setStyleSheet(f"background-color: {hex_color}; border: 1px solid #888;")
            vrow2d.addWidget(vcolor_label2d)
            vcb2d = QCheckBox()
            vcb2d.setChecked(True)
            vrow2d.addWidget(vcb2d)
            vrow2d.addWidget(QLabel(f"Кластер {i+1}: {count} точек"))
            vrow2d.addStretch()
            container2d = QWidget()
            container2d.setLayout(vrow2d)
            self.settings_2d.layout().addWidget(container2d)
            self.viewer_cluster_checkboxes_2d.append(vcb2d)

            # --- Просмотрщик 3D ---
            vrow3d = QHBoxLayout()
            vcolor_label3d = QLabel()
            vcolor_label3d.setFixedSize(16, 16)
            vcolor_label3d.setStyleSheet(f"background-color: {hex_color}; border: 1px solid #888;")
            vrow3d.addWidget(vcolor_label3d)
            vcb3d = QCheckBox()
            vcb3d.setChecked(True)
            vrow3d.addWidget(vcb3d)
            vrow3d.addWidget(QLabel(f"Кластер {i+1}: {count} точек"))
            vrow3d.addStretch()
            container3d = QWidget()
            container3d.setLayout(vrow3d)
            self.settings_3d.layout().addWidget(container3d)
            self.viewer_cluster_checkboxes_3d.append(vcb3d)

            # --- Синхронизация ---
            def on_main_checkbox_state_changed(idx):
                state = self.cluster_checkboxes[idx].isChecked()
                # Синхронизируем чекбоксы во вкладках, блокируя сигналы
                for vcb in (self.viewer_cluster_checkboxes_2d[idx], self.viewer_cluster_checkboxes_3d[idx]):
                    vcb.blockSignals(True)
                    vcb.setChecked(state)
                    vcb.blockSignals(False)
                # Обновляем график только один раз
                self.update_segmentation_display()

            def on_viewer_checkbox_state_changed(idx, which):
                state = (self.viewer_cluster_checkboxes_2d[idx] if which == '2d' else self.viewer_cluster_checkboxes_3d[idx]).isChecked()
                # Синхронизируем основной чекбокс
                self.cluster_checkboxes[idx].blockSignals(True)
                self.cluster_checkboxes[idx].setChecked(state)
                self.cluster_checkboxes[idx].blockSignals(False)
                # Синхронизируем между 2d и 3d
                other = self.viewer_cluster_checkboxes_3d if which == '2d' else self.viewer_cluster_checkboxes_2d
                other[idx].blockSignals(True)
                other[idx].setChecked(state)
                other[idx].blockSignals(False)
                # Обновляем график только один раз
                self.update_segmentation_display()

            cb.stateChanged.connect(lambda state, idx=i: on_main_checkbox_state_changed(idx))
            self.viewer_cluster_checkboxes_2d[i].stateChanged.connect(lambda state, idx=i: on_viewer_checkbox_state_changed(idx, '2d'))
            self.viewer_cluster_checkboxes_3d[i].stateChanged.connect(lambda state, idx=i: on_viewer_checkbox_state_changed(idx, '3d'))

    def update_segmentation_display(self):
        """Обновление отображения сегментации"""
        if not self.clusters or not hasattr(self, 'cluster_checkboxes'):
            return
        self.figure.clear()
        selected = [i for i, cb in enumerate(self.cluster_checkboxes) if cb.isChecked()]
        method = self.cluster_method.currentText()
        method_titles = {
            "Сегментация по HSV": "Сегментация по HSV",
            "KMeans": "Кластеризация методом KMeans",
            "Birch": "Кластеризация методом Birch",
            "OPTICS": "Кластеризация методом OPTICS",
            "DBSCAN": "Кластеризация методом DBSCAN"
        }
        title = method_titles.get(method, "Кластеризация")
        if self.segment_display_mode.currentText() == "3D пространство":
            ax = self.figure.add_subplot(111, projection='3d')
            ax.set_title(title)
            legend_elements = []
            for i in selected:
                cluster = np.array(self.clusters[i])
                color = self.cluster_colors[i]  # RGB (0..1)
                ax.scatter(cluster[:, 0], cluster[:, 1], cluster[:, 2], color=[color], s=5)
                from matplotlib.lines import Line2D
                r, g, b = color
                hex_color = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
                count = self.counts_in_cluster[i]
                legend_elements.append(Line2D([0], [0], marker='o', color='w', label=f"Кластер {i+1}: {count} точек",
                                              markerfacecolor=hex_color, markersize=5))
            ax.set_xlabel("H (Оттенок)")
            ax.set_ylabel("S (Насыщенность)")
            ax.set_zlabel("V (Яркость)")
            if legend_elements:
                ax.legend(handles=legend_elements, loc='upper right', title="Легенда кластеров", fontsize=8, title_fontsize=9)
        else:
            ax = self.figure.add_subplot(111)
            result_image = self.image.copy()
            for idx in selected:
                cluster = self.clusters[idx]
                color = self.cluster_colors[idx]  # RGB (0..1)
                bgr = (np.array(color) * 255).astype(np.uint8)[::-1]  # RGB -> BGR
                for point in cluster:
                    h, s, v = point
                    h_mask = self.image_hsv[:, :, 0] == h
                    s_mask = self.image_hsv[:, :, 1] == s
                    v_mask = self.image_hsv[:, :, 2] == v
                    mask = h_mask & s_mask & v_mask
                    result_image[mask] = bgr
            ax.imshow(cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB))
            ax.set_title(title)
            ax.axis('off')
        self.canvas.draw()
    
    def set_image(self, image_path):
        """Загрузка и подготовка изображения"""
        try:
            # Загрузка изображения с поддержкой кириллицы
            image_path_encoded = np.fromfile(image_path, np.uint8)
            self.image = cv2.imdecode(image_path_encoded, cv2.IMREAD_COLOR)
            if self.image is None:
                raise ValueError(f"Не удалось загрузить изображение: {image_path}")
            
            # Преобразование в HSV
            self.image_hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
            
            # Обновляем информацию об изображении
            height, width = self.image.shape[:2]
            self.image_info.setText(f"Изображение: {os.path.basename(image_path)}\nРазмер: {width}x{height}")
            
            # Подготовка данных
            self.prepare_data()
            
            # Обновление отображения
            if self.tab_widget.currentIndex() == 1:  # Режим сегментации
                self.update_segmentation()
            else:
                self.update_plot()
            
        except Exception as e:
            print(f"Ошибка при загрузке изображения: {str(e)}")
    
    def load_image(self):
        """Загрузка изображения через диалог выбора файла"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Изображения (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.set_image(file_path)
    
    def load_test_image(self):
        """Загрузка тестового изображения для демонстрации"""
        try:
            # Создаем тестовое изображение с градиентом HSV
            height, width = 100, 100
            image = np.zeros((height, width, 3), dtype=np.uint8)
            
            for y in range(height):
                for x in range(width):
                    h = int(180 * x / width)
                    s = int(255 * y / height)
                    v = int(255 * y / height)  # Теперь V меняется по вертикали
                    # Преобразуем HSV в BGR для OpenCV
                    hsv_image = np.zeros((1, 1, 3), dtype=np.uint8)
                    hsv_image[0, 0] = [h, s, v]
                    bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
                    b, g, r = bgr_image[0, 0]
                    image[y, x] = [b, g, r]
            
            self.image = image
            # Преобразование в HSV для анализа
            self.image_hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
            
            # Обновляем информацию об изображении
            self.image_info.setText(f"Тестовое изображение\nРазмер: {width}x{height}")
            
            # Подготовка данных
            self.prepare_data()
            
            # Обновление отображения
            if self.tab_widget.currentIndex() == 1:  # Режим сегментации
                self.update_segmentation()
            else:
                self.update_plot()
            
            print("Тестовое изображение успешно создано")
            
        except Exception as e:
            print(f"Ошибка при создании тестового изображения: {str(e)}")
            # Создаем простое изображение в случае ошибки
            self.image = np.ones((100, 100, 3), dtype=np.uint8) * 255
            self.image_hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
            self.prepare_data()
            self.update_plot()

    # --- ФУНКЦИЯ ДЛЯ ОБНОВЛЕНИЯ ПАРАМЕТРОВ МЕТОДА ---
    def update_clustering_method(self):
        method = self.cluster_method.currentText()
        if method == 'Сегментация по HSV':
            self.method_params_widget.setTitle("Параметры сегментации")
        else:
            self.method_params_widget.setTitle(f"Параметры {method}")
        # Очищаем только layout с параметрами метода
        while self.method_params_layout.count():
            child = self.method_params_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())
        # Добавляем новые параметры метода
        if method == 'Сегментация по HSV':
            widget, controls = self.create_segmentator_params()
            self.current_param_controls = controls
        else:
            widget, controls = self.create_method_params(method)
            self.current_param_controls = controls
        self.method_params_layout.addWidget(widget)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            elif item.layout() is not None:
                self.clear_layout(item.layout())

    def create_method_params(self, method):
        """Создание виджета с параметрами для указанного метода"""
        params_widget = QWidget()
        params_layout = QFormLayout(params_widget)
        params_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        params_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft)
        controls = {}
        
        def make_row(widget):
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)
            widget.setMinimumWidth(100)
            widget.setMinimumHeight(28)
            widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            widget.setStyleSheet('''
                QSpinBox, QDoubleSpinBox {
                    background: white;
                    border: 1px solid #b0b0b0;
                    border-radius: 4px;
                    padding: 2px 6px;
                    font-size: 13px;
                    min-height: 28px;
                }
                QSpinBox:focus, QDoubleSpinBox:focus {
                    border: 1.5px solid #4a86e8;
                    background: #f0f6ff;
                }
            ''')
            row_layout.addWidget(widget)
            row_layout.addStretch(1)
            return row_widget
        
        if method == "KMeans":
            controls['n_clusters'] = QSpinBox()
            controls['n_clusters'].setRange(1, 20)
            controls['n_clusters'].setValue(3)
            params_layout.addRow("Число кластеров:", make_row(controls['n_clusters']))
            
            controls['max_iter'] = QSpinBox()
            controls['max_iter'].setRange(10, 1000)
            controls['max_iter'].setValue(300)
            params_layout.addRow("Максимум итераций:", make_row(controls['max_iter']))
            
            controls['tol'] = QDoubleSpinBox()
            controls['tol'].setDecimals(4)
            controls['tol'].setRange(0.0001, 1.0)
            controls['tol'].setSingleStep(0.0001)
            controls['tol'].setValue(0.0001)
            params_layout.addRow("Порог сходимости:", make_row(controls['tol']))
            
            controls['random_state'] = QSpinBox()
            controls['random_state'].setRange(0, 9999)
            controls['random_state'].setValue(0)
            params_layout.addRow("Случайное зерно:", make_row(controls['random_state']))
            
        elif method == "Birch":
            controls['n_clusters'] = QSpinBox()
            controls['n_clusters'].setRange(1, 20)
            controls['n_clusters'].setValue(3)
            params_layout.addRow("Число кластеров:", make_row(controls['n_clusters']))
            
            controls['threshold'] = QDoubleSpinBox()
            controls['threshold'].setRange(0.1, 10.0)
            controls['threshold'].setSingleStep(0.1)
            controls['threshold'].setValue(0.5)
            controls['threshold'].setDecimals(2)
            params_layout.addRow("Порог (threshold):", make_row(controls['threshold']))
            
            controls['branching_factor'] = QSpinBox()
            controls['branching_factor'].setRange(2, 100)
            controls['branching_factor'].setValue(50)
            params_layout.addRow("Фактор ветвления:", make_row(controls['branching_factor']))
            
        elif method == "OPTICS":
            controls['min_samples'] = QSpinBox()
            controls['min_samples'].setRange(1, 100)
            controls['min_samples'].setValue(5)
            params_layout.addRow("Минимальное число точек:", make_row(controls['min_samples']))
            
            controls['xi'] = QDoubleSpinBox()
            controls['xi'].setRange(0.01, 0.5)
            controls['xi'].setSingleStep(0.01)
            controls['xi'].setValue(0.05)
            controls['xi'].setDecimals(2)
            params_layout.addRow("Порог разбиения:", make_row(controls['xi']))
            
            controls['max_eps'] = QDoubleSpinBox()
            controls['max_eps'].setRange(0.1, 50.0)
            controls['max_eps'].setSingleStep(0.1)
            controls['max_eps'].setValue(10.0)
            controls['max_eps'].setDecimals(2)
            params_layout.addRow("Максимальное расстояние:", make_row(controls['max_eps']))
            
        elif method == "DBSCAN":
            controls['eps'] = QDoubleSpinBox()
            controls['eps'].setRange(0.1, 20.0)
            controls['eps'].setSingleStep(0.1)
            controls['eps'].setValue(2.0)
            controls['eps'].setDecimals(2)
            params_layout.addRow("Максимальное расстояние:", make_row(controls['eps']))
            
            controls['min_samples'] = QSpinBox()
            controls['min_samples'].setRange(1, 100)
            controls['min_samples'].setValue(5)
            params_layout.addRow("Минимальное число точек:", make_row(controls['min_samples']))
            
        return params_widget, controls

    def create_segmentator_params(self):
        """Создание виджета с параметрами для сегментации по HSV"""
        params_widget = QWidget()
        params_layout = QFormLayout(params_widget)
        params_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        params_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft)
        params_layout.setHorizontalSpacing(16)
        params_layout.setVerticalSpacing(8)
        controls = {}
        def make_row(widget):
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)
            widget.setMinimumWidth(80)
            widget.setMaximumWidth(120)
            widget.setMinimumHeight(28)
            widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            widget.setStyleSheet('''
                QSpinBox, QDoubleSpinBox {
                    background: white;
                    border: 1px solid #b0b0b0;
                    border-radius: 4px;
                    padding: 2px 6px;
                    font-size: 13px;
                    min-height: 28px;
                }
                QSpinBox:focus, QDoubleSpinBox:focus {
                    border: 1.5px solid #4a86e8;
                    background: #f0f6ff;
                }
            ''')
            row_layout.addWidget(widget)
            row_layout.addStretch(1)
            return row_widget
        controls['difference_channels'] = QSpinBox()
        controls['difference_channels'].setRange(1, 150)
        controls['difference_channels'].setValue(25)
        params_layout.addRow("Разница по каналам:", make_row(controls['difference_channels']))
        controls['difference_density'] = QSpinBox()
        controls['difference_density'].setRange(0, 100)
        controls['difference_density'].setValue(50)
        params_layout.addRow("Разница плотности (%):", make_row(controls['difference_density']))
        controls['radius'] = QSpinBox()
        controls['radius'].setRange(1, 100)
        controls['radius'].setValue(25)
        params_layout.addRow("Радиус:", make_row(controls['radius']))
        return params_widget, controls

    def run_clustering(self):
        """Запуск кластеризации выбранным методом"""
        if self.image_hsv is None:
            return

        try:
            # Получаем диапазоны из выбранной маски
            h_min, h_max = self.target_h_range
            s_min, s_max = self.target_s_range
            v_min, v_max = self.target_v_range
            
            # Создаем маску для выбранного диапазона
            mask = np.zeros(self.image_hsv.shape[:2], dtype=bool)
            for i in range(self.image_hsv.shape[0]):
                for j in range(self.image_hsv.shape[1]):
                    h, s, v = self.image_hsv[i, j]
                    if h_min <= h <= h_max and s_min <= s <= s_max and v_min <= v <= v_max:
                        mask[i, j] = True
            
            method = self.cluster_method.currentText()
            if method == "Сегментация по HSV":
                # Передаём исходное изображение
                self.clusters, self.counts_in_cluster = self.segmentator.segment(
                    self.image_hsv,
                    self.current_param_controls['difference_channels'].value(),
                    self.current_param_controls['difference_density'].value(),
                    self.current_param_controls['radius'].value()
                )
                # Фильтруем кластеры по маске
                mask_set = set(map(tuple, self.image_hsv[mask].reshape(-1, 3)))
                filtered_clusters = []
                filtered_counts = []
                for cluster in self.clusters:
                    filtered = [pt for pt in cluster if tuple(pt) in mask_set]
                    if filtered:
                        filtered_clusters.append(filtered)
                        filtered_counts.append(len(filtered))
                self.clusters = filtered_clusters
                self.counts_in_cluster = filtered_counts
                self.cluster_colors = self.segmentator.get_cluster_colors(mode='hsv')
            else:
                controls = self.current_param_controls
                masked_data = self.image_hsv[mask]
                if method == "KMeans":
                    kmeans = KMeans(
                        n_clusters=controls['n_clusters'].value(),
                        max_iter=controls['max_iter'].value(),
                        tol=controls['tol'].value(),
                        random_state=controls['random_state'].value()
                    )
                    labels = kmeans.fit_predict(masked_data)
                elif method == "Birch":
                    birch = Birch(
                        n_clusters=controls['n_clusters'].value(),
                        threshold=controls['threshold'].value(),
                        branching_factor=controls['branching_factor'].value()
                    )
                    labels = birch.fit_predict(masked_data)
                elif method == "OPTICS":
                    optics = OPTICS(
                        min_samples=controls['min_samples'].value(),
                        xi=controls['xi'].value(),
                        max_eps=controls['max_eps'].value()
                    )
                    labels = optics.fit_predict(masked_data)
                elif method == "DBSCAN":
                    dbscan = DBSCAN(
                        eps=controls['eps'].value(),
                        min_samples=controls['min_samples'].value()
                    )
                    labels = dbscan.fit_predict(masked_data)
                else:
                    labels = np.zeros(len(masked_data), dtype=int)
                
                self.clusters = []
                self.counts_in_cluster = []
                unique_labels = [l for l in np.unique(labels) if l != -1]
                for i in unique_labels:
                    cluster_points = masked_data[labels == i]
                    if len(cluster_points) > 0:
                        self.clusters.append(cluster_points.tolist())
                        self.counts_in_cluster.append(len(cluster_points))
                
                n = len(self.clusters)
                cmap = matplotlib.colormaps.get_cmap('tab20' if n <= 20 else 'hsv')
                base_colors = [cmap(i / max(1, n-1))[:3] for i in range(n)]
                self.cluster_colors = [list(color) for color in base_colors]
            
            self.update_cluster_info()
            self.update_segmentation_display()
            
        except Exception as e:
            print(f"Ошибка при выполнении кластеризации: {str(e)}")
            traceback.print_exc()

    def add_mask_to_table(self, mask):
        row = self.mask_table.rowCount()
        self.mask_table.insertRow(row)
        self.mask_table.setItem(row, 0, QTableWidgetItem(mask['name']))
        color_item = QTableWidgetItem()
        color_item.setBackground(mask['color'])
        color_item.setFlags(color_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.mask_table.setItem(row, 1, color_item)
        percent_item = QTableWidgetItem(f"{mask['percent']:.2f}")
        percent_item.setFlags(percent_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.mask_table.setItem(row, 2, percent_item)
        range_item = QTableWidgetItem(mask['ranges'])
        range_item.setFlags(range_item.flags() | Qt.ItemFlag.ItemIsEditable)
        self.mask_table.setItem(row, 3, range_item)

    def refresh_mask_table(self):
        self.mask_table.blockSignals(True)
        self.mask_table.setRowCount(0)
        for mask in self.masks:
            # Пересчёт процента для каждой маски
            percent = 0.0
            if self.image_hsv is not None:
                import re
                m = re.match(r"H\((\d+),(\d+)\)S\((\d+),(\d+)\)V\((\d+),(\d+)\)", mask['ranges'])
                if m:
                    h_min, h_max, s_min, s_max, v_min, v_max = map(int, m.groups())
                    mask_pixels = np.zeros(self.image_hsv.shape[:2], dtype=bool)
                    for i in range(self.image_hsv.shape[0]):
                        for j in range(self.image_hsv.shape[1]):
                            h, s, v = self.image_hsv[i, j]
                            if h_min <= h <= h_max and s_min <= s <= s_max and v_min <= v <= v_max:
                                mask_pixels[i, j] = True
                    percent = 100.0 * np.sum(mask_pixels) / (self.image_hsv.shape[0] * self.image_hsv.shape[1])
            mask['percent'] = percent
            self.add_mask_to_table(mask)
        self.mask_table.blockSignals(False)

    def create_mask(self):
        from PyQt6.QtGui import QColor
        name = f"Маска {len(self.masks)+1}"
        color = QColorDialog.getColor()
        if not color.isValid():
            return
        # Диапазон по умолчанию
        ranges = 'H(0,180)S(0,255)V(0,255)'
        percent = 0.0
        if self.image_hsv is not None:
            import re
            m = re.match(r"H\((\d+),(\d+)\)S\((\d+),(\d+)\)V\((\d+),(\d+)\)", ranges)
            if m:
                h_min, h_max, s_min, s_max, v_min, v_max = map(int, m.groups())
                mask_pixels = np.zeros(self.image_hsv.shape[:2], dtype=bool)
                for i in range(self.image_hsv.shape[0]):
                    for j in range(self.image_hsv.shape[1]):
                        h, s, v = self.image_hsv[i, j]
                        if h_min <= h <= h_max and s_min <= s <= s_max and v_min <= v <= v_max:
                            mask_pixels[i, j] = True
                percent = 100.0 * np.sum(mask_pixels) / (self.image_hsv.shape[0] * self.image_hsv.shape[1])
        mask = {'name': name, 'color': color, 'percent': percent, 'ranges': ranges}
        self.masks.append(mask)
        self.refresh_mask_table()

    def delete_selected_masks(self):
        selected = set(idx.row() for idx in self.mask_table.selectedIndexes())
        self.masks = [m for i, m in enumerate(self.masks) if i not in selected]
        self.refresh_mask_table()

    def delete_all_masks(self):
        self.masks.clear()
        self.refresh_mask_table()

    def update_selected_masks(self):
        # Здесь можно применить алгоритм к выбранным маскам
        pass

    def on_mask_table_item_changed(self, item):
        # Только если редактируется столбец 'Диапазоны'
        if item.column() == 3:
            row = item.row()
            new_ranges = item.text()
            self.masks[row]['ranges'] = new_ranges
            
            # Обновляем диапазоны HSV для диаграммы
            import re
            m = re.match(r"H\((\d+),(\d+)\)S\((\d+),(\d+)\)V\((\d+),(\d+)\)", new_ranges)
            if m:
                h_min, h_max, s_min, s_max, v_min, v_max = map(int, m.groups())
                self.target_h_range = (h_min, h_max)
                self.target_s_range = (s_min, s_max)
                self.target_v_range = (v_min, v_max)
                
                # Если окно диаграммы открыто, обновляем его
                if hasattr(self, 'diagram_window') and self.diagram_window.isVisible():
                    self.show_target_diagram()
            
            # Пересчитать процент
            percent = 0.0
            if self.image_hsv is not None:
                mask_pixels = np.zeros(self.image_hsv.shape[:2], dtype=bool)
                for i in range(self.image_hsv.shape[0]):
                    for j in range(self.image_hsv.shape[1]):
                        h, s, v = self.image_hsv[i, j]
                        if h_min <= h <= h_max and s_min <= s <= s_max and v_min <= v <= v_max:
                            mask_pixels[i, j] = True
                percent = 100.0 * np.sum(mask_pixels) / (self.image_hsv.shape[0] * self.image_hsv.shape[1])
            self.masks[row]['percent'] = percent
            self.mask_table.blockSignals(True)
            self.mask_table.setItem(row, 2, QTableWidgetItem(f"{percent:.2f}"))
            self.mask_table.blockSignals(False)

    def show_target_diagram(self):
        """Отображение диаграммы цель/промах"""
        if not hasattr(self, 'clusters') or not self.clusters:
            return

        try:
            # Получаем диапазоны из выбранной маски, если она есть
            selected = self.mask_table.selectedItems()
            if selected:
                # Берём первую выбранную маску
                row = selected[0].row()
                mask = self.masks[row]
                # Ожидается формат 'H(0,180)S(0,255)V(0,255)'
                import re
                m = re.match(r"H\((\d+),(\d+)\)S\((\d+),(\d+)\)V\((\d+),(\d+)\)", mask['ranges'])
                if m:
                    h_min, h_max, s_min, s_max, v_min, v_max = map(int, m.groups())
                    self.target_h_range = (h_min, h_max)
                    self.target_s_range = (s_min, s_max)
                    self.target_v_range = (v_min, v_max)

            # Создаем новое окно для диаграммы, если его еще нет
            if not hasattr(self, 'diagram_window') or not self.diagram_window.isVisible():
                self.diagram_window = QWidget()
                self.diagram_window.setWindowTitle("Диаграмма цель/промах")
                self.diagram_window.setGeometry(200, 200, 800, 600)
                
                # Создаем layout для окна
                layout = QVBoxLayout(self.diagram_window)
                
                # Создаем новую фигуру matplotlib
                self.diagram_fig = plt.figure(figsize=(8, 6))
                self.diagram_canvas = FigureCanvas(self.diagram_fig)
                self.diagram_toolbar = NavigationToolbar(self.diagram_canvas, self.diagram_window)
                
                # Добавляем виджеты в layout
                layout.addWidget(self.diagram_toolbar)
                layout.addWidget(self.diagram_canvas)

            # Определяем целевые кластеры (те, которые содержат больше всего точек)
            cluster_sizes = [len(cluster) for cluster in self.clusters]
            target_clusters = set(np.argsort(cluster_sizes)[-3:])  # Берем 3 самых больших кластера

            # Подсчет категорий
            target_in_target = 0
            target_in_non_target = 0
            non_target_in_target = 0
            non_target_in_non_target = 0

            # Проходим по всем кластерам и точкам
            for i, cluster in enumerate(self.clusters):
                for point in cluster:
                    h, s, v = point
                    in_target = (
                        self.target_h_range[0] <= h <= self.target_h_range[1] and
                        self.target_s_range[0] <= s <= self.target_s_range[1] and
                        self.target_v_range[0] <= v <= self.target_v_range[1]
                    )
                    is_target_cluster = i in target_clusters

                    if in_target and is_target_cluster:
                        target_in_target += 1
                    elif in_target and not is_target_cluster:
                        target_in_non_target += 1
                    elif not in_target and is_target_cluster:
                        non_target_in_target += 1
                    else:
                        non_target_in_non_target += 1

            # Очищаем фигуру
            self.diagram_fig.clear()
            ax = self.diagram_fig.add_subplot(111)

            # Категории и их значения
            categories = [
                'Цель=цель кл',
                'Цель=не цель кл',
                'Не цель=цель класт',
                'не цель=не цель класт'
            ]
            counts = [
                target_in_target,
                target_in_non_target,
                non_target_in_target,
                non_target_in_non_target
            ]

            # Общая статистика
            total_points = sum(counts)
            correct_classification = target_in_target + non_target_in_non_target
            correct_percentage = (correct_classification / total_points) * 100

            # Создаем столбчатую диаграмму
            bars = ax.bar(categories, counts, color=['green', 'lightgreen', 'red', 'pink'])
            ax.set_title('Распределение точек по категориям')
            ax.set_ylabel('Количество точек')

            # Добавляем аннотацию с общей статистикой
            stats_text = (f"Точно классифицировано: {correct_classification} ({correct_percentage:.1f}%)\n"
                         f"Цель=Цель: {target_in_target} | Промах=Промах: {non_target_in_non_target}\n"
                         f"Ошибки: {target_in_non_target + non_target_in_target}")

            ax.annotate(stats_text, xy=(0.5, 0.95), xycoords='axes fraction',
                       ha='center', va='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

            # Добавляем значения на столбцы
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height}',
                           xy=(bar.get_x() + bar.get_width() / 2, height),
                           xytext=(0, 3),
                           textcoords="offset points",
                           ha='center', va='bottom')

            plt.tight_layout()
            self.diagram_canvas.draw()

            # Показываем окно
            self.diagram_window.show()

        except Exception as e:
            print(f"Ошибка при создании диаграммы: {str(e)}")
            traceback.print_exc()

    def on_apply_filter_clicked(self):
        """Обработчик кнопки 'Применить фильтрацию'"""
        self.apply_filtering()
        self.update_plot()

    def on_tab_changed(self, idx):
        # 0 — просмотрщик, 1 — кластеризация
        if idx == 0:
            self.filter_group.show()
        else:
            self.filter_group.hide()

if __name__ == '__main__':
    try:
        # Настройка логирования
        import logging
        logging.basicConfig(
            filename='app.log',
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Инициализация приложения
        app = QApplication(sys.argv)
        logging.info("Приложение инициализировано")
        
        # Создание и отображение главного окна
        viewer = ClusterViewer()
        logging.info("Главное окно создано")
        
        viewer.show()
        logging.info("Главное окно отображено")
        
        # Запуск главного цикла
        exit_code = app.exec()
        logging.info(f"Приложение завершено с кодом: {exit_code}")
        sys.exit(exit_code)
        
    except Exception as e:
        error_msg = f"Критическая ошибка: {str(e)}\n{traceback.format_exc()}"
        logging.error(error_msg)
        print(error_msg)
        
        # Сохранение лога ошибок
        with open('error_log.txt', 'w', encoding='utf-8') as f:
            f.write(error_msg)
        
        # Показ сообщения об ошибке пользователю
        from PyQt6.QtWidgets import QMessageBox
        if QApplication.instance():
            QMessageBox.critical(None, "Ошибка", 
                               "Произошла критическая ошибка. Подробности в error_log.txt")
        sys.exit(1) 