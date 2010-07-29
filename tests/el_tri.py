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

# Lambda
lbda = 0.75

class electre_tri:

	def __init__(self, a, b, q, p, v, lbda):
		self.a = a
		self.b = b
		self.q = q
		self.p = p
		self.v = v
		self.lbda = lbda

	def v_substract(self, x, y):
		return [x - y for x, y in zip(x, y)]

	def v_multiply(self, x, y):
		return [x * y for x, y in zip(x, y)]

	def partial_concordance(self, x, y):
		# compute g_j(b) - g_j(a)
		diff = self.v_substract(y, x)

		# compute c_j(a, b)
		c = []
		for i in range(len(diff)):
			if diff[i] > self.p[i]:
				c.append(0)
			elif diff[i] <= self.q[i]:
				c.append(1)
			else:
				num = float(self.p[i]-diff[i])
				den = float(self.p[i]-self.q[i])
				c.append(num/den)
	
		return c

	def concordance(self, A, B):
		cj = self.partial_concordance(A, B)
		pjcj = float(sum(self.v_multiply(w, cj)))
		wsum = float(sum(w))
		return pjcj/wsum

	def partial_discordance(self, x, y):
		# compute g_j(b) - g_j(a)
		diff = self.v_substract(y, x)
	
		# compute d_j(a,b)
		d = []
		for i in range(len(diff)):
			if diff[i] > self.v[i]:
				d.append(1)
			elif diff[i] <= self.p[i]:
				d.append(0)
			else:
				num = float(self.v[i]-diff[i])
				den = float(self.v[i]-self.p[i])
				d.append(1-num/den)
	
		return d
	
	def credibility(self, x, y):
		dj = self.partial_discordance(x, y)
		C = self.concordance(x, y)
	
		sigma = C
		for disc in dj:
			if disc > C:
				num = float(1-disc)
				den = float(1-C)
				sigma = sigma*num/den
	
		return sigma
	
	def outrank(self, action, profil, lbda):
		s_ab = self.credibility(action, profil)
		s_ba = self.credibility(profil, action)
	
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
	
	def pessimist(self):
		profils = self.b
		profils.reverse()
		nprofils = len(b)+1
		affectations = []
		for action in self.a:
			category = nprofils 
			for profil in profils:
				outr = self.outrank(action, profil, self.lbda)
				if outr != "S" and outr != "I":
					category -= 1
	
			affectations.append(category)
	
		return affectations
	
	def optimist(self):
		profils = self.b
		affectations = []
		for action in self.a:
			category = 1
			for profil in profils:
				outr = self.outrank(action, profil, self.lbda)
				if outr != "-":
					category += 1
	
			affectations.append(category)
	
		return affectations

etri = electre_tri(a, b, q, p, v, lbda)
print "ELECTRE TRI - Pessimist"
print etri.pessimist()
print "ELECTRE TRI - Optimist"
print etri.optimist()
