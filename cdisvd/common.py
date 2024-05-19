from dataclasses import dataclass
from pathlib import Path

import numpy as np
from numpy.linalg.linalg import SVDResult

INT_SIZE = 4
FLOAT_SIZE = 4
MODE = "RGB"
CHANNELS_COUNT = len(MODE)
HEADER = 16
SIGNATURE = b"\x42\x4f\x4f\x42"  # BOOB


@dataclass
class CompressedImage:
    width: int
    height: int
    k: int
    bands: list[SVDResult]

    def get_head(self) -> tuple[int, int, int]:
        return self.width, self.height, self.k


def save_compressed_svd(file: Path, image: CompressedImage) -> None:
    file.parent.mkdir(parents=True, exist_ok=True)

    if not file.suffix:
        file.with_suffix(".svd")

    with open(file, mode="wb") as f:
        f.write(SIGNATURE)
        for v in image.get_head():
            f.write(v.to_bytes(INT_SIZE, "big"))
        for band in image.bands:
            for matrix in band:
                f.write(matrix.astype(np.float32).tobytes())


def open_compressed_svd(file: Path) -> CompressedImage:
    with open(file, mode="rb") as f:
        if f.read(4) != SIGNATURE:
            raise TypeError("Input file is not a svd type.")
        data = f.read(INT_SIZE * 3)
        width, height, k = [
            int.from_bytes(data[i : i + INT_SIZE], byteorder="big")
            for i in range(0, len(data), INT_SIZE)
        ]
        bands: list[SVDResult] = []
        for _ in range(CHANNELS_COUNT):
            U = np.frombuffer(f.read(width * k * FLOAT_SIZE), dtype=np.float32).reshape(width, k)
            S = np.frombuffer(f.read(k * FLOAT_SIZE), dtype=np.float32)
            Vh = np.frombuffer(f.read(height * k * FLOAT_SIZE), dtype=np.float32).reshape(
                k, height
            )
            bands.append(SVDResult(U, S, Vh))
        return CompressedImage(width, height, k, bands)
