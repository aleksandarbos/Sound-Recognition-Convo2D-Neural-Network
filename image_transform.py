
import numpy as np

from PIL import Image

"""
    @brief Klasa za transofmacije nad slikom...
    U sardanji sa OpenCV...
    Priprema slika za Neural Network learning...
"""
class ImageTransform:

    def __init__(self, mat_figure):  # constructor
        self.img = self.fig2img(mat_figure)                     # private attr img

        """ matlab plot to image data object """
    def fig2data (self, fig ):
        """
        @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
        @param fig a matplotlib figure
        @return a numpy 3D array of RGBA values
        """
        # draw the renderer
        fig.canvas.draw ( )

        # Get the RGBA buffer from the figure
        w,h = fig.canvas.get_width_height()
        buf = np.fromstring ( fig.canvas.tostring_argb(), dtype=np.uint8 )
        buf.shape = ( w, h,4 )

        # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
        buf = np.roll ( buf, 3, axis = 2 )
        return buf

    def fig2img (self, fig ):                        # gives image from specific matplotlib plot figure
        """
        @brief Convert a Matplotlib figure to a PIL Image in RGBA format and return it
        @param fig a matplotlib figure
        @return a Python Imaging Library ( PIL ) image
        """
        # put the figure pixmap into a numpy array
        buf = self.fig2data ( fig )
        w, h, d = buf.shape
        return Image.frombytes( "RGBA", ( w ,h ), buf.tostring( ) )

    def transform(self):
        "TODO: image transforming..."

    def show_image(self):
        self.img.show()
