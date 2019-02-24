#!/usr/bin/env python

# Mix two mono files to get a stereo file

import sys, wave, struct

def mix_files(a, b, c, chann = 2, phase = -1.):
	f1 = wave.open(a, 'r')
	f2 = wave.open(b, 'r')

	r1, r2 = f1.getframerate(), f2.getframerate()
	if r1 != r2:
		print("Error: frame rates must be the same!")
		sys.exit(1)

	f3 = wave.open(c, 'w')
	f3.setnchannels(chann)
	f3.setsampwidth(2)
	f3.setframerate(r1)
	f3.setcomptype('NONE', 'Not Compressed')
	frames = min(f1.getnframes(), f2.getnframes())

	print("Mixing files, total length %.2f s..." % (frames / float(r1)))
	d1 = f1.readframes(frames)
	d2 = f2.readframes(frames)
	for n in range(frames):
		if not n % (5 * r1): print(n // r1, 's')
		if chann < 2:
			d3 = struct.pack('h', int(
				.5 * (struct.unpack('h', d1[2*n:2*n+2])[0] +
				struct.unpack('h', d2[2*n:2*n+2])[0])))
		else:
			d3 = ( struct.pack('h', int(
				phase * .3 * struct.unpack('h', d1[2*n:2*n+2])[0] +
				.7 * struct.unpack('h', d2[2*n:2*n+2])[0])) +
				struct.pack('h', int(
				.7 * struct.unpack('h', d1[2*n:2*n+2])[0] +
				phase * .3 * struct.unpack('h', d2[2*n:2*n+2])[0])) )
		f3.writeframesraw(d3)
	f3.close()

if __name__ == '__main__':
	if len(sys.argv) == 4:
		a, b, c = sys.argv[1:]
		print("Mixing %s and %s, output will be %s" % (a, b, c))
		mix_files(a, b, c)

