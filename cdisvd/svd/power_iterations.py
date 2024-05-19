import numpy as np
from numpy.linalg.linalg import SVDResult

from cdisvd.svd.common import FloatMatrix, SvdMethod


class PowerIterationsMethod(SvdMethod):
    @staticmethod
    def get_svd(A: FloatMatrix, k: int) -> SVDResult:
        U = np.zeros((A.shape[0], 1))
        Vh = np.zeros((A.shape[1], 1))
        S = []

        rank = np.linalg.matrix_rank(A)
        for _ in range(rank):
            B = A.T.dot(A)
            x = B.dot(np.random.normal(0, 1, size=A.shape[1]))

            v = x / np.linalg.norm(x)
            sigma = np.linalg.norm(A.dot(v))
            u = A.dot(v) / sigma

            u, sigma, v = np.reshape(u, (A.shape[0], 1)), sigma, np.reshape(v, (A.shape[1], 1))

            U = np.hstack((U, u))
            S.append(sigma)
            Vh = np.hstack((Vh, v))

            A = A - u.dot(v.T) * sigma

        return SVDResult(U=U[:, 1 : k + 1], S=np.array(S)[:k], Vh=Vh.T[1 : k + 1, :])
