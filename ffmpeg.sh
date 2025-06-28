#!/bin/bash

# Concatenate all MP3s 10x to make them reach 1+ hour
for i in {1..10}
do
  cat 1.mp3 2.mp3 3.mp3 4.mp3 5.mp3 >> combined.mp3
done

# Stitch the artwork + audio into video
ffmpeg -loop 1 -i artwork.jpg -i combined.mp3 -c:v libx264 -c:a aac -b:a 192k \
       -pix_fmt yuv420p -shortest -t 3600 output.mp4
