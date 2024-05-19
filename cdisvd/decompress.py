import numpy as np
from nptyping import Float32, NDArray, Shape, UInt8
from numpy.linalg.linalg import SVDResult
from PIL import Image
from rich.progress import track

from cdisvd.common import CHANNELS_COUNT, MODE, CompressedImage
from cdisvd.svd.common import FloatMatrix


def svd_to_matrix(svd: SVDResult) -> FloatMatrix:
    res: FloatMatrix = (svd.U @ np.diag(svd.S) @ svd.Vh).clip(0, 255)
    return np.nan_to_num(res)


def decompress_image(
    compressed: CompressedImage,
) -> Image.Image:
    out_channels: list[NDArray[Shape[...], Float32]] = []
    for svd in track(compressed.bands, description="Decompressing...", total=CHANNELS_COUNT):
        out_channels.append(svd_to_matrix(svd))
    merged = np.dstack(out_channels).astype(UInt8)
    return Image.fromarray(merged, mode=MODE)  # type: ignore
