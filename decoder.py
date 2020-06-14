import sys
import numpy
import scipy.signal
from PIL import Image
import scipy.io.wavfile


class APT(object):

    # Audio signal rate
    RATE = 20800
    # Line length
    NOAA_LINE_LENGTH = 2080

    def __init__(self, filename):
        # Retrieve signal rate and signal from wav file
        (rate, self.signal) = scipy.io.wavfile.read(filename)
        # Check if signal rate is 20800 Hz
        if rate != self.RATE:
            # Resample audio file to 20800 Hz
            coef = self.RATE / rate
            samples = int(coef * len(self.signal))
            signal = scipy.signal.resample(self.signal, samples)
            # Write resampled signal file
            scipy.io.wavfile.write("resampled.wav", self.RATE, signal)
        truncate = self.RATE * int(len(self.signal) // self.RATE)
        self.signal = self.signal[:truncate]

    def decode(self, outfile=None):
        # Hilbert transform
        hilbert = scipy.signal.hilbert(self.signal)
        # Filter the signal
        filtered = scipy.signal.medfilt(numpy.abs(hilbert), 5)
        # Reshape
        reshaped = filtered.reshape(len(filtered) // 5, 5)
        # Digitize
        digitized = self._digitize(reshaped[:, 2])
        # Reshape and form matrix
        matrix = self._reshape(digitized)
        # Render image from matrix
        image = Image.fromarray(matrix)
        if not outfile is None:
            # Save the image given the outfile name
            image.save(outfile)
        image.show()
        return matrix

    def _digitize(self, signal, plow=0.5, phigh=99.5):
        # Convert signal to numbers between 0 and 255.
        (low, high) = numpy.percentile(signal, (plow, phigh))
        delta = high - low
        data = numpy.round(255 * (signal - low) / delta)
        data[data < 0] = 0
        data[data > 255] = 255
        return data.astype(numpy.uint8)

    def reshape(self, signal):
        '''
        Find sync frames and reshape the 1D signal into a 2D image.
        Finds the sync A frame by looking at the maximum values of the cross
        correlation between the signal and a hardcoded sync A frame.
        The expected distance between sync A frames is 2080 samples, but with
        small variations because of Doppler effect.
        '''
        # sync frame to find: seven impulses and some black pixels (some lines
        # have something like 8 black pixels and then white ones)
        syncA = [0, 128, 255, 128]*7 + [0]*7

        # list of maximum correlations found: (index, value)
        peaks = [(0, 0)]

        # minimum distance between peaks
        mindistance = 2000

        # need to shift the values down to get meaningful correlation values
        signalshifted = [x-128 for x in signal]
        syncA = [x-128 for x in syncA]
        for i in range(len(signal)-len(syncA)):
            corr = numpy.dot(syncA, signalshifted[i : i+len(syncA)])

            # if previous peak is too far, keep it and add this value to the
            # list as a new peak
            if i - peaks[-1][0] > mindistance:
                peaks.append((i, corr))

            # else if this value is bigger than the previous maximum, set this
            # one
            elif corr > peaks[-1][1]:
                peaks[-1] = (i, corr)

        # create image matrix starting each line on the peaks found
        matrix = []
        for i in range(len(peaks) - 1):
            matrix.append(signal[peaks[i][0] : peaks[i][0] + 2080])

        return numpy.array(matrix)


if __name__ == '__main__':
    apt = APT(sys.argv[1])
    # Check for outfile name
    if len(sys.argv) > 2:
        outfile = sys.argv[2]
    else:
        outfile = None
    # Decode the APT signal
    apt.decode(outfile)