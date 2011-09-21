class criterion:

    DISABLED = 1
    ENABLED = 0

    def __init__(self, id, name=None, disabled=None, direction=None,
                 weight=None):
        self.id = id
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
        return "[%s]%s: %g" % (self.id, self.name,
                               int(self.direction)*float(self.weight))

class action:

    def __init__(self, id=None, name=None, evaluations=None):
        self.id = id
        self.name = name
        self.evaluations = evaluations

    def __repr__(self):
        return "[%s]%s" % (self.id, self.name)

class profile(action):
    pass

class threshold(action):
    pass
