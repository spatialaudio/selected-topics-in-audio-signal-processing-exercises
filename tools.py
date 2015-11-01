"""Some tools used in the communication acoustics exercises."""
from __future__ import division  # Only needed for Python 2.x
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


def fade(x, in_length, out_length=None, type='l', copy=True):
    """Apply fade in/out to a signal.

    If `x` is two-dimenstional, this works along the columns (= first
    axis).

    This is based on the *fade* effect of SoX, see:
    http://sox.sourceforge.net/sox.html

    The C implementation can be found here:
    http://sourceforge.net/p/sox/code/ci/master/tree/src/fade.c

    Parameters
    ----------
    x : array_like
        Input signal.
    in_length : int
        Length of fade-in in samples (contrary to SoX, where this is
        specified in seconds).
    out_length : int, optional
        Length of fade-out in samples.  If not specified, `fade_in` is
        used also for the fade-out.
    type : {'t', 'q', 'h', 'l', 'p'}, optional
        Select the shape of the fade curve: 'q' for quarter of a sine
        wave, 'h' for half a sine wave, 't' for linear ("triangular")
        slope, 'l' for logarithmic, and 'p' for inverted parabola.
        The default is logarithmic.
    copy : bool, optional
        If `False`, the fade is applied in-place and a reference to
        `x` is returned.

    """
    x = np.array(x, copy=copy)

    if out_length is None:
        out_length = in_length

    def make_fade(length, type):
        fade = np.arange(length) / length
        if type == 't':  # triangle
            pass
        elif type == 'q':  # quarter of sinewave
            fade = np.sin(fade * np.pi / 2)
        elif type == 'h':  # half of sinewave... eh cosine wave
            fade = (1 - np.cos(fade * np.pi)) / 2
        elif type == 'l':  # logarithmic
            fade = np.power(0.1, (1 - fade) * 5)  # 5 means 100 db attenuation
        elif type == 'p':  # inverted parabola
            fade = (1 - (1 - fade)**2)
        else:
            raise ValueError("Unknown fade type {0!r}".format(type))
        return fade

    # Using .T w/o [:] causes error: https://github.com/numpy/numpy/issues/2667
    x[:in_length].T[:] *= make_fade(in_length, type)
    x[len(x) - out_length:].T[:] *= make_fade(out_length, type)[::-1]
    return x


def db(x, power=False):
    """Convert a signal to decibel.

    Parameters
    ----------
    x : array_like
        Input signal.  Values of 0 lead to negative infinity.
    power : bool, optional
        If `power=False` (the default), `x` is squared before
        conversion.

    """
    with np.errstate(divide='ignore'):
        return 10 if power else 20 * np.log10(np.abs(x))


def blackbox(x, samplerate, axis=0):
    """Some unknown (except that it's LTI) digital system.

    Parameters
    ----------
    x : array_like
        Input signal.
    samplerate : float
        Sampling rate in Hertz.
    axis : int, optional
        The axis of the input data array along which to apply the
        system.  By default, this is the first axis.

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


def blackbox_nonlinear(x, samplerate, axis=0):
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
