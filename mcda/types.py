from xml.etree import ElementTree

type2tag = {
    int: 'integer',
    float: 'real'
}

unmarshallers = {
    'integer': lambda x: int(x.text),
    'real': lambda x: float(x.text),
}

def marshal(value):
    tag = type2tag.get(type(value))
    e = ElementTree.Element(tag)
    e.text = str(value)
    return e

def unmarshal(xml):
    m = unmarshallers.get(xml.tag)
    return m(xml)

class criteria(list):

    def to_xmcda(self):
        root = ElementTree.Element('criteria')
        for crit in self:
            crit_xmcda = crit.to_xmcda()
            root.append(crit_xmcda)
        return root

    def from_xmcda(self, xmcda, xmcda_critval=None):
        tag_list = xmcda.getiterator('criterion')
        for tag in tag_list:
            c = criterion(0)
            c.from_xmcda(tag)
            self.append(c)

        if xmcda_critval is not None:
            tag_list = xmcda_critval.getiterator('criterionValue')
            for tag in tag_list:
                c.from_xmcda(xmcda_critval=tag)

class criterion:

    DISABLED = 1
    ENABLED = 0

    def __init__(self, id, name=None, disabled=None, direction=None,
                 weight=None):
        self.id = id
        self.name = name
        if disabled == None:
            disabled = False
        self.disabled = disabled
        if direction == None:
            direction = 1
        self.direction = direction
        self.weight = weight

    def __repr__(self):
        if self.name is not None:
            return "%s (%s)" % (self.id, self.name)
        else:
            return "%s" % self.id

    def to_xmcda(self):
        xmcda = ElementTree.Element('criterion', id=self.id, name=self.name)

        active = ElementTree.SubElement(xmcda, 'active')
        if self.disabled == False:
            active.text = 'true'
        else:
            active.text = 'false'

        scale = ElementTree.SubElement(xmcda, 'scale')
        quant = ElementTree.SubElement(scale, 'quantitative')
        prefd = ElementTree.SubElement(quant, 'preferenceDirection')
        if self.direction == 1:
            prefd.text = 'max'
        else:
            prefd.text = 'min'

        if self.weight:
            crit_val = ElementTree.SubElement(xmcda, 'criterionValue')
            value = ElementTree.SubElement(crit_val, 'value')
            weight = marshal(self.weight)
            value.append(weight)

        return xmcda

    def from_xmcda(self, xmcda=None, xmcda_critval=None):
        if xmcda is not None:
            if xmcda.tag == 'criterion':
                crit = xmcda
            else:
                crit = xmcda.find('.//criterion')
            id = crit.get('id')
            if id is not None:
                self.id = id
            name = crit.get('name')
            if name is not None:
                self.name = name
            active = crit.find('.//active')
            if active is not None:
                if active.text == 'false':
                    self.disabled = True
                else:
                    self.disabled = False
            pdir = crit.find('.//scale/quantitative/preferenceDirection')
            if pdir is not None:
                if pdir.text == 'max':
                    self.direction = 1
                elif pdir.text == 'min':
                    self.direction = -1
                else:
                    raise TypeError, 'criterion::invalid preferenceDirection'
            value = crit.find('.//criterionValue/value')
            if value is not None:
                self.weight = unmarshal(value.getchildren()[0])

        if xmcda_critval is not None:
            if xmcda_critval.tag == 'criterionValue':
                critval = xmcda_critval
            else:
                critval = xmcda_critval.find('.//criterionValue')
            value = critval.find('.//value')
            if value is not None:
                self.weight = unmarshal(value.getchildren()[0])

class actions(list):

    def to_xmcda(self):
        root = ElementTree.Element('alternatives')
        root2 = ElementTree.Element('performanceTable')
        for action in self:
            alt, perf = action.to_xmcda()
            root.append(alt)
            root2.append(perf)
        return (root, root2)

class action:

    def __init__(self, id=None, name=None, performances=None, disabled=None):
        self.id = id
        self.name = name
        self.performances = performances
        if disabled == None:
            disabled = False
        self.disabled = disabled

    def __repr__(self):
        if self.name is not None:
            return "%s (%s)" % (self.id, self.name)
        else:
            return "%s" % self.id

    def __add__(self, other):
        a = self.performances
        b = other.performances
        return dict( (n, a.get(n, 0)+b.get(n, 0)) for n in set(a)|set(b) )

    def __sub__(self, other):
        a = self.performances
        b = other.performances
        return dict( (n, a.get(n, 0)-b.get(n, 0)) for n in set(a)|set(b) )

    def to_xmcda(self):
        xmcda = ElementTree.Element('alternative', id=self.id,
                                    name=self.name)

        active = ElementTree.SubElement(xmcda, 'active')
        if self.disabled == False:
            active.text = 'true'
        else:
            active.text = 'false'

        if self.performances:
            xmcda2 = ElementTree.Element('alternativePerformances')
            altid = ElementTree.SubElement(xmcda2, 'alternativeID')
            altid.text = self.id

            for crit, val in self.performances.iteritems():
                perf = ElementTree.SubElement(xmcda2, 'performance')

                critid = ElementTree.SubElement(perf, 'criterionID')
                critid.text = crit.id

                value = ElementTree.SubElement(perf, 'value')
                p = marshal(val)
                value.append(p)
        else:
            xmcda2 = None

        return (xmcda, xmcda2)

class performance_table(list):

    def __call__(self, alternative, criterion=None):
        for altp in self:
            if altp.alternative == alternative:
                alt_perfs = altp
                break

        if alt_perfs is None:
            raise KeyError, "Alternative %si not found" % alternative

        if criterion is None:
            return alt_perfs
        else:
            return alt_perfs(criterion)

    def has_alternative(self, alternative):
        for altp in self:
            if altp.alternative == alternative:
                return True

        return False

    def to_xmcda(self):
        root = ElementTree.Element('performanceTable')
        for alt_perfs in self:
            xmcda = alt_perfs.to_xmcda()
            root.append(xmcda)
        return root

class alternative_performances():

    def __init__(self, alternative, performances={}):
        self.alternative = alternative
        self.performances = performances

    def __call__(self, criterion):
        return self.performances[criterion]

    def to_xmcda(self):
        xmcda = ElementTree.Element('alternativePerformances')
        altid = ElementTree.SubElement(xmcda, 'alternativeID')
        altid.text = self.alternative.id 

        for crit, val in self.performances.iteritems():
            perf = ElementTree.SubElement(xmcda, 'performance')
            critid = ElementTree.SubElement(perf, 'criterionID')
            critid.text = crit.id
            value = ElementTree.SubElement(perf, 'value')
            p = marshal(val)
            value.append(p)

class threshold(action):
    pass

class profile(action):

    def __init__(self, id=None, name=None, performances=None,
                 indifference=None, preference=None, veto=None):
        action.__init__(self, id, name, performances)
        self.indifference = indifference
        self.preference = preference
        self.veto = veto
