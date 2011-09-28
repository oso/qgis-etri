from xmcda import xmcda_utils

class criterion(xmcda_utils):

    DISABLED = 1
    ENABLED = 0

    def __init__(self, id, name=None, disabled=None, direction=None,
                 weight=None):
        self.id = id
        if name == None:
            self.name = str(id)
        self.name = name
        if disabled == None:
            disabled = 0
        self.disabled = disabled
        if direction == None:
            direction = 1
        self.direction = direction
        if weight == None:
            weight = 10
        self.weight = weight

    def __repr__(self):
        return "C_%s: %g" % (self.name,
                             int(self.direction)*float(self.weight))

    def to_xmcda(self):
        output = "<criterion id='%s' name='%s'>" % (self.id, self.name)

        if self.disabled == 0:
            output += "<active>true</active>"
        else:
            output += "<active>false</active>"

        output += "<scale><quantitative>"
        if self.direction == 1:
            output += "<preferenceDirection>max</preferenceDirection>"
        else:
            output += "<preferenceDirection>min</preferenceDirection>"
        output += "</quantitative></scale>"

        output += "<criterionValue>"
        output += self.set_value(self.weight) 
        output += "</criterionValue>"

        output += "</criterion>"

        return output

class action:

    def __init__(self, id=None, name=None, evaluations=None):
        self.id = id
        if name == None:
            self.name = str(id)
        else:
            self.name = name
        self.evaluations = evaluations

    def __repr__(self):
        return "A_%s: %s" % (self.name, self.evaluations)

    def __add__(self, other):
        a = self.evaluations
        b = other.evaluations
        return dict( (n, a.get(n, 0)+b.get(n, 0)) for n in set(a)|set(b) )

    def __sub__(self, other):
        a = self.evaluations
        b = other.evaluations
        return dict( (n, a.get(n, 0)-b.get(n, 0)) for n in set(a)|set(b) )

class threshold(action):
    pass

class profile(action):

    def __init__(self, id=None, name=None, evaluations=None,
                 indifference=None, preference=None, veto=None):
        action.__init__(self, id, name, evaluations)
        self.indifference = indifference
        self.preference = preference
        self.veto = veto
