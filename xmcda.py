from ZSI.client import NamedParamBinding
import sys #FIXME: useless
import time

ETRI_BM_URL = 'http://webservices.decision-deck.org/soap/ElectreTriBMInference-PyXMCDA-test.py'

def format_alternatives(alts):
    output = "<alternatives>\n"
    for alt in alts:
        output += "\t<alternative id=\"%s\">\n" % alt
        output += "\t\t<active>true</active>\n"
        output += "\t</alternative>\n"
    output += "</alternatives>\n"
    return output

def format_affectations(affectations):
    output = "<alternativesAffectations>\n"
    for alternative, category in affectations.iteritems():
        output += "\t<alternativeAffectation>\n"
        output += "\t\t<alternativeID>%s</alternativeID>\n" % alternative
        output += "\t\t<categoryID>%s</categoryID>\n" % category
        output += "\t</alternativeAffectation>\n"
    output += "</alternativesAffectations>\n"
    return output

def format_criteria(criteria, directions=None, q_thresholds=None, p_thresholds=None, v_thresholds=None):
    output = "<criteria>\n"
    for criterion in criteria:
        output += "\t<criterion id=\"%s\">\n" % criterion
        if directions:
            if directions[criterion] == -1:
                direction = 'min'
            else:
                direction = 'max'
            output += "\t\t<scale>\n"
            output += "\t\t\t<quantitative>\n"
            output += "\t\t\t\t<preferenceDirection>%s</preferenceDirection>\n" % direction
            output += "\t\t\t</quantitative>\n"
            output += "\t\t</scale>\n"
        if q_thresholds or p_thresholds or v_thresholds:
            output += "\t\t<thresholds>\n"
            if q_thresholds:
                for i, q in enumerate(q_thresholds):
                    output += "\t\t\t<threshold id=\"q%d\" name=\"indifference\" mcdaConcept=\"indifference\">\n" % (i+1)
                    output += "\t\t\t\t<constant><real>%f</real></constant>\n" % q[criterion]
                    output += "\t\t\t</threshold>\n"
            if p_thresholds:
                for i, p in enumerate(p_thresholds):
                    output += "\t\t\t<threshold id=\"p%d\" name=\"preference\" mcdaConcept=\"preference\">\n" % (i+1)
                    output += "\t\t\t\t<constant><real>%f</real></constant>\n" % p[criterion]
                    output += "\t\t\t</threshold>\n"
            if v_thresholds:
                for i, v in enumerate(v_thresholds):
                    if v.has_key(criterion):
                        output += "\t\t\t<threshold id=\"v%d\" name=\"veto\" mcdaConcept=\"veto\">\n" % (i+1)
                        output += "\t\t\t\t<constant><real>%f</real></constant>\n" % v[criterion]
                        output += "\t\t\t</threshold>\n"
            output += "\t\t</thresholds>\n"
        output += "\t</criterion>\n"
    output += "</criteria>\n"
    return output

def format_categories(categories):
    output = "<categories>\n"
    for i, category in enumerate(categories):
        output += "\t<category id=\"%s\">\n" % category
        output += "\t\t<active>true</active>\n"
        output += "\t\t<rank><integer>%d</integer></rank>\n" % (i+1)
        output += "\t</category>\n"
    output += "</categories>\n"
    return output

def format_performances_table(perfs_table):
    output = "<performanceTable>\n"
    for alternative, perfs in perfs_table.iteritems():
        output += "\t<alternativePerformances>\n"
        output += "\t\t<alternativeID>%s</alternativeID>\n" % alternative
        for criterion, value in perfs.iteritems():
            output += "\t\t<performance>\n"
            output += "\t\t\t<criterionID>%s</criterionID>\n" % criterion
            output += "\t\t\t<value><real>%s</real></value>\n" % value
            output += "\t\t</performance>\n"
        output += "\t</alternativePerformances>\n"
    output += "</performanceTable>\n"
    return output

def format_criteria_weights(weights):
    output = "<criteriaValues>\n"
    for crit, weight in weights.iteritems():
        output += "\t<criterionValue>\n"
        output += "\t\t<criterionID>%s</criterionID>\n" % crit
        output += "\t\t<value><real>%s</real></value>\n" % weight
        output += "\t</criterionValue>\n"
    output += "</criteriaValues>\n"
    return output

def format_category_profiles(profiles, palts_id, cat_id):
    output = "<categoriesProfiles>\n"
    for i, profile in enumerate(profiles):
        output += "\t<categoryProfile>\n"
        output += "\t\t<alternativeID>%s</alternativeID>\n" % palts_id[i]
        output += "\t\t<limits>\n"
        output += "\t\t\t<lowerCategory><categoryID>%s</categoryID></lowerCategory>\n" % cat_id[i]
        output += "\t\t\t<upperCategory><categoryID>%s</categoryID></upperCategory>\n" % cat_id[i+1]
        output += "\t\t</limits>\n"
        output += "\t</categoryProfile>\n"
    output += "</categoriesProfiles>\n"
    return output

def format_pt_reference_alternatives(profiles, palts_id, crit_id):
    output = "<performanceTable>\n"
    output += "\t<description>\n"
    output += "\t\t<title>Performance table of reference alternatives</title>\n"
    output += "\t</description>\n"
    for i, profile in enumerate(profiles):
        output += "\t<alternativePerformances>\n"
        output += "\t\t<alternativeID>%s</alternativeID>\n" % palts_id[i]
        for j, crit in enumerate(crit_id): 
           output += "\t\t<performance>\n"
           output += "\t\t\t<criterionID>%s</criterionID>\n" % crit
           output += "\t\t\t<value><real>%s</real></value>\n" % profile['refs'][crit]
           output += "\t\t</performance>\n"
        output += "\t</alternativePerformances>\n"

    output += "</performanceTable>\n"
    return output

def format_lambda(lbda):
    output = "<methodParameters>\n"
    output += "\t<parameter name=\"lambda\">\n"
    output += "\t\t<value><real>%s</real></value>\n" % lbda
    output += "\t</parameter>\n"
    output += "</methodParameters>\n"
    return output

def add_xmcda_tags(xml_data):
    output = '<?xml version="1.0" encoding="UTF-8"?>\n'
    output += '<?xml-stylesheet type="text/xsl" href="xmcdaXSL.xsl"?>\n'
    output += '<xmcda:XMCDA xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.decision-deck.org/2009/XMCDA-2.0.0 file:../XMCDA-2.0.0.xsd" xmlns:xmcda="http://www.decision-deck.org/2009/XMCDA-2.0.0" instanceID="void">\n'
    output += xml_data
    output += "</xmcda:XMCDA>\n"
    return output

def submit_problem(url, params):
    host=url.split('/')[2]

    service = NamedParamBinding(host=host,
                                port=80,
                                url=url,
                                tracefile=None)
    print service.hello()['message'].encode('UTF-8')
    sp = service.submitProblem(**params)
    print "Return Ticket: " + sp['ticket']
    return sp['ticket']

def request_solution(url, ticket_id, timeout=0):
    host=url.split('/')[2]

    service = NamedParamBinding(host=host,
                                port=80,
                                url=url,
                                tracefile=sys.stderr)

    start = time.time()
    while True:
        answer = service.requestSolution(ticket=ticket_id)
        if answer['service-status'] != 1:
            break;

        if timeout == 0:
            return None

        time.sleep(0.5)
        if timeout >= 0 and time.time()>start+timeout:
            print('timeout: solution not available after %i seconds: exiting'%timeout)
            return None

    return answer

def get_lambda(xmltree):
    xml_lbda = xmltree.find(".//methodParameters/parameter/value/real")
    return float(xml_lbda.text)

def get_method_messages(xmltree):
    messages = []
    for xmlmsg in xmltree.findall(".//methodMessages/logMessage/text"):
        messages.append(xmlmsg.text)
    return messages

def get_method_errors(xmltree):
    errors = []
    for xmlmsg in xmltree.findall(".//methodMessages/errorMessage/text"):
        errors.append(xmlmsg.text)
    return errors

def save_file(filename, xmcda_data):
    file = open(filename, "w")
    file.write(add_xmcda_tags(xmcda_data))
    file.close()

# FIXME: PyXMCDA variant of getConstantThresholds
# FIXME: camelcase of all the functions below
def get_value (xmltree) :
    try :
        xmlvalue = xmltree.find("value")
        if xmlvalue.find("integer") != None:
            val = int(xmlvalue.find("integer").text)
        elif xmlvalue.find("real") != None:
            val = float(xmlvalue.find("real").text)
        elif xmlvalue.find("rational") != None:
            val = float(xmlvalue.find("rational/numerator").text)/float(xmlvalue.find("rational/denominator").text)
        elif xmlvalue.find("label") != None:
            val = xmlvalue.find("label").text
        elif xmlvalue.find("rankedLabel") != None:
            val = float(xmlvalue.find("rankedLabel/rank").text)
        elif xmlvalue.find("boolean") != None:
            val = xmlvalue.find("boolean").text
        elif xmlvalue.find("NA") != None:
            val = "NA"
        else:
            val = None
    except:
        val = None

    return val

def get_thresholds(xmltree, critId):
    thresholds = {}
    try:
        for criterion in xmltree.findall(".//criterion") :
            criterionID = criterion.get("id")
            xmlthresholds = criterion.find("thresholds")
            if xmlthresholds != None :
                tempThresholds = {}
                for xmlthreshold in xmlthresholds.findall("threshold") :
                    xmlVal = xmlthreshold.find("constant/real")
                    if xmlVal == None :
                        xmlVal = xmlthreshold.find("constant/integer")
                    if xmlVal != None :
                        if xmlthreshold.get("id") != None :
                            tempThresholds[xmlthreshold.get("id")] = float(xmlVal.text)
                thresholds[criterionID] = tempThresholds
            else :
                thresholds[criterionID] = {}
    except :
        return None
     
    return thresholds

def get_performance_table(xmltree, alternativesId, criteriaId):
    perfTable = xmltree.find(".//performanceTable")
    Table = {}
    if perfTable != None :
        allAltPerf = perfTable.findall("alternativePerformances")
        for altPerf in allAltPerf :
            alt = altPerf.find("alternativeID").text
            Table[alt]={}
            allCritPerf = altPerf.findall("performance")
            for critPerf in allCritPerf :
                crit = critPerf.find("criterionID").text
                val = get_value(critPerf)
                Table[alt][crit] = val
                        
    return Table

def get_criterion_value(xmltree, criteriaId) :
    values = {}
    for criterionValue in xmltree.findall("criteriaValues/criterionValue") :
        crit = criterionValue.find("criterionID").text
        if criteriaId.count(crit) > 0 :
            values[crit] = get_value(criterionValue)

    return values

def get_alternatives_id (xmltree, condition="ACTIVE"):
    alternativesID = []
    for listAlternatives in xmltree.findall('alternatives'):
        for alternative in listAlternatives.findall('alternative'):
            active = alternative.find('active')
            if condition == "ACTIVE" and (active == None or active.text == "true"):
                alternativesID.append(str(alternative.get('id')))
            elif condition == "INACTIVE" and (active != None and active.text == "false"):
                alternativesID.append(str(alternative.get('id')))
            elif condition == "ALL" :
                alternativesID.append(str(alternative.get('id')))

    return alternativesID

def get_criteria_id(xmltree, condition="ACTIVE"):
    criteriaID = []
    for listCriteria in xmltree.findall('criteria'):
        for criterion in listCriteria.findall('criterion'):
            active = criterion.find('active')

            if condition == "ACTIVE" and (active == None or active.text == "true"):
                criteriaID.append(str(criterion.get('id')))
            elif condition == "INACTIVE" and (active != None and active.text == "false"):
                criteriaID.append(str(criterion.get('id')))
            elif condition == "ALL":
                criteriaID.append(str(criterion.get('id')))

    return criteriaID

def get_criteria_directions(xmltree, critId):
    prefDir = {}
    for criterion in xmltree.findall(".//criterion") :
        criterionID = criterion.get("id")
        try:
            xmlprefdir = criterion.find(".//preferenceDirection")
            prefDir[criterionID] = xmlprefdir.text 
        except:
            prefDir[criterionID] = 'max'

    return prefDir
