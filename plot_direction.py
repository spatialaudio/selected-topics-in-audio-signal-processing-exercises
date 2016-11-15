#!/usr/bin/env python3
"""Plot the live microphone signal(s) with matplotlib."""
import argparse
from queue import Queue, Empty


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-w', '--window', type=float, default=200, metavar='DURATION',
    help='visible time slot (default: %(default)s ms)')
parser.add_argument(
    '-i', '--interval', type=float, default=30,
    help='minimum time between plot updates (default: %(default)s ms)')
parser.add_argument(
    '-b', '--blocksize', type=int, help='block size (in samples)')
parser.add_argument(
    '-r', '--samplerate', type=float, help='sampling rate of audio device')
parser.add_argument(
    '-n', '--downsample', type=int, default=1, metavar='N',
    help='display every Nth sample (default: %(default)s)')
parser.add_argument(
    'channels', type=int, default=[1,2], nargs='*', metavar='CHANNEL',
    help='input channels for estimation of direction (default: the first two)')
parser.add_argument(
    '-D', '--distance', type=float, default=0.2, metavar='DISTANCE', 
    help='distance of the two microphones channels (default: $(default) m)')
args = parser.parse_args()
if any(c < 1 for c in args.channels):
    parser.error('argument CHANNEL: must be >= 1')
mapping = [c - 1 for c in args.channels]  # Channel numbers start with 1
queue = Queue()


def audio_callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, flush=True)
    # Fancy indexing with mapping creates a (necessary!) copy:
    queue.put(indata[::args.downsample, mapping])


def update_plot(frame):
    """This is called by matplotlib for each plot update.

    Typically, audio callbacks happen more frequently than plot updates,
    therefore the queue tends to contain multiple blocks of audio data.

    """
    global newdata
    global corr
    block = True  # The first read from the queue is blocking ...
    
    while True:
        try:
            data = queue.get(block=block)
        except Empty:
            break
        shift = len(data)
        
        newdata = np.roll(newdata, -shift, axis=0)
        newdata[-shift:,:] = data
        block=False # ... all further reads are non-blocking
    
    corr = np.correlate(newdata[:,0], newdata[:,1], mode='full')
    corr = np.abs(corr)/np.max(np.max(corr))
    
    lines[0].set_ydata(corr)

    return lines

try:
    from matplotlib.animation import FuncAnimation
    import matplotlib.pyplot as plt
    import numpy as np
    import sounddevice as sd

    if args.list_devices:
        print(sd.query_devices())
        parser.exit()
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        args.samplerate = device_info['default_samplerate']

    length = int(args.window * args.samplerate/ (1000 * args.downsample))
    ran = args.distance/343*args.samplerate/args.downsample
    newdata = np.zeros((length, len(args.channels)))
    corr = np.zeros((2*length-1))

    phi = np.linspace(0, 180, 6);
    phi = np.append(phi, 90)
    xtics = ran*np.cos(phi*np.pi/180) +length-1
    xlabels = phi

    fig, ax = plt.subplots()
    lines = ax.plot(corr)
    ax.axis((-ran+length-1, ran+length-1, 0, 1))
    ax.set_xticks(xtics)
    ax.set_xticklabels(xlabels)
    ax.yaxis.grid(True)
    fig.tight_layout(pad=0)

    stream = sd.InputStream(
        device=args.device, channels=max(args.channels),
        samplerate=args.samplerate, callback=audio_callback)
    ani = FuncAnimation(fig, update_plot, interval=args.interval, blit=True)
    with stream:
        plt.show()
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
