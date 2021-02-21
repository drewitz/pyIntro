#!/usr/bin/env python3

# Hello and welcome to this example file
# Everything appearing after the octothorp (or hashtag sign #) in a line is a
# comment and is ignored by python. Comments are more important than you think.
# If you ever come back to a file not remembering what you did there, you will
# be happy about every single comment. Trust me.

# The very first line in this file can be ignored by most people. It's a useful
# little thing called a "shebang" telling a UNIX operating system what
# programme to use to execute the file. If you use UNIX (e.g. Linux, a BSD
# distribution, or macOS), just google the name or ask me. If not, there's no
# harm in not using it.

# This file plots the numbers of the world population between 1950 and 2020.
# It's supposed to be an illustrative example.

# The three lines starting with "import" load modules which include necessary
# functionalities to the code.
#  - numpy (numerical python) includes important mathematical functions and
#    capabilities to calculate with arrays. It's not necessary here, but one
#    could use it and it will be important in almost all the files we will
#    create.
#  - matplotlib.pyplot includes the methods to plot functions
#  - pandas is a module that helps working with datasets. It's not completely
#    necessary to do what we want to do here. However, if one includes the data
#    from a csv file as I do here.

# import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys

########################################
# load the data
########################################

if len(sys.argv) != 3:
    sys.exit("Please invoke with two arguments: input and output paths\n"+
            "suggested input: ../data/worlddata.csv\n"+
            "output should be pdf")

inputfile = sys.argv[1]
outputfile = sys.argv[2]
# data taken from
# https://www.worldometers.info/world-population/world-population-by-year/
popsize = pd.read_csv(inputfile)

x = popsize["year"]
y = popsize["world population"]


########################################
# plot the data
########################################

fig, axs = plt.subplots(1, 2)
axs[0].plot(x, y)

# now change the scale
axs[1].plot(x, y)
plt.yscale("log")

plt.savefig(outputfile)
