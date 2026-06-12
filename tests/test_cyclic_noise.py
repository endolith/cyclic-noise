"""Tests for cyclic_noise."""

import numpy as np
import pytest

from cyclic_noise import cyclic_noise


@pytest.mark.parametrize(
    "shape",
    [
        32,
        (16, 24),
        (8, 12, 10),
    ],
)
def test_output_shape(shape: int | tuple[int, ...]) -> None:
    expected = (shape,) if isinstance(shape, int) else shape
    out = cyclic_noise(shape, sigma=2.0, seed=0)
    assert out.shape == expected
    assert out.dtype == np.float64


@pytest.mark.parametrize(
    "shape",
    [
        64,
        (48, 40),
        (24, 32, 20),
    ],
)
def test_loop_periodicity(shape: int | tuple[int, ...]) -> None:
    """Tiled output should not jump more than a typical interior step at each seam."""
    out = cyclic_noise(shape, sigma=3.0, seed=1)
    for axis in range(out.ndim):
        seam = np.abs(np.take(out, 0, axis=axis) - np.take(out, -1, axis=axis))
        max_interior_step = np.abs(np.diff(out, axis=axis)).max()
        assert seam.max() <= max_interior_step
