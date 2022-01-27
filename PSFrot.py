class PSFrot(object):
    def readImage(path, gray=True, normalize=True):
        """
        erads image from a file
        """
        from skimage import exposure
        from skimage import io
        im = io.imread(path, as_gray=gray, plugin='pil')
        if normalize:
            im = exposure.rescale_intensity(im)
        return im

    def threshold(im, intensity=0.4):
        """
        Makes an threshold on given intensity level.
        """
        thresholded = (im < intensity)*1.0
        return thresholded

    def findCircles(im, minRadius=2, maxRadius=5):
        """
        finds circler in a image
        returns arrays of centres
        """
        from skimage.transform import hough_circle, hough_circle_peaks
        hough_radii = range(minRadius, maxRadius)
        hough_res = hough_circle(im, hough_radii)
        accums, cx, cy, radii = hough_circle_peaks(
            hough_res, hough_radii, total_num_peaks=2)
        return cx, cy, radii

    def centresOfMases(im, labeledImage=False, darkBlobs=True):
        """
        Finds centres of mass from each blob.
            `im` - binary image with separated blbs. 

            `labeledImage` - option for labeling the centre with green color

            `darkBlobs` - set as `True` if the blobs have value zero or `False`.
        Returns
        """
        from scipy import ndimage as ndi
        import numpy as np
        from skimage.color import gray2rgb
        if labeledImage:
            imC = gray2rgb(im)
        if darkBlobs:
            im = np.abs(1-im)
        label_objects, _ = ndi.label(im)
        c1 = ndi.center_of_mass(label_objects*(label_objects == 1))
        c2 = ndi.center_of_mass(label_objects*(label_objects == 2))
        angle = np.rad2deg(np.arctan2(c1[0] - c2[0], c1[1] - c2[1]))
        cx = [int(c1[1]), int(c2[1])]
        cy = [int(c1[0]), int(c2[0])]
        if labeledImage:
            for cx, cy in zip(cx, cy):
                imC[cy, cx] = (0, 1., 0)
            return c1, c2, angle, imC
        else:
            return c1, c2, angle

# %% Libraries import


if __name__ == "__main__":
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
        axs[0].imshow(im1, cmap=cmap)
        axs[1].imshow(im2, cmap=cmap)
        plt.show()

    def normalize(imAr, type=255):
        """
        `imAr` array of images
        """
        return(np.uint8(imAr * 255/np.max(imAr)))

    # %% import test image
    imC = Image.open("test_imgs/0.tiff").convert('L')
    imAr = np.array(imC)
    # %%

    imShow2(imAr, normalize(imAr))

    # %%
    im = io.imread("test_imgs/3.tiff", as_gray=True)
    im = exposure.rescale_intensity(im)  # normalizace obrázku

    binGray = (im > 0.4)*1.
    plt.imshow(binGray)
    plt.colorbar()

    # https://www.geeksforgeeks.org/image-segmentation-using-pythons-scikit-image-module/

    # %% segmentation
    hough_radii = np.arange(2, 5)
    hough_res = hough_circle(binGray, hough_radii)
    accums, cx, cy, radii = hough_circle_peaks(
        hough_res, hough_radii, total_num_peaks=2)

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
    # %% Pokusná buňka pro separacu
    i = -2
    filename = "test_imgs/" + str(i) + ".tiff"
    image = PSFrot.readImage(path=filename)
    image = PSFrot.threshold(image, intensity=0.4)
    # cx, cy, rad = PSFrot.findCircles(image)
    # imC = gray2rgb(image)
    # print(np.rad2deg(np.arctan2(cy[1] - cy[0], cx[1] - cx[0])))
    # for cx, cy in zip(cx, cy):
    #     imC[cy, cx] = (0, 1., 0)
    # axs[i//5, 4-i%5].imshow(imC)
    # axs[i//5, 4-i%5].format(title = str(i) + " um")
    fill_psf = np.abs(1-image)
    plt.imshow(fill_psf)
    # fill_psf = ndi.binary_fill_holes(image)
    label_objects, nb_labels = ndi.label(fill_psf)
    plt.imshow(label_objects)
    c1 = ndi.center_of_mass(label_objects*(label_objects == 1))
    c2 = ndi.center_of_mass(label_objects*(label_objects == 2))
    print(c1, '\n', c2)
