import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
from omegaconf import OmegaConf, MISSING
from mpl_toolkits.mplot3d import Axes3D

# #Загрузка изображения (Апатит)
# image1 = cv2.imread('Test2.jpg')
# # Конвертация изображения в HSV
# hsv_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)

# # Загрузка второго изображения (для тестов)
# image2 = cv2.imread('Originalv2.jpg')
# # Конвертация второго изображения в HSV
# hsv_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2HSV)

# #Маска
def nothing(x): pass

# Load in image
image = cv2.imread('Test1.jpg')

# Create a window
cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('HMin','image',0,179,nothing) # Hue is from 0-179 for Opencv
cv2.createTrackbar('SMin','image',0,255,nothing)
cv2.createTrackbar('VMin','image',0,255,nothing)
cv2.createTrackbar('HMax','image',0,179,nothing)
cv2.createTrackbar('SMax','image',0,255,nothing)
cv2.createTrackbar('VMax','image',0,255,nothing)

# Set default value for MAX HSV trackbars.
cv2.setTrackbarPos('HMax', 'image', 179)
cv2.setTrackbarPos('SMax', 'image', 255)
cv2.setTrackbarPos('VMax', 'image', 255)

# Initialize to check if HSV min/max value changes
hMin = sMin = vMin = hMax = sMax = vMax = 0
phMin = psMin = pvMin = phMax = psMax = pvMax = 0

output = image
wait_time = 33

while(1):
    # get current positions of all trackbars
    hMin = cv2.getTrackbarPos('HMin','image')
    sMin = cv2.getTrackbarPos('SMin','image')
    vMin = cv2.getTrackbarPos('VMin','image')

    hMax = cv2.getTrackbarPos('HMax','image')
    sMax = cv2.getTrackbarPos('SMax','image')
    vMax = cv2.getTrackbarPos('VMax','image')

    # Set minimum and max HSV values to display
    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])

    # lower = np.array([140, 165, 136])
    # upper = np.array([153, 230, 180])

    # Create HSV Image and threshold into a range.
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(image,image, mask= mask)

# Print if there is a change in HSV value
    if( (phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax) ):
        print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (hMin , sMin , vMin, hMax, sMax , vMax))
    phMin = hMin
    psMin = sMin
    pvMin = vMin
    phMax = hMax
    psMax = sMax
    pvMax = vMax

    # Display output image
    cv2.imshow('image',output)

    # Wait longer to prevent freeze for videos.
    if cv2.waitKey(wait_time) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

#Ещё тест
#lower_bound = np.array([318, 55, 26])
#upper_bound = np.array([357, 86, 95])
# #
# #Это даже работает
# lower_bound = np.array([140, 165, 136])
# upper_bound = np.array([153, 230, 180])
#
# # Создание маски к изображениям
# mask_img1 = cv2.inRange(hsv_image1, lower_bound, upper_bound)
#
# # mask_img2 = cv2.inRange(hsv_image2, lower_bound, upper_bound)
#
# # Применение маски к изображениям
# masked_image1 = cv2.bitwise_and(image1, image1, mask=mask_img1)
#
# # masked_image2 = cv2.bitwise_and(image2, image2, mask=mask_img2)
#
# #----- Отображение маски и итогового изображения -----
# plt.figure(figsize=(40, 20))
#
# plt.subplot(1, 1, 1)
# plt.imshow(cv2.cvtColor(hsv_image1, cv2.COLOR_BGR2RGB))
# plt.title('HSV Image')
# plt.axis('off')
# #
# # plt.subplot(1, 2, 2)
# # plt.imshow(cv2.cvtColor(hsv_image1, cv2.COLOR_BGR2RGB))
# # plt.title('HSV Image 2')
# # plt.axis('off')
#
# # plt.subplot(1, 2, 1)
# # plt.imshow(mask_img1, cmap='gray')
# # plt.title('Mask Image 1')
# # plt.axis('off')
# #
# # plt.subplot(1, 2, 2)
# # plt.imshow(cv2.cvtColor(masked_image1, cv2.COLOR_BGR2RGB))
# # plt.title('Masked Image 1')
# # plt.axis('off')
#
# # plt.subplot(10, 4, 3)
# # plt.imshow(mask_img2, cmap='gray')
# # plt.title('Mask Image 2')
# # plt.axis('off')
# #
# # plt.subplot(10, 4, 4)
# # plt.imshow(cv2.cvtColor(masked_image2, cv2.COLOR_BGR2RGB))
# # plt.title('Masked Image 2')
# # plt.axis('off')
#
# plt.show()

# # # ----- Гистограмма 2-ухмерная -----
#
# # image3 = cv2.imread('Original33.png')
# # hsv_image3 = cv2.cvtColor(image3, cv2.COLOR_BGR2HSV)
# # H, S, V = image3[:,:,0], image3[:,:,1], image3[:,:,2]
# # plt.figure(figsize=(10,8))
# # plt.subplot(311)  # график в первой ячейке
# # plt.subplots_adjust(hspace=.5)
# # plt.title("Hue")
# # plt.hist(np.ndarray.flatten(H), bins=180)
# # plt.subplot(312)  # график во второй ячейке
# # plt.title("Saturation")
# # plt.hist(np.ndarray.flatten(S), bins=128)
# # plt.subplot(313)
# # plt.title("Value")
# # plt.hist(np.ndarray.flatten(V), bins=128)
# #
# # plt.show()
#
#
# # ----- Гистограмма 3-ехмерная (не используется) ------
# #
# # def hist3d_hsv(rgb_img, bins=20, scale_dots=1.0, figsize=(10, 5), range=((0, 255), (0, 255), (0, 255)), bg_color=(0, 0.2, 0)):
# #     h, w, ch = rgb_img.shape
# #     assert ch == 3, "Only 3-channel images allowed!"
# #     hsv_img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2HSV)
# #     hist, edges = np.histogramdd(hsv_img.reshape(h * w, ch), range=range, bins=bins)
#
#
#
# #____Показ по каждому каналу____
#
# # plt.figure(figsize=(15, 5))
# # plt.subplot(1, 3, 1)
# # plt.imshow(hsv_image[:, :, 0], cmap='gray')
# # plt.title('Hue Channel')
# # plt.axis('off')
# #
# # plt.subplot(1, 3, 2)
# # plt.imshow(hsv_image[:, :, 1], cmap='gray')
# # plt.title('Saturation Channel')
# # plt.axis('off')
# #
# # plt.subplot(1, 3, 3)
# # plt.imshow(hsv_image[:, :, 2], cmap='gray')
# # plt.title('Value Channel')
# # plt.axis('off')
# #
# # plt.show()

#Среднее значение каналов HSV изображения
# mean_hue = np.mean(hsv_image2[:, :, 0])
# mean_saturation = np.mean(hsv_image2[:, :, 1])
# mean_value = np.mean(hsv_image2[:, :, 2])
#
# print(f"Среднее значение Hue: {mean_hue}")
# print(f"Среднее значение Saturation: {mean_saturation}")
# print(f"Среднее значение Value: {mean_value}")

# ----- График от Димы ------

# image_path = "HSV Test2.png"
#
# def plot_hsv_points(image_path):
#     import cv2
#     import matplotlib.pyplot as plt
#     from mpl_toolkits.mplot3d import Axes3D
#     import numpy as np
#
#     img = cv2.imread(image_path)
#     if img is None:
#         raise ValueError(f"Не удалось загрузить изображение по пути: {image_path}")
#
#     # Преобразуем изображение в HSV
#     hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#
#     # Извлекаем каналы H, S и V
#     h_channel = hsv_img[:, :, 0].flatten() # Hue
#     s_channel = hsv_img[:, :, 1].flatten() # Saturation
#     v_channel = hsv_img[:, :, 2].flatten() # Value
#
#     hMin = 125
#     hMax = 170
#     sMin = 165
#     sMax = 230
#     vMin = 136
#     vMax = 180
#
#     # Фильтруем по заданным диапазонам HSV
#     mask = (
#     (h_channel >= hMin) & (h_channel <= hMax) &
#     (s_channel >= sMin) & (s_channel <= sMax) &
#     (v_channel >= vMin) & (v_channel <= vMax)
#     )
#
#     # Применяем маску для фильтрации значений
#     h_filtered = h_channel[mask]
#     s_filtered = s_channel[mask]
#     v_filtered = v_channel[mask]
#
#     # Создаем 3D график
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')
#
#     # Создаем точечный график
#     ax.scatter(h_filtered, s_filtered, v_filtered, c='b', marker='o', alpha=0.5)
#
#     ax.set_xlabel('Hue')
#     ax.set_ylabel('Saturation')
#     ax.set_zlabel('Value')
#     plt.title('3D Scatter Plot in HSV Space (Filtered)')
#     plt.show()
#
# # Путь к изображению
# image_path = "HSV Test2.png"
#
# # Создаем 3D график
# plot_hsv_points(image_path)



# # ##############################################################################
# # # HISTOGRAM FUNCTION
# # ##############################################################################
# #Облако точек с проекцией
# """
# def hist3d_hsv(rgb_img, bins=20, scale_dots=1.0, figsize=(12, 6), range=((0, 255), (0, 255), (0, 255)),
#                bg_color=(0, 0.2, 0)):
#
#     #rgb_img must be in range 0, 255!
#     #HSV will be in range 0..179, 0..255, 0..255
#
#     h, w, ch = rgb_img.shape
#     assert ch == 3, "Only 3-channel images allowed!"
#
#     # Convert image to HSV
#     image1 = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2HSV)
#
#     # Calculate histogram
#     hist, edges = np.histogramdd(image1.reshape(h * w, ch), range=range, bins=bins)
#
#     # Get non-zero histogram indices
#     hidxs = hist.nonzero()
#     n_hidxs = hidxs[0].shape[0]
#
#     # Initialize size and color arrays
#     sizevals = np.zeros(n_hidxs, dtype=np.float64)
#     hsv_vals = np.zeros((n_hidxs, ch), dtype=np.float64)
#
#     for i, hid in enumerate(zip(*hidxs)):
#         sizevals[i] = hist[hid]
#         hsv_vals[i] = [edg[j] for j, edg in zip(hid, edges)]
#
#     # Normalize sizes
#     try:
#         sizevals /= sizevals.max()
#     except ZeroDivisionError:
#         raise RuntimeError("This should never happen")
#
#     # Convert HSV to RGB for coloring
#     rgb_vals = hsv_vals.copy()
#     rgb_vals[:, 0] /= 179
#     rgb_vals[:, 1] /= 255
#     rgb_vals[:, 2] /= 255
#     rgb_vals = hsv_to_rgb(rgb_vals)
#
#     # Adjust dot size for better visualization
#     sizevals *= (scale_dots * 100)
#
#     # Create figure and 3D axis
#     fig = plt.figure(figsize=figsize)
#     ax_im = fig.add_subplot(1, 2, 1)
#     ax_hist = fig.add_subplot(1, 2, 2, projection='3d')
#
#     # Display original image
#     ax_im.imshow(rgb_img)
#
#     # Plot histogram as 3D scatter plot
#     scatter = ax_hist.scatter(hsv_vals[:, 0], hsv_vals[:, 1], hsv_vals[:, 2], c=rgb_vals, s=sizevals, alpha=0.8,
#                               edgecolor='k')
#
#     # Plot projections on each axis plane
#     ax_hist.scatter(hsv_vals[:, 0], hsv_vals[:, 1], np.zeros_like(hsv_vals[:, 2]), c='red', alpha=0.3, s=5,
#                     label='Hue-Saturation plane')
#     ax_hist.scatter(hsv_vals[:, 0], np.zeros_like(hsv_vals[:, 1]), hsv_vals[:, 2], c='green', alpha=0.3, s=5,
#                     label='Hue-Value plane')
#     ax_hist.scatter(np.zeros_like(hsv_vals[:, 0]), hsv_vals[:, 1], hsv_vals[:, 2], c='blue', alpha=0.3, s=5,
#                     label='Saturation-Value plane')
#
#     # Set labels, legend, and background color
#     ax_hist.set_xlabel("Hue", color='red')
#     ax_hist.set_ylabel("Saturation", color='green')
#     ax_hist.set_zlabel("Value", color='blue')
#     ax_hist.set_facecolor(bg_color)
#     ax_hist.legend()
#
#     fig.tight_layout()
#     return fig
# """
#
# #Облако точек без проекции
# def hist3d_hsv(rgb_img, bins=20, scale_dots=1.0, figsize=(12, 6), range=((0, 255), (0, 255), (0, 255)),
#                bg_color=(0, 0.2, 0)):
#     """
#     rgb_img must be in range 0, 255!
#     HSV will be in range 0..179, 0..255, 0..255
#     """
#     h, w, ch = rgb_img.shape
#     assert ch == 3, "Only 3-channel images allowed!"
#
#     # Convert image to HSV
#     image1 = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2HSV)
#
#     # Calculate histogram
#     hist, edges = np.histogramdd(image1.reshape(h * w, ch), range=range, bins=bins)
#
#     # Get non-zero histogram indices
#     hidxs = hist.nonzero()
#     n_hidxs = hidxs[0].shape[0]
#
#     # Initialize size and color arrays
#     sizevals = np.zeros(n_hidxs, dtype=np.float64)
#     hsv_vals = np.zeros((n_hidxs, ch), dtype=np.float64)
#
#     for i, hid in enumerate(zip(*hidxs)):
#         sizevals[i] = hist[hid]
#         hsv_vals[i] = [edg[j] for j, edg in zip(hid, edges)]
#
#     # Normalize sizes
#     try:
#         sizevals /= sizevals.max()
#     except ZeroDivisionError:
#         raise RuntimeError("This should never happen")
#
#     # Convert HSV to RGB for coloring
#     rgb_vals = hsv_vals.copy()
#     rgb_vals[:, 0] /= 179
#     rgb_vals[:, 1] /= 255
#     rgb_vals[:, 2] /= 255
#     rgb_vals = hsv_to_rgb(rgb_vals)
#
#     # Adjust dot size for better visualization
#     sizevals *= (scale_dots * 100)
#
#     # Create figure and 3D axis
#     fig = plt.figure(figsize=figsize)
#     ax_im = fig.add_subplot(1, 2, 1)
#     ax_hist = fig.add_subplot(1, 2, 2, projection='3d')
#
#     # Display original image
#     ax_im.imshow(rgb_img)
#
#     # Plot histogram as 3D scatter plot with different colors for each axis
#     ax_hist.scatter(hsv_vals[:, 0], hsv_vals[:, 1], hsv_vals[:, 2], c=rgb_vals, s=sizevals, alpha=0.8, edgecolor='k')
#
#     # Set labels and background color
#     ax_hist.set_xlabel("Hue", color='red')
#     ax_hist.set_ylabel("Saturation", color='green')
#     ax_hist.set_zlabel("Value", color='blue')
#     ax_hist.set_facecolor(bg_color)
#
#     fig.tight_layout()
#     return fig
#
# # ----- Гистограмма с линиями 3-ехмерная -----
# """
# def hist3d_hsv(rgb_img, bins=20, scale_dots=1.0, figsize=(10, 5), range=((0, 255), (0, 255), (0, 255)),
#                bg_color=(0, 0.2, 0)):
#
#     #rgb_img must be in range 0, 255!
#     #HSV will be in range 0..179, 0..255, 0..255
#
#     h, w, ch = rgb_img.shape
#     assert ch == 3, "Only 3-channel images allowed!"
#
#     # Convert image to HSV
#     image1 = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2HSV)
#
#     # Calculate histogram
#     hist, edges = np.histogramdd(image1.reshape(h * w, ch), range=range, bins=bins)
#
#     # Get non-zero histogram indices
#     hidxs = hist.nonzero()
#     n_hidxs = hidxs[0].shape[0]
#
#     # Initialize size and color arrays
#     sizevals = np.zeros(n_hidxs, dtype=np.float64)
#     hsv_vals = np.zeros((n_hidxs, ch), dtype=np.float64)
#
#     for i, hid in enumerate(zip(*hidxs)):
#         sizevals[i] = hist[hid]
#         hsv_vals[i] = [edg[j] for j, edg in zip(hid, edges)]
#
#     # Normalize sizes
#     try:
#         sizevals /= sizevals.max()
#     except ZeroDivisionError:
#         raise RuntimeError("This should never happen")
#
#     # Convert HSV to RGB for coloring
#     rgb_vals = hsv_vals.copy()
#     rgb_vals[:, 0] /= 179
#     rgb_vals[:, 1] /= 255
#     rgb_vals[:, 2] /= 255
#     rgb_vals = hsv_to_rgb(rgb_vals)
#
#     # Create figure and 3D axis
#     fig = plt.figure(figsize=figsize)
#     ax_im = fig.add_subplot(1, 2, 1)
#     ax_hist = fig.add_subplot(1, 2, 2, projection='3d')
#
#     # Display original image
#     ax_im.imshow(rgb_img)
#
#     # Plot histogram as 3D bars
#     width = depth = (255 / bins)
#     ax_hist.bar3d(hsv_vals[:, 0], hsv_vals[:, 1], np.zeros(n_hidxs), width, depth, sizevals, color=rgb_vals, shade=True)
#
#     # Set labels and background color
#     ax_hist.set_xlabel("Hue")
#     ax_hist.set_ylabel("Saturation")
#     ax_hist.set_zlabel("Value")
#     ax_hist.set_facecolor(bg_color)
#
#     fig.tight_layout()
#     return fig
# """
# # ----- Ещё гистограмма с цветными линиями для большей наглядности -----
#
# """
# def hist3d_hsv(rgb_img, bins=20, scale_dots=1.0, figsize=(10, 5), range=((0, 255), (0, 255), (0, 255)),
#                bg_color=(0, 0.2, 0)):
#
#     #rgb_img must be in range 0, 255!
#     #HSV will be in range 0..179, 0..255, 0..255
#
#     h, w, ch = rgb_img.shape
#     assert ch == 3, "Only 3-channel images allowed!"
#
#     # Convert image to HSV
#     image1 = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2HSV)
#
#     # Calculate histogram
#     hist, edges = np.histogramdd(image1.reshape(h * w, ch), range=range, bins=bins)
#
#     # Get non-zero histogram indices
#     hidxs = hist.nonzero()
#     n_hidxs = hidxs[0].shape[0]
#
#     # Initialize size and color arrays
#     sizevals = np.zeros(n_hidxs, dtype=np.float64)
#     hsv_vals = np.zeros((n_hidxs, ch), dtype=np.float64)
#
#     for i, hid in enumerate(zip(*hidxs)):
#         sizevals[i] = hist[hid]
#         hsv_vals[i] = [edg[j] for j, edg in zip(hid, edges)]
#
#     # Normalize sizes
#     try:
#         sizevals /= sizevals.max()
#     except ZeroDivisionError:
#         raise RuntimeError("This should never happen")
#
#     # Convert HSV to RGB for coloring with adjusted brightness
#     rgb_vals = hsv_vals.copy()
#     rgb_vals[:, 0] /= 179
#     rgb_vals[:, 1] /= 255
#     rgb_vals[:, 2] /= 255
#     rgb_vals = hsv_to_rgb(rgb_vals)
#
#     # Normalize HSV values for better color scaling
#     rgb_vals[:, 1] = np.clip(rgb_vals[:, 1] * 1.5, 0, 1)  # Increase saturation
#     rgb_vals[:, 2] = np.clip(rgb_vals[:, 2] * 1.5, 0, 1)  # Increase brightness
#
#     # Apply unique color adjustments to make plots more expressive
#     rgb_vals_hue = np.copy(rgb_vals)
#     rgb_vals_hue[:, 1:] *= 1  # Dim saturation and value to highlight hue
#
#     rgb_vals_saturation = np.copy(rgb_vals)
#     rgb_vals_saturation[:, [0, 2]] *= 1  # Dim hue and value to highlight saturation
#
#     rgb_vals_value = np.copy(rgb_vals)
#     rgb_vals_value[:, :2] *= 1  # Dim hue and saturation to highlight value
#
#     # Create figure and 3D axis
#     fig = plt.figure(figsize=figsize)
#     ax_im = fig.add_subplot(1, 2, 1)
#     ax_hist = fig.add_subplot(1, 2, 2, projection='3d')
#
#     # Display original image
#     ax_im.imshow(rgb_img)
#
#     # Plot histogram as 3D bars with color highlighting
#     width = depth = (255 / bins)
#     alpha_value = 0.95
#     ax_hist.bar3d(hsv_vals[:, 0], hsv_vals[:, 1], np.zeros(n_hidxs), width, depth, sizevals, color=rgb_vals_hue,
#                   alpha=alpha_value, shade=False, label='Hue')
#     ax_hist.bar3d(hsv_vals[:, 0], hsv_vals[:, 1], np.zeros(n_hidxs), width, depth, sizevals, color=rgb_vals_saturation,
#                   alpha=alpha_value, shade=False, label='Saturation')
#     ax_hist.bar3d(hsv_vals[:, 0], hsv_vals[:, 1], np.zeros(n_hidxs), width, depth, sizevals, color=rgb_vals_value,
#                   alpha=alpha_value, shade=False, label='Value')
#
#     # Set labels and background color
#     ax_hist.set_xlabel("Hue")
#     ax_hist.set_ylabel("Saturation")
#     ax_hist.set_zlabel("Value")
#     ax_hist.set_facecolor(bg_color)
#
#     # Add legend to differentiate bars
#     ax_hist.legend()
#
#     fig.tight_layout()
#     return fig
# """
#
# # ##############################################################################
# # # GLOBALS
# # ##############################################################################
# CONF = OmegaConf.create()
# CONF.IMG_PATH = 'Original.png'
# CONF.BINS = 20
# CONF.SCALE_DOTS = 7.0
# CONF.DPI = 200
# CONF.SUFFIX_OUT = "_plot.png"
# CONF.FIGSIZE = (11, 5)  # h, w
# CONF.BG_RGB = (0.8, 1, 0.8)
# CONF.PLOT = False
# #
# cli_conf = OmegaConf.from_cli()
# CONF = OmegaConf.merge(CONF, cli_conf)
# print(OmegaConf.to_yaml(CONF))
#
#
# # ##############################################################################
# # # MAIN ROUTINE
# # ##############################################################################
# img_rgb = cv2.cvtColor(cv2.imread(CONF.IMG_PATH), cv2.COLOR_BGR2RGB)
# fig = hist3d_hsv(img_rgb,
#                  bins=CONF.BINS,
#                  scale_dots=CONF.SCALE_DOTS,
#                  figsize=CONF.FIGSIZE,
#                  bg_color=CONF.BG_RGB)
#
# if CONF.PLOT:
#     fig.show()
#     breakpoint()
# else:
#     out_path = os.path.splitext(CONF.IMG_PATH)[0] + CONF.SUFFIX_OUT
#     fig.savefig(out_path, dpi=CONF.DPI)