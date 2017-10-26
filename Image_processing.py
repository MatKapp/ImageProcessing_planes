from skimage import data, io
from matplotlib import pyplot as plt

image = data.coins() # Albo: coins(), page(), moon()
io.imshow(image)
plt.show()