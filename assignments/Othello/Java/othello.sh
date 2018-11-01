#!/bin/bash

# Example script for the Othello assignment. Don't forget to make it executable (chmod +x othello)
# Change the last line (java Othello ...) to suit your needs
#
# usage: bash othello <position> <time_limit>
#
# Author: Ola Ringdahl

# Change directory to the location of your program 
# $(dirname "$0") is the path to where this script is located (don't change this) 
cd "$(dirname "$0")"

# Compile the code:
javac *.java

# Call your Java program ($1 and $2 are the input parameters):
java Othello $1 $2

