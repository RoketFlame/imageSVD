from nptyping import Float32, NDArray, Shape
import numpy as np
from numpy.linalg.linalg import SVDResult
from cdisvd.svd.common import FloatMatrix, SvdMethod


class NumpySvdMethod(SvdMethod):
    @staticmethod
    def get_svd(A: FloatMatrix, k: int) -> SVDResult:
        U, S, Vh = np.linalg.svd(A)
        return SVDResult(U=U[:, :k], S=S[:k], Vh=Vh[:k, :])
