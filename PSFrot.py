class PSFrot(object):
    import numpy as np
    def readImage(path, gray = True, normalize=True):
        """
        erads image from a file
        """
        from skimage import exposure
        from skimage import io  
        im = io.imread(path, as_gray=gray)
        if normalize:
            im = exposure.rescale_intensity(im)
        return im
    def threshold(im, intensity=0.4):
        """
        Makes an threshold on given intensity level.
        """
        thresholded = (im < intensity)*1.0
        return thresholded
    def findCircles(im , minRadius = 2, maxRadius = 5):
        """
        finds circler in a image
        returns arrays of centres
        """
        from skimage.transform import hough_circle, hough_circle_peaks
        hough_radii = range(minRadius, maxRadius)
        hough_res = hough_circle(im, hough_radii)
        accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii, total_num_peaks=2)
        return cx, cy, radii

# %% Libraries import

if __name__=="__main__":
    from PIL import Image
    from PIL import ImageOps
    from skimage import exposure
    from skimage import io
    from skimage import segmentation
    from skimage.color import rgb2gray, gray2rgb
    from skimage.transform import hough_circle, hough_circle_peaks
    import numpy as np
    from skimage.draw import circle_perimeter
    import matplotlib.pyplot as plt

    def imShow2(im1, im2, cmap='Greys'):
        fig, axs = plt.subplots(2)
        axs[0].imshow(im1, cmap = cmap)
        axs[1].imshow(im2, cmap = cmap)
        plt.show()

    def normalize(imAr, type = 255):
        """
        `imAr` array of images
        """
        return(np.uint8(imAr* 255/np.max(imAr)))

    # %% import test image
    imC = Image.open("test_imgs/0.tiff").convert('L')
    imAr = np.array(imC)
    # %%

    imShow2(imAr, normalize(imAr))


    # %%
    im = io.imread("test_imgs/3.tiff", as_gray=True)
    im = exposure.rescale_intensity(im) # normalizace obrázku

    binGray = (im>0.4)*1.
    plt.imshow(binGray)
    plt.colorbar()

    # https://www.geeksforgeeks.org/image-segmentation-using-pythons-scikit-image-module/

    # %% segmentation 
    hough_radii = np.arange(2, 5)
    hough_res = hough_circle(binGray, hough_radii)
    accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii, total_num_peaks=2)

    # %%

    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 4))
    imC = gray2rgb(binGray)
    for center_y, center_x, radius in zip(cy, cx, radii):
        circy, circx = circle_perimeter(center_y, center_x, radius,
                                        shape=imC.shape)
        imC[circy, circx] = (1.0, 0, 0)
        imC[center_y, center_x] = (0, 1., 0)

    ax.imshow(imC, cmap=plt.cm.gray)
    plt.show()