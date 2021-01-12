#!/usr/bin/env python3

import termcolor
import argparse, sys
import re
import os

parser = argparse.ArgumentParser(description = "Take hostnames on stdin and return IPs.")
parser.add_argument('-f', '--foreground', default=None, help="Set the foreground color for matching lines.")
parser.add_argument('-b', '--background', default=None, help="Set the background color for matching lines.")
parser.add_argument('-p', '--pattern', help="We highlight lines that match this regex pattern")
parser.add_argument('--colors', default=False, action="store_true", help="Show a list of valid colors")

args = parser.parse_args()

foreground = args.foreground
background = args.background
pattern = args.pattern

if args.colors:
	colors = [x for x in termcolor.COLORS.keys()]
	print ("colors: ", ", ".join(colors))
	exit()

term_width, z = os.get_terminal_size()

# compile pattern param into a regex pattern object
try:
	p = re.compile(pattern)
except:
	print("Supplied pattern is not valid regex")
	exit(1)

for line in sys.stdin:
	line = line.rstrip() # remove crlf
	if p.search(line):
		line = line.replace("\t", "    ") # replace tabs with spaces so termcolor will color them.
		line = line+" "*(term_width-len(line)) # highlight to the end of the line.
		print(termcolor.colored(line, foreground, f"on_{background}"))
	else:
		print(line)
