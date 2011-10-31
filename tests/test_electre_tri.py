#!/usr/bin/python
import sys
sys.path.insert(0, "..")
from mcda.electre_tri import electre_tri

if __name__ == "__main__":
    
    if len(sys.argv) == 2 and sys.argv[1] == "-l":
        from data_loulouka_new import *
    else:
        from data_ticino_new import *

    etri = electre_tri(c, pt, ptb, lbda)
    print "ELECTRE TRI - Pessimist"
    etri_p = etri.pessimist()
    print etri_p
    print "ELECTRE TRI - Optimist"
    etri_o = etri.optimist()
    print etri_o

    for key in affect_p.keys():
        if affect_p[key] <> etri_p(key):
            print 'Pessimits affectation of %s mismatch (%d <> %d)' % (str(key), affect_p[key], etri_p[key])
        if affect_o[key] <> etri_o(key):
            print 'Optimist affectation of %s mismatch (%d <> %d)' % (str(key), affect_o[key], etri_o[key])
