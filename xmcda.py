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

def format_criteria(criteria):
    output = "<criteria>\n"
    for criterion in criteria:
        output += "\t<criterion id=\"%s\"></criterion>\n" % criterion
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
        if answer['service-status'] != 1: # NOT AVAILABLE
            break;
        time.sleep(0.5)
        if timeout and time.time()>start+timeout:
            print('timeout: solution not available after %i seconds: exiting'%timeout)
            return None

    for k,v in answer.items():
        print "%s: %s" % (k,v)

    return answer

def get_lambda(xmltree):
    xml_lbda = xmltree.find(".//methodParameters/parameter/value/real")
    return float(xml_lbda.text)
