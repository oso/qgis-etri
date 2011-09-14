#!/usr/bin/python
import sys
sys.path.append("..")
from etri import *
from data_loulouka import *

etri = electre_tri(a, profiles, w, lbda)
print "ELECTRE TRI - Pessimist"
etri_p = etri.pessimist()
print etri_p
print "ELECTRE TRI - Optimist"
etri_o = etri.optimist()
print etri_o

etri.print_concordance_table()
etri.print_credibility_table()

for key in affect_p.keys():
	if affect_p[key] <> etri_p[key]:
		print 'Pessimits affectation of %s mismatch (%d <> %d)' % (str(key), affect_p[key], etri_p[key])
	if affect_o[key] <> etri_o[key]:
		print 'Optimist affectation of %s mismatch (%d <> %d)' % (str(key), affect_o[key], etri_o[key])

print "Model min values"
model_min = etri.get_model_min()
print model_min
print "Model max values"
model_max = etri.get_model_max()
print model_max
