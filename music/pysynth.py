#!/usr/bin/env python

"""
##########################################################################
#                       * * *  PySynth  * * *
#       A very basic audio synthesizer in Python (www.python.org)
#
#          Martin C. Doege, 2009-04-07 (mdoege@compuserve.com)
##########################################################################
# Based on a program by Tyler Eaves (tyler at tylereaves.com) found at
#   http://mail.python.org/pipermail/python-list/2000-August/041308.html
##########################################################################

# 'song' is a Python list (or tuple) in which the song is defined,
#   the format is [['note', value]]

# Notes are 'a' through 'g' of course,
# optionally with '#' or 'b' appended for sharps or flats.
# Finally the octave number (defaults to octave 4 if not given).
# An asterisk at the end makes the note a little louder (useful for the beat).
# 'r' is a rest.

# Note value is a number:
# 1=Whole Note; 2=Half Note; 4=Quarter Note, etc.
# Dotted notes can be written in two ways:
# 1.33 = -2 = dotted half
# 2.66 = -4 = dotted quarter
# 5.33 = -8 = dotted eighth
"""

from demosongs import *
from mkfreq import getfreq

pitchhz, keynum = getfreq(pr = True)

##########################################################################
#### Main program starts below
##########################################################################
# Some parameters:

# Beats (quarters) per minute
# e.g. bpm = 95

# Octave shift (neg. integer -> lower; pos. integer -> higher)
# e.g. transpose = 0

# Pause between notes as a fraction (0. = legato and e.g., 0.5 = staccato)
# e.g. pause = 0.05

# Volume boost for asterisk notes (1. = no boost)
# e.g. boost = 1.2

# Output file name
#fn = 'pysynth_output.wav'

# Other parameters:

# Influences the decay of harmonics over frequency. Lowering the
# value eliminates even more harmonics at high frequencies.
# Suggested range: between 3. and 5., depending on the frequency response
#  of speakers/headphones used
harm_max = 4.
##########################################################################

import wave, math, struct
from mixfiles import mix_files

def make_wav(song,bpm=120,transpose=0,pause=.05,boost=1.1,repeat=0,fn="out.wav", silent=False):
	f=wave.open(fn,'w')

	f.setnchannels(1)
	f.setsampwidth(2)
	f.setframerate(44100)
	f.setcomptype('NONE','Not Compressed')

	bpmfac = 120./bpm

	def length(l):
		return 88200./l*bpmfac

	def waves2(hz,l):
		a=44100./hz
		b=float(l)/44100.*hz
		return [a,round(b)]

	def sixteenbit(x):
		return struct.pack('h', round(32000*x))

	def asin(x):
		return math.sin(2.*math.pi*x)

	def render2(a,b,vol):
		b2 = (1.-pause)*b
		l=waves2(a,b2)
		ow=b''
		q=int(l[0]*l[1])

		# harmonics are frequency-dependent:
		lf = math.log(a)
		lf_fac = (lf-3.) / harm_max
		if lf_fac > 1: harm = 0
		else: harm = 2. * (1-lf_fac)
		decay = 2. / lf
		t = (lf-3.) / (8.5-3.)
		volfac = 1. + .8 * t * math.cos(math.pi/5.3*(lf-3.))

		for x in range(q):
			fac=1.
			if x<100: fac=x/80.
			if 100<=x<300: fac=1.25-(x-100)/800.
			if x>q-400: fac=1.-((x-q+400)/400.)
			s = float(x)/float(q)
			dfac =  1. - s + s * decay
			ow=ow+sixteenbit((asin(float(x)/l[0])
				+harm*asin(float(x)/(l[0]/2.))
				+.5*harm*asin(float(x)/(l[0]/4.)))/4.*fac*vol*dfac*volfac)
		fill = max(int(ex_pos - curpos - q), 0)
		f.writeframesraw((ow)+(sixteenbit(0)*fill))
		return q + fill

	##########################################################################
	# Write to output file (in WAV format)
	##########################################################################

	if silent == False:
		print("Writing to file", fn)
	curpos = 0
	ex_pos = 0.
	for rp in range(repeat+1):
		for nn, x in enumerate(song):
			if not nn % 4 and silent == False:
				print("[%u/%u]\t" % (nn+1,len(song)))
			if x[0]!='r':
				if x[0][-1] == '*':
					vol = boost
					note = x[0][:-1]
				else:
					vol = 1.
					note = x[0]
				try:
					a=pitchhz[note]
				except:
					a=pitchhz[note + '4']	# default to fourth octave
				a = a * 2**transpose
				if x[1] < 0:
					b=length(-2.*x[1]/3.)
				else:
					b=length(x[1])
				ex_pos = ex_pos + b
				curpos = curpos + render2(a,b,vol)

			if x[0]=='r':
				b=length(x[1])
				ex_pos = ex_pos + b
				f.writeframesraw(sixteenbit(0)*int(b))
				curpos = curpos + int(b)

	f.writeframes(b'')
	f.close()
	print()

##########################################################################
# Synthesize demo songs
##########################################################################

if __name__ == '__main__':
	print()
	print("Creating Demo Songs... (this might take about a minute)")
	print()

	# SONG 1
	make_wav(song1, fn = "pysynth_scale.wav")

	# SONG 2
	make_wav(song2, bpm = 95, boost = 1.2, fn = "pysynth_anthem.wav")

	# SONG 3
	make_wav(song3, bpm = 132/2, pause = 0., boost = 1.1, fn = "pysynth_chopin.wav")

	# SONG 4
	#   right hand part
	make_wav(song4_rh, bpm = 130, transpose = 1, pause = .1, boost = 1.15, repeat = 1, fn = "pysynth_bach_rh.wav")
	#   left hand part
	make_wav(song4_lh, bpm = 130, transpose = 1, pause = .1, boost = 1.15, repeat = 1, fn = "pysynth_bach_lh.wav")
	#   mix both files together
	mix_files("pysynth_bach_rh.wav", "pysynth_bach_lh.wav", "pysynth_bach.wav")

