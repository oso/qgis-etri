from utils import v_multiply,v_substract

def d_add(a, b):
    return dict( (n, a.get(n, 0)+b.get(n, 0)) for n in set(a)|set(b) )

def d_substract(a, b):
    return dict( (n, a.get(n, 0)-b.get(n, 0)) for n in set(a)|set(b) )

def d_multiply(a, b):
    return dict( (n, a.get(n, 0)*b.get(n, 0)) for n in set(a)|set(b) )

class electre_tri:

    def __init__(self, actions, profiles, weights, lbda):
        self.actions = actions
        self.profiles = profiles
        self.weights = weights
        self.lbda = lbda

    def partial_concordance(self, x, y, q, p):
        # compute g_j(b) - g_j(a)
        diff = d_substract(y, x)

        # compute c_j(a, b)
        c = {}
        for key, value in diff.iteritems():
            if value > p[key]:
                c[key] = 0
            elif value <= q[key]:
                c[key] = 1
            else:
                num = float(p[key]-diff[key])
                den = float(p[key]-q[key])
                c[key] = num/den

        return c

    def concordance(self, x, y, q, p, w):
        cj = self.partial_concordance(x, y, q, p)
        wcj = d_multiply(w, cj)
        pjcj = float(sum([i for i in wcj.values()]))
        wsum = float(sum([i for i in w.values()]))
        return pjcj/wsum

    def partial_discordance(self, x, y, p, v):
        # compute g_j(b) - g_j(a)
        diff = d_substract(y, x)

        # compute d_j(a,b)
        d = {}
        for key, value in diff.iteritems():
             if value > v[key]:
                d[key] = 1
             elif value <= p[key]:
                d[key] = 0
             else:
                num = float(v[key]-value)
                den = float(v[key]-p[key])
                d[key] = 1-num/den

        return d

    def credibility(self, x, y, q, p, v, w):
        dj = self.partial_discordance(x, y, p, v)
        C = self.concordance(x, y, q, p, w)

        sigma = C
        for key, value in dj.iteritems():
            if value > C:
                num = float(1-value)
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
        affectations = {}
        for action, evals in self.actions.iteritems():
            category = nprofils 
            for profil in profils:
                outr = self.outrank(evals, profil, self.weights, self.lbda)
                if outr != "S" and outr != "I":
                    category -= 1
    
            affectations[action] = category

        return affectations
    
    def optimist(self):
        profils = self.profiles
        affectations = {}
        for action, evals in self.actions.iteritems():
            category = 1
            for profil in profils:
                outr = self.outrank(evals, profil, self.weights, self.lbda)
                if outr != "-":
                    category += 1

            affectations[action] = category

        return affectations
