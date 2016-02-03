
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
        """
        @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
        @param fig a matplotlib figure
        @return a numpy 3D array of RGBA values
        """

        """ neispravno ... """

        # draw the renderer
        fig.canvas.draw ( )

        # Get the RGBA buffer from the figure
        w,h = fig.canvas.get_width_height()
        buf = np.fromstring ( fig.canvas.tostring_argb(), dtype=np.uint8 )
        buf.shape = ( w, h, 4 )

        # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
        buf = np.roll ( buf, 3, axis = 2 )
        return buf

    def transform(self):
        "TODO: image transforming..."

    def show_image(self):
        self.img.show()
