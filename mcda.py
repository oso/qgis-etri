class criterion:

    DISABLED = 1
    ENABLED = 0

    def __init__(self, id, name=None, disabled=None, direction=None,
                 weight=None):
        self.id = id
        self.name = name
        self.disabled = disabled
        self.direction = direction
        self.weight = weight
