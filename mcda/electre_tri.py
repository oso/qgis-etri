from mcda.types import alternative_affectation, alternatives_affectations

class electre_tri:

    def __init__(self, criteria, pt, profiles, lbda):
        self.criteria = criteria
        self.pt = pt
        self.profiles = profiles
        self.lbda = lbda

    def __get_threshold_by_profile(self, c, threshold_id, profile_number):
        threshid = "%s%s" % (threshold_id, profile_number)
        if c.thresholds.has_threshold(threshid):
            return c.thresholds(threshid).values.value
        elif c.thresholds.has_threshold(threshold_id):
            return c.thresholds(threshold_id).values.value
        else:
            return None

    def __partial_concordance(self, x, y, c, profile_number):
        # compute g_j(b) - g_j(a)
        diff = (y.performances[c.id]-x.performances[c.id])*c.direction

        # compute c_j(a, b)
        p = self.__get_threshold_by_profile(c, 'p', profile_number)
        q = self.__get_threshold_by_profile(c, 'q', profile_number)
        if diff > p:
            return 0
        elif diff <= q:
            return 1
        else:
            num = float(p-diff)
            den = float(p-q)
            return num/den

    def __concordance(self, x, y, clist, profile_number):
        wsum = 0
        pjcj = 0
        for c in clist:
            if c.disabled == 1:
                continue

            cj = self.__partial_concordance(x, y, c, profile_number)
            wcj = c.weight*cj

            pjcj += wcj
            wsum += c.weight 

        return pjcj/wsum

    def __partial_discordance(self, x, y, c, profile_number):
        # compute g_j(b) - g_j(a)
        diff = (y.performances[c.id]-x.performances[c.id])*c.direction

        # compute d_j(a,b)
        p = self.__get_threshold_by_profile(c, 'p', profile_number)
        v = self.__get_threshold_by_profile(c, 'v', profile_number)
        if v is None:
            return 0
        elif diff > v:
            return 1
        elif diff <= p:
            return 0
        else:
            num = float(v-diff)
            den = float(v-p)
            return num/den

    def __credibility(self, x, y, clist, profile_number):
        concordance = self.__concordance(x, y, clist, profile_number)

        sigma = concordance
        for c in clist:
            if c.disabled == 1:
                continue

            dj = self.__partial_discordance(x, y, c, profile_number)
            if dj > concordance:
                num = float(1-dj)
                den = float(1-concordance)
                sigma = sigma*num/den

        return sigma

    def __outrank(self, action_perfs, criteria, profile, profile_number, lbda):
        s_ab = self.__credibility(action_perfs, profile, criteria, profile_number)
        s_ba = self.__credibility(profile, action_perfs, criteria, profile_number)

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
        affectations = alternatives_affectations([])
        for action_perfs in self.pt:
            category = nprofiles
            for i, profile in enumerate(profiles):
                outr = self.__outrank(action_perfs, self.criteria, profile, i+1, self.lbda)
                if outr != "S" and outr != "I":
                    category -= 1

            alternative_id = action_perfs.alternative_id
            alt_affect = alternative_affectation(alternative_id, category)
            affectations.append(alt_affect)

        return affectations

    def optimist(self):
        profiles = self.profiles
        affectations = alternatives_affectations([])
        for action_perfs in self.pt:
            category = 1
            for i, profile in enumerate(profiles):
                outr = self.__outrank(action_perfs, self.criteria, profile, i+1, self.lbda)
                if outr != "-":
                    category += 1

            alternative_id = action_perfs.alternative_id
            alt_affect = alternative_affectation(alternative_id, category)
            affectations.append(alt_affect)

        return affectations
