import math
from pathlib import Path
from typing import List

import numpy as np
from numpy.linalg.linalg import SVDResult
from PIL import Image
from rich.progress import track

from cdisvd.common import CHANNELS_COUNT, FLOAT_SIZE, HEADER, MODE
from cdisvd.svd.common import SvdMethod


def compress_image(path_image: Path, method: SvdMethod, power: int) -> List[SVDResult]:
    image = Image.open(path_image)
    k = get_k(path_image.stat().st_size, image, power)
    bands = image.convert(MODE).split()
    compressed_bands: list[SVDResult] = []
    for band in track(bands, description="Yeah, it's compressing!.?", total=len(bands)):
        matrix = np.array(band)
        compressed_bands.append(method.get_svd(matrix, k))
    return compressed_bands


def get_k(raw_size: int, image: Image.Image, power: int) -> int:
    w, h = image.size
    k = (raw_size / power - HEADER) / (CHANNELS_COUNT * FLOAT_SIZE * (w + h + 1))
    if k < 1:
        raise ValueError(
            "Compression power is impossible, maximum is",
            raw_size / (HEADER + CHANNELS_COUNT * FLOAT_SIZE * (w + h + 1)),
        )
    return math.floor(k)
