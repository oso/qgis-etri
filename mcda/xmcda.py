from xml.etree import ElementTree

class xmcda_utils:

    def get_value(self, xmltree):
        xmlvalue = xmltree.find("value")
        if xmlvalue.find("integer") != None:
            val = int(xmlvalue.find("integer").text)
        elif xmlvalue.find("real") != None:
            val = float(xmlvalue.find("real").text)
        else:
            val = xmlvalue.find("real").text
        return val

    def set_value(self, value):
        out = "<value>"
        if isinstance(value, int):
            out += "<integer>%d</integer>" % value
        elif isinstance(value, float):
            out += "<float>%f</float>" % value
        else:
            raise TypeError, "xmcda: invalid object type"
        out += "</value>"
        return out

class xmcda_object(ElementTree.Element):

    def __init__(self, input=None):
        super(ElementTree.Element, self).__init__(parent)

    def get_method_message(self):
        msg = []
        for xmlmsg in self.findall(".//methodMessages/logMessage/text"):
            msg.append(xmlmsg.text)
        return msg

    def get_method_errors(self):
        msg = []
        for xmlmsg in self.findall(".//methodMessages/errorMessage/text"):
            msg.append(xmlmsg.text)
        return msg 

    def get_lambda(self):
        lbda = self.find(".//methodParameters/parameter/value/real") 
        return float(lbda.text)

    def update_criteria_weight(self, criteria):
        for crit_val in self.findall("criteriaValues/criterionValue"):
            crit = crit_val.find("criterionID").text
            criterion = criteria.index(crit)
            criterion.weight = self.get_value(crit_val)

    def update_criteria_direction(self, criteria):
        for crit in self.findall(".//criterion"):
            id = crit.get("id")
            criterion = criteria.index(id)
            xmlprefdir = criterion.find(".//preferenceDirection")
            if xmlprefdir != None:
                if xmlprefdir.text == 'min':
                    criterion.direction = -1
                else:
                    criterion.direction = 1
