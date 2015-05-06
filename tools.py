"""Some tools used in the communication acoustics exercises."""

import numpy as np
import os
from scipy import signal
try:
    from urllib.request import Request, urlopen  # Python 3.x
except ImportError:
    from urllib2 import Request, urlopen  # Python 2.x


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


class HttpFile(object):

    """based on http://stackoverflow.com/a/7852229/500098"""

    def __init__(self, url):
        self._url = url
        self._offset = 0
        self._content_length = None

    def __len__(self):
        if self._content_length is None:
            response = urlopen(self._url)
            self._content_length = int(response.headers["Content-length"])
        return self._content_length

    def read(self, size=-1):
        request = Request(self._url)
        if size < 0:
            end = len(self) - 1
        else:
            end = self._offset + size - 1
        request.add_header('Range', "bytes={0}-{1}".format(self._offset, end))
        data = urlopen(request).read()
        self._offset += len(data)
        return data

    def seek(self, offset, whence=os.SEEK_SET):
        if whence == os.SEEK_SET:
            self._offset = offset
        elif whence == os.SEEK_CUR:
            self._offset += offset
        elif whence == os.SEEK_END:
            self._offset = len(self) + offset
        else:
            raise ValueError("Invalid whence")

    def tell(self):
        return self._offset
