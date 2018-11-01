#!/bin/bash

# Example script for the Othello assignment. Don't forget to make it executable (chmod +x othello)
# Change the last line (python3 Othello.py ...) if you are using python2 
#
# usage: bash othello <position> <time_limit>
#
# Author: Ola Ringdahl

# Change directory to the location of your program  
# $(dirname "$0") is the path to where this script is located (don't change this)
cd "$(dirname "$0")"

# Call your Python program ($1 and $2 are the input parameters):
python3 Othello.py $1 $2

