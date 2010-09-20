#!/usr/bin/python

# Result should be:
# ELECTRE TRI - Pessimist
# [2, 1, 2, 3, 1, 2, 2]
# ELECTRE TRI - Optimist
# [2, 3, 2, 3, 2, 2, 2]

import sys
sys.path.append("..")
from etri import *

# Criterions
criterions = ['prix', 'transport', 'envir', 'residents', 'competition']

# Weights
w = {'prix': 25, 'transport': 45, 'envir': 10, 'residents': 12, 'competition': 8}

# Actions
a1 = {'prix': -120, 'transport':  -284, 'envir': 5, 'residents': 3.5, 'competition': 18}
a2 = {'prix': -150, 'transport':  -269, 'envir': 2, 'residents': 4.5, 'competition': 24}
a3 = {'prix': -100, 'transport':  -413, 'envir': 4, 'residents': 5.5, 'competition': 17}
a4 = {'prix':  -60, 'transport':  -596, 'envir': 6, 'residents': 8.0, 'competition': 20}
a5 = {'prix':  -30, 'transport': -1321, 'envir': 8, 'residents': 7.5, 'competition': 16}
a6 = {'prix':  -80, 'transport':  -734, 'envir': 5, 'residents': 4.0, 'competition': 21}
a7 = {'prix':  -45, 'transport':  -982, 'envir': 7, 'residents': 8.5, 'competition': 13}
a = {'a1': a1, 'a2': a2, 'a3': a3, 'a4': a4, 'a5': a5, 'a6': a6, 'a7': a7}

# Reference actions
b1 = {'prix': -100, 'transport': -1000, 'envir': 4, 'residents': 4, 'competition': 15}
b2 = {'prix':  -50, 'transport':  -500, 'envir': 7, 'residents': 7, 'competition': 20}
b = [b1, b2]

# Indifference, Preference and Veto
q = {'prix': 15,  'transport':  80, 'envir': 1, 'residents': 0.5, 'competition': 1}
p = {'prix': 40,  'transport': 350, 'envir': 3, 'residents': 3.5, 'competition': 5}
v = {'prix': 100, 'transport': 850, 'envir': 5, 'residents': 4.5, 'competition': 8}

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

etri.print_concordance_table()
etri.print_credibility_table()
