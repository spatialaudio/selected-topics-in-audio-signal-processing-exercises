"""Some tools used in the communication acoustics exercises."""

import numpy as np
from scipy import signal


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
    numpy.array
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
