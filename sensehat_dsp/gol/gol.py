import torch
import torch.nn.functional as F

from typing import Iterator
from collections import deque


class GOL:
    def __init__(
        self,
        grid_size: int = 8,
        kernel_size: int = 3,
        n_prev_grids: int = 2,
    ):
        self.grid_size = grid_size
        self.grid = self.get_initial_grid()
        self.kernel = self.get_kernel(kernel_size=kernel_size)

        self.prev_grids = deque(maxlen=n_prev_grids)
        self.prev_grids.append(self.get_initial_grid())

    def get_initial_grid(self, alive_proportion: float = 0.2) -> torch.Tensor:
        return (
            torch.rand((1, 1, self.grid_size, self.grid_size))
            < alive_proportion
        ).float()

    @staticmethod
    def get_kernel(kernel_size: int) -> torch.Tensor:
        kernel = torch.ones(
            (1, 1, kernel_size, kernel_size),
            dtype=torch.float32,
        )

        kernel[:, :, kernel_size // 2, kernel_size // 2] = 0
        return kernel

    def get_grids(self) -> Iterator[torch.Tensor]:
        while True:
            if self.grid.sum() == 0:
                self.grid = self.get_initial_grid()
                yield self.grid

            if torch.equal(self.prev_grids[-1], self.grid):
                self.grid = self.get_initial_grid()
                yield self.grid

            neighbors = F.conv2d(self.grid.float(), self.kernel, padding=1)
            self.grid = (
                (neighbors == 3) | ((self.grid == 1) & (neighbors == 2))
            ).float()

            self.prev_grids.append(self.grid)
            yield self.grid
