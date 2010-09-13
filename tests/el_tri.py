#!/usr/bin/python

# Result should be:
# ELECTRE TRI - Pessimist
# [2, 1, 2, 3, 1, 2, 2]
# ELECTRE TRI - Optimist
# [2, 3, 2, 3, 2, 2, 2]

import sys
sys.path.append("..")
from etri import *

# Criterias
criterias = ['prix', 'transport', 'envir', 'residents', 'competitions']

# Weights
w = [25, 45, 10, 12, 8]

# Actions
a1 = [-120,  -284, 5, 3.5, 18]
a2 = [-150,  -269, 2, 4.5, 24]
a3 = [-100,  -413, 4, 5.5, 17]
a4 = [ -60,  -596, 6, 8.0, 20]
a5 = [ -30, -1321, 8, 7.5, 16]
a6 = [ -80,  -734, 5, 4.0, 21]
a7 = [ -45,  -982, 7, 8.5, 13]
a = {'a1': a1, 'a2': a2, 'a3': a3, 'a4': a4, 'a5': a5, 'a6': a6, 'a7': a7}

# Reference actions
b1 = [-100, -1000, 4, 4, 15]
b2 = [ -50,  -500, 7, 7, 20]
b = [b1, b2]

# Indifference, Preference and Veto
q = [15,   80, 1, 0.5, 1]
p = [40,  350, 3, 3.5, 5]
v = [100, 850, 5, 4.5, 8]

prof1 = { 'refs': b1, 'q': q, 'p': p, 'v': v }
prof2 = { 'refs': b2, 'q': q, 'p': p, 'v': v }
profiles = [ prof1, prof2 ]

# Lambda
lbda = 0.75

etri = electre_tri(a, profiles, w, lbda)
print "ELECTRE TRI - Pessimist"
print etri.pessimist()
print "ELECTRE TRI - Optimist"
print etri.optimist()
