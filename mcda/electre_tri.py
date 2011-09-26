import sys
sys.path.insert(0, "..")
from mcda.types import criterion, action, profile

class electre_tri:

    def __init__(self, actions, criteria, profiles, lbda):
        self.criteria = criteria
        self.actions = actions
        self.profiles = profiles
        self.lbda = lbda

    def __partial_concordance(self, x, y, c, q, p):
        # compute g_j(b) - g_j(a)
        diff = (y.evaluations[c]-x.evaluations[c])*c.direction

        # compute c_j(a, b)
        if diff > p.evaluations[c]:
            return 0
        elif diff <= q.evaluations[c]:
            return 1
        else:
            num = float(p.evaluations[c]-diff)
            den = float(p.evaluations[c]-q.evaluations[c])
            return num/den

    def __concordance(self, x, y, clist, q, p):
        wsum = 0
        pjcj = 0
        for c in clist:
            if c.disabled == 1:
                continue

            cj = self.__partial_concordance(x, y, c, q, p)
            wcj = c.weight*cj

            pjcj += wcj
            wsum += c.weight 

        return pjcj/wsum

    def __partial_discordance(self, x, y, c, p, v):
        # compute g_j(b) - g_j(a)
        diff = (y.evaluations[c]-x.evaluations[c])*c.direction

        # compute d_j(a,b)
        if v.evaluations.has_key(c) == False:
            return 0
        elif diff > v.evaluations[c]:
            return 1
        elif diff <= p.evaluations[c]:
            return 0
        else:
            num = float(v.evaluations[c]-diff)
            den = float(v.evaluations[c]-p.evaluations[c])
            return num/den

    def __credibility(self, x, y, clist, q, p, v):
        concordance = self.__concordance(x, y, clist, q, p)

        sigma = concordance
        for c in clist:
            if c.disabled == 1:
                continue

            dj = self.__partial_discordance(x, y, c, p, v)
            if dj > concordance:
                num = float(1-dj)
                den = float(1-concordance)
                sigma = sigma*num/den

        return sigma

    def __outrank(self, action, criteria, profile, lbda):
        q = profile.indifference
        p = profile.preference
        v = profile.veto

        s_ab = self.__credibility(action, profile, criteria, q, p, v)
        s_ba = self.__credibility(profile, action, criteria, q, p, v)

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
        profiles = self.profiles[:]
        profiles.reverse()
        nprofiles = len(profiles)+1
        affectations = {}
        for action in self.actions:
            category = nprofiles
            for profile in profiles:
                outr = self.__outrank(action, self.criteria, profile, self.lbda)
                if outr != "S" and outr != "I":
                    category -= 1

            affectations[action] = category

        return affectations

    def optimist(self):
        profiles = self.profiles
        affectations = {}
        for action in self.actions:
            category = 1
            for profile in profiles:
                outr = self.__outrank(action, self.criteria, profile, self.lbda)
                if outr != "-":
                    category += 1

            affectations[action] = category

        return affectations
