import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter

rng = np.random.default_rng()

# shape = (1024, )
# shape = (512, 512)
shape = (128, 128, 128)

white = rng.normal(size=shape)
if len(shape) == 1:
    fig, ax = plt.subplots(3, 1, sharex='col',
                           num='LPF noise comparison',
                           figsize=(9, 6))
else:
    fig, ax = plt.subplots(1, 3,
                           num='LPF noise comparison',
                           figsize=(9, 6))

if white.ndim == 1:
    # Plot the curve
    ax[0].plot(white)
elif white.ndim == 2:
    # Plot a heatmap
    ax[0].imshow(white, cmap='gray')
elif white.ndim == 3:
    # Plot a heatmap of the first slice
    ax[0].imshow(white[0], cmap='gray')
ax[0].set_title('White noise')

filtered = gaussian_filter(white, 7, mode='wrap')

del white


# Plot it tiled next to itself
tiled = np.hstack((filtered, filtered))

if tiled.ndim == 1:
    ax[1].plot(tiled)
elif tiled.ndim == 2:
    ax[1].imshow(tiled, cmap='gray')
elif tiled.ndim == 3:
    ax[1].imshow(tiled[0], cmap='gray')
ax[1].set_title('Filtered, tiled')

del tiled

vmin = filtered.min()
vmax = filtered.max()
if filtered.ndim == 3:
    for n, slice in enumerate(filtered):
        plt.imsave(f'slice {n:03d}.png', filtered[n], vmin=vmin, vmax=vmax,
                   cmap='gray')
