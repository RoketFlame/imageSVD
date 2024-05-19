from typing import Any, Protocol

from numpy.linalg.linalg import SVDResult
from nptyping import NDArray, Float32, Shape

FloatMatrix = NDArray[Shape["*, *"], Float32]


class SvdMethod(Protocol):
    @staticmethod
    def get_svd(a: FloatMatrix, k: int) -> SVDResult: ...
