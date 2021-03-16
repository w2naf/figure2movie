#!/usr/bin/env python
import sys
import os
import glob
from subprocess import call

# Name of the output file.
outFile = 'movie.mp4'

# Remove the old output file if it already exists.
try:
  os.remove(outFile)
except:
  pass

# Remove old symbolic links if they already exist.
def cleanHouse():
  oldFiles = glob.glob('*-symlink*')
  if len(oldFiles) > 0:
    for file in oldFiles: os.remove(file)
cleanHouse()

# Find all of the PNGs in the folder that will be made into 
if len(sys.argv) == 1:
  files = glob.glob('*.png')
else:
  files = sys.argv[1:-1]

# Sort the images in order.
files.sort()

inx=0
for ff in files:
  path,ext = os.path.splitext(ff)
  if ext.lower() != '.png':
    call("convert -verbose -density 400 +matte "+ff+" "+path+".png",shell=True)
    ff = path+'.png'
  newName = ('%06d' % inx) +'-symlink.png'
  inx = inx + 1
  os.symlink(ff,newName)
  print(ff + ' --> ' + newName)

#call("avconv -qscale 10 -r 10 -b 9600 -i %06d-symlink.png "+outFile,shell=True)
#call("ffmpeg -i %06d-symlink.png -r 10 -b 20000 -qscale 10 "+outFile,shell=True)
# Actually create the movie.
call("ffmpeg -framerate 6 -i %06d-symlink.png -s:v 1280x720 -c:v libx264 \
        -profile:v high -crf 20 -pix_fmt yuv420p "+outFile,shell=True)
#call("avconv -mbd rd -flags +mv4+aic -trellis 2 -cmp 2 -subcmp 2 -g 300 -qscale 4 -pass 1 -strict experimental -i %06d-symlink.png "+outFile,shell=True)

cleanHouse()
