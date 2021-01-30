#!/bin/bash

# Script to convert maps over time into to a gif.
# Example: ./makegif.sh map-20210130-150452-*.png

if [ "$#" -lt 1 ]; then
    echo "Usage: ./makegif files"
    exit
fi

convert -delay 50 -loop 0 "$@" animation.gif
