from utils import v_multiply,v_substract

class electre_tri:

    def __init__(self, actions, profiles, weights, lbda):
        self.actions = actions
        self.profiles = profiles
        self.weights = weights
        self.lbda = lbda

    def partial_concordance(self, x, y, q, p):
        # compute g_j(b) - g_j(a)
        diff = v_substract(y, x)

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

    def concordance(self, x, y, q, p, w):
        cj = self.partial_concordance(x, y, q, p)
        pjcj = float(sum(v_multiply(w, cj)))
        wsum = float(sum(w))
        return pjcj/wsum

    def partial_discordance(self, x, y, p, v):
        # compute g_j(b) - g_j(a)
        diff = v_substract(y, x)

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

    def credibility(self, x, y, q, p, v, w):
        dj = self.partial_discordance(x, y, p, v)
        C = self.concordance(x, y, q, p, w)

        sigma = C
        for disc in dj:
            if disc > C:
                num = float(1-disc)
                den = float(1-C)
                sigma = sigma*num/den

        return sigma
    
    def outrank(self, action, profil, weights, lbda):
        s_ab = self.credibility(action, profil['refs'], profil['q'], profil['p'], profil['v'], weights)
        s_ba = self.credibility(profil['refs'], action, profil['q'], profil['p'], profil['v'], weights)

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
        profils = self.profiles
        profils.reverse()
        nprofils = len(profils)+1
        affectations = []
        for action in self.actions:
            category = nprofils 
            for profil in profils:
                outr = self.outrank(action, profil, self.weights, self.lbda)
                if outr != "S" and outr != "I":
                    category -= 1
    
            affectations.append(category)
    
        return affectations
    
    def optimist(self):
        profils = self.profiles
        affectations = []
        for action in self.actions:
            category = 1
            for profil in profils:
                outr = self.outrank(action, profil, self.weights, self.lbda)
                if outr != "-":
                    category += 1
    
            affectations.append(category)
    
        return affectations
