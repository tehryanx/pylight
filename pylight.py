#!/usr/bin/env python3

import termcolor                                                                                                                                      
import argparse, sys                                                                                                                                  
import re                                                                                                                                             
import os                                                                                                                                             

term_width, z = os.get_terminal_size()
colors = termcolor.COLORS.keys()

parser = argparse.ArgumentParser(description = "Highlighth lines in bash")
parser.add_argument('--colors', default=False, action="store_true", help="Show a list of valid colors")
parser.add_argument('-o', '--only', default=False, action="store_true", help="setting this will highlight only the regex match rather than the entire line.")
for color in colors:
	parser.add_argument(f"--{color}", default="", help=f"Set the highlight color to {color} for lines that match the given regex.")

patterns = vars(parser.parse_args())

only = patterns['only']
del patterns['only']

if patterns['colors']:
    print("colors: ", ", ".join(colors))                                                                                                              
	exit()
del patterns['colors']

compiled_patterns = {}

for k, p in patterns.items():
	if p:
		try:
			compiled_patterns[k] = re.compile(p)
		except:
            print(f"{p} is not valid regex")                                                                                                          
			exit()

for line in sys.stdin:
	line = line.rstrip()

	for k,p in compiled_patterns.items():
		if p.search(line):
			foreground = 'white' if k in list(colors)[:-1] else 'grey'
			line = line.replace("\t", "    ")
			line = line+" "*(term_width-len(line))
			if not only:
				line = termcolor.colored(line, foreground, f"on_{k}")
			else:
				i = re.search(p, line).start()
				l = len(re.search(p, line).group(0))
				line = line[0:i] + termcolor.colored(line[i:i+l], foreground, f"on_{k}") + line[i+l:]

    print(line)                                                                                                                                       

