#!/usr/bin/python

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
a = [a1, a2, a3, a4, a5, a6, a7]

# Reference actions
b1 = [-100, -1000, 4, 4, 15]
b2 = [ -50,  -500, 7, 7, 20]
b = [b1, b2]

# Indifference, Preference and Veto
q = [15,   80, 1, 0.5, 1]
p = [40,  350, 3, 3.5, 5]
v = [100, 850, 5, 4.5, 8]

# Vector A (1xN) - Vector B (1xN)
def v_substract(a, b):
	return [a - b for a, b in zip(a, b)]

def v_multiply(a, b):
	return [a * b for a, b in zip(a, b)]

def partial_concordance(a, b):
	# compute g_j(b) - g_j(a)
	diff = v_substract(b, a)

	# compute c_j(a, b)
	c = []
	for i in range(len(diff)):
		if diff[i] > p[i]:
			c.append(0)
		elif diff[i] <= q[i]:
			c.append(1)
		else:
			num = float(p[i]-diff[i])
			den = float(p[i]-q[i])
			c.append(num/den)
	
	return c

def concordance(a, b):
	cj = partial_concordance(a, b)
	pjcj = float(sum(v_multiply(w, cj)))
	wsum = float(sum(w))
	return pjcj/wsum

def partial_discordance(a, b):
	# compute g_j(b) - g_j(a)
	diff = v_substract(b, a)

	# compute d_j(a,b)
	d = []
	for i in range(len(diff)):
		if diff[i] > v[i]:
			d.append(1)
		elif diff[i] <= p[i]:
			d.append(0)
		else:
			num = float(v[i]-diff[i])
			den = float(v[i]-p[i])
			d.append(1-num/den)

	return d

def credibility(a, b):
	dj = partial_discordance(a, b)
	C = concordance(a, b)

	sigma = C
	for disc in dj:
		if disc > C:
			num = float(1-disc)
			den = float(1-C)
			sigma = sigma*num/den

	return sigma

def outrank(action, profil, lbda):
	s_ab = credibility(action, profil)
	s_ba = credibility(profil, action)

	if s_ab >= lbda:
		if s_ba >= lbda:
			return "I"
		else:
			return "S"
	else:
		if s_ba >= lbda:
			return "-"
		else:
			return "R"

def etri_p(actions, profils, lbda):
	profils.reverse()
	nprofils = len(profils)+1
	affectations = []
	for action in actions:
		category = nprofils 
		for profil in profils:
			outr = outrank(action, profil, lbda)
			if outr != "S" and outr != "I":
				category -= 1

		affectations.append(category)

	return affectations

def etri_o(actions, profils, lbda):
	affectations = []

	for action in actions:
		category = 1
		for profil in profils:
			outr = outrank(action, profil, lbda)
			if outr != "-":
				category += 1

		affectations.append(category)

	return affectations

print "ELECTRE TRI - Pessimist"
print etri_p(a, b, 0.75)
print "ELECTRE TRI - Optimist"
print etri_o(a, b, 0.75)
