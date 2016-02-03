
import numpy as np
import matplotlib.pylab as pylab
import cv2
import matplotlib.pyplot as plt

from PIL import Image

"""
    @brief Klasa za transofmacije nad slikom...
    U sardanji sa OpenCV...
    Priprema slika za Neural Network learning...
"""
class ImageTransform:

    def __init__(self, mat_figure):  # constructor
        self.img = self.fig2data(mat_figure)                     # private attr img

    @staticmethod
    def load_image(path):
        return cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)
    @staticmethod
    def image_gray(image):
        return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    @staticmethod
    def image_bin(image_gs):
        height, width = image_gs.shape[0:2]
        image_binary = np.ndarray((height, width), dtype=np.uint8)
        ret,image_bin = cv2.threshold(image_gs, 100, 255, cv2.THRESH_BINARY)
        return image_bin

    @staticmethod
    def invert(image):
        return 255-image

    @staticmethod
    def display_image(image, color= False):
        if color:
            plt.imshow(image)
        else:
            plt.imshow(image, 'gray')
    @staticmethod
    def dilate(image):
        kernel = np.ones((3,3)) # strukturni element 3x3 blok
        return cv2.dilate(image, kernel, iterations=1)
    @staticmethod
    def erode(image):
        kernel = np.ones((3,3)) # strukturni element 3x3 blok
        return cv2.erode(image, kernel, iterations=1)

        """ matlab plot to image data object """
    @staticmethod
    def fig2data (fig ):
        # draw the renderer
        fig.canvas.draw ( )

        data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        return data

    @staticmethod
    def crop_image(img, x1, x2, y1, y2):
        #self.img = self.img[40:305, 80:470]
        img = img[y1:y2, x1:x2]
        return img

    @staticmethod
    def transform(img):
        img = ImageTransform.crop_image(img, 80,470, 40,305)
        img = ImageTransform.image_gray(img)
        return img

    @staticmethod
    def show_image(self):
        self.img.show()
