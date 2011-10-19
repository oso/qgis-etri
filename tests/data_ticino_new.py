#!/usr/bin/python
import sys
sys.path.insert(0, "..")
from mcda.types import criterion, criteria, action, actions, profile, threshold, alternative_performances, performance_table

# Criteria
prix = criterion('prix', 'prix', 0, -1, 25)
transport = criterion('transport', 'transport', 0, -1, 45)
envir = criterion('envir', 'environment', 0, 1, 10)
residents = criterion('residents', 'residents', 0, 1, 12)
competition = criterion('competition', 'competition', 0, 1, 8)
c = criteria([ prix, transport, envir, residents, competition ])

# Actions
a1 = action('a1', 'a1')
a2 = action('a2', 'a2')
a3 = action('a3', 'a3')
a4 = action('a4', 'a4')
a5 = action('a5', 'a5')
a6 = action('a6', 'a6')
a7 = action('a7', 'a7')
a = actions([ a1, a2, a3, a4, a5, a6, a7 ])

# Performance table
p1 = alternative_performances(a1, {prix: 120, transport:  284, envir: 5, residents: 3.5, competition: 18})
p2 = alternative_performances(a2, {prix: 150, transport:  269, envir: 2, residents: 4.5, competition: 24})
p3 = alternative_performances(a3, {prix: 100, transport:  413, envir: 4, residents: 5.5, competition: 17})
p4 = alternative_performances(a4, {prix:  60, transport:  596, envir: 6, residents: 8.0, competition: 20})
p5 = alternative_performances(a5, {prix:  30, transport: 1321, envir: 8, residents: 7.5, competition: 16})
p6 = alternative_performances(a6, {prix:  80, transport:  734, envir: 5, residents: 4.0, competition: 21})
p7 = alternative_performances(a7, {prix:  45, transport:  982, envir: 7, residents: 8.5, competition: 13})
pt = performance_table([ p1, p2, p3, p4, p5, p6, p7 ])

# Reference actions
b1 = {prix: 100, transport: 1000, envir: 4, residents: 4, competition: 15}
b2 = {prix:  50, transport:  500, envir: 7, residents: 7, competition: 20}

# Indifference, Preference and Veto
q = threshold('q', 'indifference',  {prix: 15,  transport:  80, envir: 1, residents: 0.5, competition: 1})
p = threshold('p', 'preference', {prix: 40, transport: 350, envir: 3, residents: 3.5, competition: 5})
v = threshold('v', 'veto', {prix: 100, transport: 850, envir: 5, residents: 4.5, competition: 8})

# Profiles
prof1 = profile('p1', 'profile_down', b1, q, p, v)
prof2 = profile('p2', 'profile_up', b2, q, p, v)
profiles = [ prof1, prof2 ]

# Affecations
affect_p = {a1: 2, a2: 1, a3: 2, a4: 3, a5: 1, a6: 2, a7:2}
affect_o = {a1: 2, a2: 3, a3: 2, a4: 3, a5: 2, a6: 2, a7:2}

# Lambda
lbda = 0.75
