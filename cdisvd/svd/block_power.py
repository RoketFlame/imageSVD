import numpy as np
from nptyping import Float32
from numpy.linalg.linalg import SVDResult

from cdisvd.svd.common import FloatMatrix, SvdMethod


class BlockPowerIterMethod(SvdMethod):
    @staticmethod
    def get_svd(A: FloatMatrix, k: int) -> SVDResult:
        width = A.shape[1]

        Vh = np.zeros((width, k))
        err = 1
        while err > 0.1:
            q, _ = np.linalg.qr(A @ Vh)
            U = np.matrix(q[:, :k])

            q, r = np.linalg.qr(A.T @ U)
            Vh = np.matrix(q[:, :k])
            S = np.matrix(r[:k, :k])

            err = np.linalg.norm(A @ Vh - U * S).astype(Float32)

        return SVDResult(U=U, S=np.diagonal(S).astype(np.float32), Vh=Vh.T)
