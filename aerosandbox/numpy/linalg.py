import numpy as _onp
import casadi as _cas
from aerosandbox.numpy.determine_type import is_casadi_type

def inner(x, y):
    """Return the inner product of vectors x and y."""
    try:
        return _onp.inner(x, y)
    except Exception:
        if len(x.shape) == 1:  # Force x to be transposable if it's not.
            x = _onp.expand_dims(x, 1)
        return x.T @ y


def outer(x, y):
    """Return the outer product of vectors x and y."""
    try:
        return _onp.outer(x, y)
    except Exception:
        if len(y.shape) == 1:  # Force y to be transposable if it's not.
            y = _onp.expand_dims(y, 1)
        return x @ y.T


def solve(A, b):  # TODO get this working
    """
    Solve the linear system Ax=b for x.
    Args:
        A: A square matrix.
        b: A vector representing the RHS of the linear system.

    Returns: The solution vector x.

    """
    try:
        return _onp.linalg.solve(A, b)
    except Exception:
        return _cas.solve(A, b)


def norm(x):
    """
    Returns the L2-norm of a vector x.
    """
    try:
        return _onp.linalg.norm(x)
    except Exception:
        return _cas.norm_2(x)
