# Author: Nicolas Boulanger-Lewandowski
# University of Montreal (2013)
# RNN-RBM deep learning tutorial
#
# Implements midiread and midiwrite functions to read/write MIDI files to/from piano-rolls


from MidiOutFile import MidiOutFile
from MidiInFile import MidiInFile
from MidiOutStream import MidiOutStream

import numpy


class midiread(MidiOutStream):
  def __init__(self, filename, r=(21, 109), dt=0.2):
    self.notes = []
    self._tempo = 500000
    self.beat = 0
    self.time = 0.0

    midi_in = MidiInFile(self, filename)
    midi_in.read()
    self.notes = [n for n in self.notes if n[2] is not None]  # purge incomplete notes

    length = int(numpy.ceil(max(zip(*self.notes)[2]) / dt))  # create piano-roll
    self.piano_roll = numpy.zeros((length, r[1]-r[0]))
    for n in self.notes:
      self.piano_roll[int(numpy.ceil(n[1]/dt)) : int(numpy.ceil(n[2]/dt)), n[0]-r[0]] = 1

  def abs_time_in_seconds(self):
    return self.time + self._tempo * (self.abs_time() - self.beat) * 1e-6 / self.div

  def tempo(self, value):
    self.time = self.abs_time_in_seconds()
    self.beat = self.abs_time()
    self._tempo = value
  
  def header(self, format=0, nTracks=1, division=96):
    self.div = division

  def note_on(self, channel=0, note=0x40, velocity=0x40):
    self.notes.append([note, self.abs_time_in_seconds(), None])

  def note_off(self, channel=0, note=0x40, velocity=0x40):
    i = len(self.notes) - 1
    while i >= 0 and self.notes[i][0] != note:
      i -= 1
    if i >= 0 and self.notes[i][2] is None:
      self.notes[i][2] = self.abs_time_in_seconds()

  def sysex_event(*args):
    pass

  def device_name(*args):
    pass


def midiwrite(filename, piano_roll, r=(21, 109), dt=0.2, patch=0):
  midi = MidiOutFile(filename)
  midi.header(division=100)
  midi.start_of_track() 
  midi.patch_change(channel=0, patch=patch)
  t = 0
  samples = [i.nonzero()[0] + r[0] for i in piano_roll]

  for i in xrange(len(samples)):
    for f in samples[i]:
      if i==0 or f not in samples[i-1]:
        midi.update_time(t)
        midi.note_on(channel=0, note=f, velocity=90)
        t = 0
    
    t += int(dt*200)

    for f in samples[i]:
      if i==len(samples)-1 or f not in samples[i+1]:
        midi.update_time(t)
        midi.note_off(channel=0, note=f, velocity=0)
        t = 0
      
  midi.update_time(0)
  midi.end_of_track()
  midi.eof()


""" This file contains different utility functions that are not connected
in anyway to the networks presented in the tutorials, but rather help in
processing the outputs into a more understandable way.

For example ``tile_raster_images`` helps in generating a easy to grasp
image from a set of samples or weights.
"""


def scale_to_unit_interval(ndar, eps=1e-8):
    """ Scales all values in the ndarray ndar to be between 0 and 1 """
    ndar = ndar.copy()
    ndar -= ndar.min()
    ndar *= 1.0 / (ndar.max() + eps)
    return ndar


def tile_raster_images(X, img_shape, tile_shape, tile_spacing=(0, 0),
                       scale_rows_to_unit_interval=True,
                       output_pixel_vals=True):
    """
    Transform an array with one flattened image per row, into an array in
    which images are reshaped and layed out like tiles on a floor.

    This function is useful for visualizing datasets whose rows are images,
    and also columns of matrices for transforming those rows
    (such as the first layer of a neural net).

    :type X: a 2-D ndarray or a tuple of 4 channels, elements of which can
    be 2-D ndarrays or None;
    :param X: a 2-D array in which every row is a flattened image.

    :type img_shape: tuple; (height, width)
    :param img_shape: the original shape of each image

    :type tile_shape: tuple; (rows, cols)
    :param tile_shape: the number of images to tile (rows, cols)

    :param output_pixel_vals: if output should be pixel values (i.e. int8
    values) or floats

    :param scale_rows_to_unit_interval: if the values need to be scaled before
    being plotted to [0,1] or not


    :returns: array suitable for viewing as an image.
    (See:`Image.fromarray`.)
    :rtype: a 2-d array with same dtype as X.

    """

    assert len(img_shape) == 2
    assert len(tile_shape) == 2
    assert len(tile_spacing) == 2

    # The expression below can be re-written in a more C style as
    # follows :
    #
    # out_shape    = [0,0]
    # out_shape[0] = (img_shape[0]+tile_spacing[0])*tile_shape[0] -
    #                tile_spacing[0]
    # out_shape[1] = (img_shape[1]+tile_spacing[1])*tile_shape[1] -
    #                tile_spacing[1]
    out_shape = [
        (ishp + tsp) * tshp - tsp
        for ishp, tshp, tsp in zip(img_shape, tile_shape, tile_spacing)
    ]

    if isinstance(X, tuple):
        assert len(X) == 4
        # Create an output numpy ndarray to store the image
        if output_pixel_vals:
            out_array = numpy.zeros((out_shape[0], out_shape[1], 4),
                                    dtype='uint8')
        else:
            out_array = numpy.zeros((out_shape[0], out_shape[1], 4),
                                    dtype=X.dtype)

        #colors default to 0, alpha defaults to 1 (opaque)
        if output_pixel_vals:
            channel_defaults = [0, 0, 0, 255]
        else:
            channel_defaults = [0., 0., 0., 1.]

        for i in range(4):
            if X[i] is None:
                # if channel is None, fill it with zeros of the correct
                # dtype
                dt = out_array.dtype
                if output_pixel_vals:
                    dt = 'uint8'
                out_array[:, :, i] = numpy.zeros(
                    out_shape,
                    dtype=dt
                ) + channel_defaults[i]
            else:
                # use a recurrent call to compute the channel and store it
                # in the output
                out_array[:, :, i] = tile_raster_images(
                    X[i], img_shape, tile_shape, tile_spacing,
                    scale_rows_to_unit_interval, output_pixel_vals)
        return out_array

    else:
        # if we are dealing with only one channel
        H, W = img_shape
        Hs, Ws = tile_spacing

        # generate a matrix to store the output
        dt = X.dtype
        if output_pixel_vals:
            dt = 'uint8'
        out_array = numpy.zeros(out_shape, dtype=dt)

        for tile_row in range(tile_shape[0]):
            for tile_col in range(tile_shape[1]):
                if tile_row * tile_shape[1] + tile_col < X.shape[0]:
                    this_x = X[tile_row * tile_shape[1] + tile_col]
                    if scale_rows_to_unit_interval:
                        # if we should scale values to be between 0 and 1
                        # do this by calling the `scale_to_unit_interval`
                        # function
                        this_img = scale_to_unit_interval(
                            this_x.reshape(img_shape))
                    else:
                        this_img = this_x.reshape(img_shape)
                    # add the slice to the corresponding position in the
                    # output array
                    c = 1
                    if output_pixel_vals:
                        c = 255
                    out_array[
                        tile_row * (H + Hs): tile_row * (H + Hs) + H,
                        tile_col * (W + Ws): tile_col * (W + Ws) + W
                    ] = this_img * c
        return out_array
