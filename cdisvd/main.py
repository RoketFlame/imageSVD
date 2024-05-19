import enum
from pathlib import Path
from typing import Annotated

import typer
from typer import Argument, Option

from cdisvd.common import (
    CompressedImage,
    open_compressed_svd,
    save_compressed_svd,
)
from cdisvd.compress import compress_image
from cdisvd.decompress import decompress_image
from cdisvd.svd.block_power import BlockPowerIterMethod
from cdisvd.svd.common import SvdMethod
from cdisvd.svd.numpy_svd import NumpySvdMethod
from cdisvd.svd.power_iterations import PowerIterationsMethod

app = typer.Typer(
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
)


class SvdMethods(enum.Enum):
    numpy = "numpy"
    power_iterations = "power-iterations"
    block_power_iter = "block-power-iter"


def get_svd_method(method: SvdMethods) -> SvdMethod:
    match method:
        case SvdMethods.numpy:
            return NumpySvdMethod
        case SvdMethods.power_iterations:
            return PowerIterationsMethod
        case SvdMethods.block_power_iter:
            return BlockPowerIterMethod
    return NumpySvdMethod


@app.command()
def compress(
    input_file: Annotated[
        Path,
        Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            resolve_path=True,
            readable=True,
            autocompletion=lambda: [],
            help="Path to input .bmp image.",
        ),
    ],
    method: Annotated[
        SvdMethods,
        Option(
            ...,
            help="SVD method used.",
        ),
    ] = SvdMethods.numpy,
    out: Annotated[
        Path,
        Option(
            "--out-file",
            "-o",
            autocompletion=lambda: [],
            help="Path to out compressed image.",
        ),
    ] = Path("compressed.svd"),
    power: Annotated[
        int,
        Option(
            min=2,
            clamp=True,
            help="Degree of compression, the number of times the file size is reduced.",
        ),
    ] = 2,
) -> None:
    svd_method = get_svd_method(method)
    compressed = compress_image(input_file, svd_method, power)
    width, k = compressed[0].U.shape
    height = compressed[0].Vh.shape[1]
    compressed_image = CompressedImage(width, height, k, compressed)
    save_compressed_svd(out, compressed_image)


@app.command()
def decompress(
    input_file: Annotated[
        Path,
        Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            resolve_path=True,
            readable=True,
            autocompletion=lambda: [],
            help="Path to input compressed file.",
        ),
    ],
    out: Annotated[
        Path,
        Option(
            "--out-file",
            "-o",
            help="Path to out decompressed image.",
        ),
    ],
) -> None:
    compressed_image = open_compressed_svd(input_file)
    image = decompress_image(compressed_image)
    out.parent.mkdir(parents=True, exist_ok=True)
    image.save(out, format="BMP")


if __name__ == "__main__":
    app()
