class electre_tri:

    def __init__(self, criteria, actions, pt, profiles, lbda):
        self.criteria = criteria
        self.actions = actions
        self.pt = pt
        self.profiles = profiles
        self.lbda = lbda

    def __partial_concordance(self, x, y, c, q, p):
        # compute g_j(b) - g_j(a)
        diff = (y.performances[c.id]-x.performances[c.id])*c.direction

        # compute c_j(a, b)
        if diff > p.performances[c.id]:
            return 0
        elif diff <= q.performances[c.id]:
            return 1
        else:
            num = float(p.performances[c.id]-diff)
            den = float(p.performances[c.id]-q.performances[c.id])
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
        diff = (y.performances[c.id]-x.performances[c.id])*c.direction

        # compute d_j(a,b)
        if v.performances.has_key(c.id) is False:
            return 0
        elif diff > v.performances[c.id]:
            return 1
        elif diff <= p.performances[c.id]:
            return 0
        else:
            num = float(v.performances[c.id]-diff)
            den = float(v.performances[c.id]-p.performances[c.id])
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

    def __outrank(self, action_perfs, criteria, profile, lbda):
        q = profile.indifference
        p = profile.preference
        v = profile.veto

        s_ab = self.__credibility(action_perfs, profile, criteria, q, p, v)
        s_ba = self.__credibility(profile, action_perfs, criteria, q, p, v)

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
        for action_perfs in self.pt:
            category = nprofiles
            for profile in profiles:
                outr = self.__outrank(action_perfs, self.criteria, profile, self.lbda)
                if outr != "S" and outr != "I":
                    category -= 1

            affectations[action_perfs.alternative_id] = category

        return affectations

    def optimist(self):
        profiles = self.profiles
        affectations = {}
        for action_perfs in self.pt:
            category = 1
            for profile in profiles:
                outr = self.__outrank(action_perfs, self.criteria, profile, self.lbda)
                if outr != "-":
                    category += 1

            affectations[action_perfs.alternative_id] = category

        return affectations
