#FIXME: put these 4 functions in another place
def d_add(a, b):
    return dict( (n, a.get(n, 0)+b.get(n, 0)) for n in set(a)|set(b) )

def d_substract(a, b):
    return dict( (n, a.get(n, 0)-b.get(n, 0)) for n in set(a)|set(b) )

def d_multiply(a, b):
    return dict( (n, a.get(n, 0)*b.get(n, 0)) for n in set(a)|set(b) )

def d_divide(a, b):
    return dict( (n, a.get(n, 0)/b.get(n, 0)) for n in set(a)|set(b) )

class electre_tri:

    def __init__(self, actions, profiles, weights, lbda, directions=None, criteria=None):
        self.actions = actions
        self.profiles = profiles
        self.weights = weights
        self.lbda = lbda
        self.directions = directions
        if criteria == None:
            self.criteria = weights.keys()
        else:
            self.criteria = criteria

    def get_model_min(self):
        actions = self.update_actions(self.actions, self.directions)
        profiles = self.update_profiles(self.profiles, self.directions)

        minima = {}
        for action, evals in actions.iteritems():
            for crit, value in evals.iteritems():
                if minima.has_key(crit) == False:
                    minima[crit] = value

                if minima[crit] > value:
                    minima[crit] = value

        for profile in profiles:
            prof = profile['refs']
            for crit, value in profile['refs'].iteritems():
                if minima[crit] > value:
                    minima[crit] = value

        if self.directions <> None:
            minima = d_multiply(minima, self.directions)

        return minima

    def get_model_max(self):
        actions = self.update_actions(self.actions, self.directions)
        profiles = self.update_profiles(self.profiles, self.directions)

        maxima = {}
        for action, evals in actions.iteritems():
            for crit, value in evals.iteritems():
                if maxima.has_key(crit) == False:
                    maxima[crit] = value

                if maxima[crit] < value:
                    maxima[crit] = value

        for profile in profiles:
            prof = profile['refs']
            for crit, value in profile['refs'].iteritems():
                if maxima[crit] < value:
                    maxima[crit] = value

        if self.directions <> None:
            maxima = d_multiply(maxima, self.directions)

        return maxima

    def update_actions(self, actions, directions):
        if directions == None:
            return actions.copy()

        a = {}
        for action, evals in actions.iteritems():
            a[action] = d_multiply(evals, directions)

        return a

    def update_profiles(self, profiles, directions):
        if directions == None:
            return profiles[:]

        p = [ profile.copy() for profile in profiles ]

        for profile in p:
            profile['refs'] = d_multiply(profile['refs'], directions)

        return p

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
            if v.has_key(key) == False:
                d[key] = 0
            elif value > v[key]:
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
    
    def outrank(self, action, profile, weights, lbda):
        s_ab = self.credibility(action, profile['refs'], profile['q'], profile['p'], profile['v'], weights)
        s_ba = self.credibility(profile['refs'], action, profile['q'], profile['p'], profile['v'], weights)

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
        actions = self.update_actions(self.actions, self.directions)
        profiles = self.update_profiles(self.profiles, self.directions)
        profiles.reverse()
        nprofiles = len(profiles)+1
        affectations = {}
        for action, evals in actions.iteritems():
            category = nprofiles
            for profile in profiles:
                outr = self.outrank(evals, profile, self.weights, self.lbda)
                if outr != "S" and outr != "I":
                    category -= 1
    
            affectations[action] = category

        return affectations
    
    def optimist(self):
        actions = self.update_actions(self.actions, self.directions)
        profiles = self.update_profiles(self.profiles, self.directions)
        affectations = {}
        for action, evals in actions.iteritems():
            category = 1
            for profile in profiles:
                outr = self.outrank(evals, profile, self.weights, self.lbda)
                if outr != "-":
                    category += 1

            affectations[action] = category

        return affectations

    def print_concordance_table(self):
        actions = self.update_actions(self.actions, self.directions)
        profiles = self.update_profiles(self.profiles, self.directions)

        print 'Concordance Table'
        print '================='
        prtstr = 'ACTION' + ' ' * (16-len('ACTION'))
        for i in range(1, len(profiles)+1):
            prtstr2 = 'ai,b%d' % i
            prtstr +=  prtstr2
            prtstr += ' ' * (16-len(prtstr2))
            prtstr2 = 'b%d,ai' % i
            prtstr +=  prtstr2
            prtstr += ' ' * (16-len(prtstr2))

        print prtstr
        print '-' * len(prtstr)

        for action, evals in actions.iteritems():
            print '%s\t\t' % action,
            for profile in profiles:
                concordance = self.concordance(evals, profile['refs'], profile['q'], profile['p'], self.weights)
                print '%.2f\t\t' % concordance, 
                concordance = self.concordance(profile['refs'], evals, profile['q'], profile['p'], self.weights)
                print '%.2f\t\t' % concordance, 
            print ''

    def print_credibility_table(self):
        actions = self.update_actions(self.actions, self.directions)
        profiles = self.update_profiles(self.profiles, self.directions)

        print 'Credibility Table'
        print '================='
        prtstr = 'ACTION' + ' ' * (16-len('ACTION'))
        for i in range(1, len(profiles)+1):
            prtstr2 = 'ai,b%d' % i
            prtstr +=  prtstr2
            prtstr += ' ' * (16-len(prtstr2))
            prtstr2 = 'b%d,ai' % i
            prtstr +=  prtstr2
            prtstr += ' ' * (16-len(prtstr2))
        print prtstr
        print '-' * len(prtstr)

        for action, evals in actions.iteritems():
            print '%s\t\t' % action,
            for profile in profiles:
                credibility = self.credibility(evals, profile['refs'], profile['q'], profile['p'], profile['v'], self.weights)
                print '%.2f\t\t' % credibility,
                credibility = self.credibility(profile['refs'], evals, profile['q'], profile['p'], profile['v'], self.weights)
                print '%.2f\t\t' % credibility,
            print ''
