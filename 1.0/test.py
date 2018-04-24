from skimage import io


image = io.imread("chevalnb.png")
image = image.astype(int)
print(image)
