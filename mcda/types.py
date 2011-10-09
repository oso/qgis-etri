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

    def from_xmcda(self, xmcda):
        tag_list = xmcda.getiterator('criterion')
        for tag in tag_list:
            c = criterion(0)
            c.from_xmcda(tag)
            self.append(c)

class criterion:

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
        xmcda = ElementTree.Element('criterion', id=self.id, name=self.name)

        active = ElementTree.SubElement(xmcda, 'active')
        if self.disabled == 0:
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

        value = ElementTree.SubElement(xmcda, 'criterionValue')
        weight = marshal(self.weight)
        value.append(weight)

        return xmcda

    def from_xmcda(self, xmcda):
        if xmcda.tag == 'criterion':
            crit = xmcda
        else:
            crit = xmcda.find('.//criterion')
        id = crit.get('id')
        if id != None:
            self.id = id
        name = crit.get('name')
        if name != None:
            self.name = name
        pdir = crit.find('.//scale/quantitative/preferenceDirection').text
        if pdir != None:
            if pdir == 'max':
                self.direction = 1
            elif pdir == 'min':
                self.direction = -1
            else:
                raise TypeError, 'criterion::invalid preferenceDirection'
        value = crit.find('.//criterionValue')

        value = crit.find('criterionValue')
        if value != None:
            self.weight = unmarshal(value.getchildren()[0])

class action:

    def __init__(self, id=None, name=None, evaluations=None, disabled=None):
        self.id = id
        if name == None:
            self.name = str(id)
        else:
            self.name = name
        self.evaluations = evaluations
        if disabled == None:
            disabled = 0
        self.disabled = disabled

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

    def to_xmcda(self):
        xmcda = ElementTree.Element('alternative', id=self.id,
                                    name=self.name)

        active = ElementTree.SubElement(xmcda, 'active')
        if self.disabled == 0:
            active.text = 'true'
        else:
            active.text = 'false'

        xmcda2 = ElementTree.Element('alternativePerformances')
        altid = ElementTree.SubElement(xmcda2, 'alternativeID')
        altid.text = self.id
        #FIXME: add the performance table !!!

        return (xmcda, xmcda2)

class threshold(action):
    pass

class profile(action):

    def __init__(self, id=None, name=None, evaluations=None,
                 indifference=None, preference=None, veto=None):
        action.__init__(self, id, name, evaluations)
        self.indifference = indifference
        self.preference = preference
        self.veto = veto
