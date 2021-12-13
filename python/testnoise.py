import matplotlib.pyplot as plt
import noise
from perlin_noise import PerlinNoise

noise1 = PerlinNoise(octaves=3)


xpix, ypix = 100, 100
pic = []
for i in range(xpix):
    row = []
    for j in range(ypix):
        noise_val = noise.pnoise2(i/xpix,  j/ypix, 3, 0.5, 2)
        #noise_val = noise1([i/xpix, j/ypix])

        row.append(noise_val)
    pic.append(row)

plt.imshow(pic, cmap='gray')
plt.show()