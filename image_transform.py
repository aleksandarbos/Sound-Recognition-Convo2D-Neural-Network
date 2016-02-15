
import numpy as np
import matplotlib.pylab as pylab
import cv2
import matplotlib.pyplot as plt
import os

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
        ret,image_bin = cv2.threshold(image_gs, 110, 255, cv2.THRESH_BINARY)
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
        img = img[y1:y2, x1:x2]
        return img

    @staticmethod
    def transform(img):
        img = ImageTransform.crop_image(img, 125,475, 140,305)#posmatra se opseg od 0 - 5000 Hz
        img = ImageTransform.image_gray(img)
        return img

    @staticmethod
    def resize_graph(graph, x_dim = 70, y_dim = 33):
        resized_graph = cv2.resize(graph,(x_dim, y_dim), interpolation = cv2.INTER_NEAREST)
        return resized_graph

    @staticmethod
    def show_image(self):
        self.img.show()

    @staticmethod
    def dilate(image):
        kernel = np.ones((3,3)) # strukturni element 3x3 blok
        return cv2.dilate(image, kernel, iterations=1)

    @staticmethod
    def erode(image):
        kernel = np.ones((2,2)) # strukturni element 3x3 blok
        return cv2.erode(image, kernel, iterations=1)

    @staticmethod
    def remove_noise(binary_image, times=1):
        for i in range(0, times):
            ret_val = ImageTransform.dilate(ImageTransform.erode(binary_image))
        return ret_val


    @staticmethod
    def image_augm_translate(image_path):
        img = cv2.imread(image_path,0)
        rows,cols = img.shape

        image_path_arr = image_path.split('/')
        image_dir_loc = ""

        image_file_name = image_path_arr[len(image_path_arr)-1]
        image_file_name = image_file_name.strip('.png')

        for i in range(0, len(image_path_arr)-1):
            image_dir_loc = image_dir_loc + image_path_arr[i] + "/"

        # x+ translating... time invariance
        for i in range(1, 3):
            M = np.float32([[1,0,i+1*10],[0,1,0]])
            dst = cv2.warpAffine(img,M,(cols,rows))
            cv2.imwrite(image_dir_loc+'/'+image_file_name+'_aug_x_plus_'+str(i)+".png", dst)

        # x- translating... time invariance
        for i in range(1, 3):
            M = np.float32([[1,0,-i*10],[0,1,0]])
            dst = cv2.warpAffine(img,M,(cols,rows))
            cv2.imwrite(image_dir_loc+'/'+image_file_name+'_aug_x_minus_'+str(i)+".png", dst)

        # y+ translating... time invariance
        for i in range(1, 3):
            M = np.float32([[1,0,0],[0,1,i*3]])
            dst = cv2.warpAffine(img,M,(cols,rows))
            cv2.imwrite(image_dir_loc+'/'+image_file_name+'_aug_y_plus_'+str(i)+".png", dst)

        # y- translating... time invariance
        for i in range(1, 3):
            M = np.float32([[1,0,0],[0,1,-i*3]])
            dst = cv2.warpAffine(img,M,(cols,rows))
            cv2.imwrite(image_dir_loc+'/'+image_file_name+'_aug_y_minus_'+str(i)+".png", dst)

        # x+ y- translating... time invariance
        for i in range(1, 3):
            M = np.float32([[1,0,i*10],[0,1,-i*3]])
            dst = cv2.warpAffine(img,M,(cols,rows))
            cv2.imwrite(image_dir_loc+'/'+image_file_name+'_aug_y_minus_x_plus_'+str(i)+".png", dst)

        # x+ y+ translating... time invariance
        for i in range(1, 3):
            M = np.float32([[1,0,i*10],[0,1,i*3]])
            dst = cv2.warpAffine(img,M,(cols,rows))
            cv2.imwrite(image_dir_loc+'/'+image_file_name+'_aug_y_plus_x_plus_'+str(i)+".png", dst)

        # x- y- translating... time invariance
        for i in range(1, 3):
            M = np.float32([[1,0,-i*10],[0,1,-i*3]])
            dst = cv2.warpAffine(img,M,(cols,rows))
            cv2.imwrite(image_dir_loc+'/'+image_file_name+'_aug_y_minus_x_minus_'+str(i)+".png", dst)

        # x- y+ translating... time invariance
        for i in range(1, 3):
            M = np.float32([[1,0,-i*10],[0,1,i*3]])
            dst = cv2.warpAffine(img,M,(cols,rows))
            dst = ImageTransform.resize_graph(dst) # vrati na org...
            cv2.imwrite(image_dir_loc+'/'+image_file_name+'_aug_y_plus_x_minus_'+str(i)+".png", dst)
        """
        # stetching scaleX+
        for i in range(1, 3):
            dst = cv2.resize(img,None,fx=1+i*0.5, fy=1, interpolation = cv2.INTER_CUBIC)
            #dst = ImageTransform.resize_graph(dst)
            cv2.imwrite(image_dir_loc+'/'+image_file_name+'_aug_scalex_plus_'+str(i)+".png", dst)

        # stetching scaleX-
        for i in range(1, 3):
            dst = cv2.resize(img,None,fx=1-i*0.5, fy=1, interpolation = cv2.INTER_CUBIC)
            #dst = ImageTransform.resize_graph(dst)
            cv2.imwrite(image_dir_loc+'/'+image_file_name+'_aug_scalex_minus_'+str(i)+".png", dst)
        """

    @staticmethod
    def gen_dataset_augmens():
        for asc_file in os.listdir("samples/ASC/graphs/"):
            if asc_file.endswith(".png"):
                ImageTransform.image_augm_translate("samples/ASC/graphs/"+asc_file)

        for desc_file in os.listdir("samples/DESC/graphs/"):
            if desc_file.endswith(".png"):
                ImageTransform.image_augm_translate("samples/DESC/graphs/"+desc_file)

        for flat_file in os.listdir("samples/FLAT/graphs/"):
            if flat_file.endswith(".png"):
                ImageTransform.image_augm_translate("samples/FLAT/graphs/"+flat_file)

        for soy_file in os.listdir("samples/SOY/graphs/"):
            if soy_file.endswith(".png"):
                ImageTransform.image_augm_translate("samples/SOY/graphs/"+soy_file)

