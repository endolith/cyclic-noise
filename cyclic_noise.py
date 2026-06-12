"""Low-pass filtered noise that tiles seamlessly along every axis (cyclic / toroidal)."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from scipy.ndimage import gaussian_filter

__all__ = ["cyclic_noise"]


def cyclic_noise(
    shape: int | Sequence[int],
    sigma: float | Sequence[float],
    *,
    rng: np.random.Generator | None = None,
    seed: int | np.ndarray | np.random.SeedSequence | np.random.BitGenerator | np.random.Generator | None = None,
    order: int = 0,
    truncate: float = 4.0,
) -> np.ndarray:
    """Generate smooth noise that loops perfectly when tiled along each dimension.

    White noise is drawn from a standard normal distribution, then low-pass filtered
    with a Gaussian kernel using boundary mode ``wrap`` so opposite edges match.
    That yields a field that can be repeated (e.g. for looping textures or animation)
    without seams.

    Parameters
    ----------
    shape
        Output array shape. A single integer ``n`` is treated as ``(n,)``.
    sigma
        Gaussian standard deviation in pixels, passed to
        :func:`scipy.ndimage.gaussian_filter`. A scalar uses the same sigma on every
        axis; a sequence sets one value per axis (length must match ``shape``).
    rng
        NumPy random generator. If given, ``seed`` must not be set.
    seed
        Seed for :func:`numpy.random.default_rng` when ``rng`` is omitted.
    order
        Filter order along each axis (0 = plain Gaussian smoothing). See SciPy.
    truncate
        Truncate the Gaussian kernel after this many standard deviations. See SciPy.

    Returns
    -------
    numpy.ndarray
        Filtered noise with ``dtype`` ``float64``, same shape as requested.

    Raises
    ------
    ValueError
        If both ``rng`` and ``seed`` are set, or ``shape`` is invalid.
    """
    if rng is not None and seed is not None:
        raise ValueError("Pass at most one of rng and seed.")
    if rng is None:
        rng = np.random.default_rng(seed)

    if isinstance(shape, int):
        shape_tuple = (shape,)
    else:
        shape_tuple = tuple(int(x) for x in shape)
    if not shape_tuple or any(d <= 0 for d in shape_tuple):
        raise ValueError("shape must be a non-empty tuple of positive integers.")

    white = rng.normal(size=shape_tuple)
    return gaussian_filter(
        white,
        sigma,
        order=order,
        mode="wrap",
        truncate=truncate,
    )


def _demo() -> None:
    import matplotlib.pyplot as plt

    # shape = (1024,)
    # shape = (512, 512)
    shape = (128, 128, 128)
    # Same seed as ``cyclic_noise`` so this matches the white noise it filters internally.
    white = np.random.default_rng(0).normal(size=shape)
    filtered = cyclic_noise(shape, 7, seed=0)

    if len(shape) == 1:
        fig, ax = plt.subplots(2, 1, sharex="col", num="LPF noise comparison", figsize=(9, 6))
    else:
        fig, ax = plt.subplots(1, 2, num="LPF noise comparison", figsize=(9, 6))

    if white.ndim == 1:
        ax[0].plot(white)
    elif white.ndim == 2:
        ax[0].imshow(white, cmap="gray")
    elif white.ndim == 3:
        ax[0].imshow(white[0], cmap="gray")
    ax[0].set_title("White noise")

    tiled = np.hstack((filtered, filtered))

    if tiled.ndim == 1:
        ax[1].plot(tiled)
    elif tiled.ndim == 2:
        ax[1].imshow(tiled, cmap="gray")
    elif tiled.ndim == 3:
        ax[1].imshow(tiled[0], cmap="gray")
    ax[1].set_title("Filtered, tiled")

    if filtered.ndim == 3:
        vmin = filtered.min()
        vmax = filtered.max()
        for n, frame in enumerate(filtered):
            plt.imsave(f"slice {n:03d}.png", frame, vmin=vmin, vmax=vmax, cmap="gray")


if __name__ == "__main__":
    _demo()
