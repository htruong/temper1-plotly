#!/bin/bash

# whatever you have to do to get the temperature...
tempered $(tempered -e | cut -f1 -d' ') | cut -d" " -f4 | tr -d '\n'
