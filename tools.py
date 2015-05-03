"""Some tools used in the communication acoustics exercises."""

import numpy as np
from scipy import signal


def normalize(x, maximum=1, axis=None, out=None):
    """Normalize a signal to the given maximum (absolute) value.

    Parameters
    ----------
    x : array_like
        Input signal.
    maximum : float or sequence of floats, optional
        Desired (absolute) maximum value.  By default, the signal is
        normalized to +-1.0.  If a sequence is given, it must have the
        same length as the dimension given by `axis`.  Each sub-array
        along the given axis is normalized with one of the values.
    axis : int, optional
        Normalize along a given axis.
        By default, the flattened array is normalized.
    out : numpy.ndarray or similar, optional
        If given, the result is stored in `out` and `out` is returned.
        If `out` points to the same memory as `x`, the normalization
        happens in-place.

    Returns
    -------
    numpy.ndarray
        The normalized signal.

    """
    if axis is None and not np.isscalar(maximum):
        raise TypeError("If axis is not specified, maximum must be a scalar")

    maximum = np.max(np.abs(x), axis=axis) / maximum
    if axis is not None:
        maximum = np.expand_dims(maximum, axis=axis)
    return np.true_divide(x, maximum, out)


def blackbox(x, samplerate, axis=-1):
    """Some unknown (except that it's LTI) digital system.

    Parameters
    ----------
    x : array_like
        Input signal.
    samplerate : float
        Sampling rate in Hertz.
    axis : int, optional
        The axis of the input data array along which to apply the
        system.  By default, this is the last axis.

    Returns
    -------
    numpy.ndarray
        The output signal.

    """
    # You are not supposed to look!
    b, a = signal.cheby1(8, 0.1, 3400 * 2 / samplerate)
    x = signal.lfilter(b, a, x, axis)
    b, a = signal.cheby1(4, 0.1, 300 * 2 / samplerate, 'high')
    return signal.lfilter(b, a, x, axis)


def blackbox_nonlinear(x, samplerate, axis=-1):
    """Some unknown (except that it's non-linear) digital system.

    See Also
    --------
    blackbox

    """
    # You are not supposed to look!
    thr = 1/7
    out = blackbox(x, samplerate, axis)
    x = np.max(np.abs(out)) * thr
    return np.clip(out, -x, x, out=out)
