import requests
import os
import numpy as np

def get_props_nist(P,T1,T2,Tstep,CAS):
    '''
    P (psi)
    The rest: SI
    '''
    #CAS = "C74828"
    data = {"Action":"Data","Wide":"on","ID":CAS,"Type":"IsoBar",
"Digits":5,"P":P,"THigh":T2,"TLow":T1,"TInc":Tstep,"RefState":"DEF",
"TUnit":"K","PUnit":"psia","DUnit":"kg%2Fm3",
"HUnit":"kJ%2Fmol","WUnit":"m%2Fs","VisUnit":"uPa*s","STUnit":"N%2Fm"}
    r = requests.post("https://webbook.nist.gov/cgi/fluid.cgi",data=data)
    text = r.text.replace('liquid','1')
    text = text.replace('vapor','0')
    text = text.replace('supercritical','2')
    f = open('./%s/%s_%.5d.csv'%(CAS,CAS,P),'w')
    f.write(text)
    f.close()

def get_all_data(CAS,P1,P2,Pstep,T1,T2,Tstep):
    if not os.path.isdir(CAS):
        os.mkdir(CAS)
    for P in range(P1,P2+Pstep,Pstep):
        get_props_nist(P,T1,T2,Tstep,CAS)

def make_big_table(CAS,P1,P2,Pstep,T1,T2,Tstep):
    table = None
    for P in range(P1,P2+Pstep,Pstep):
        if P == P1:
            table = np.genfromtxt('./%s/%s_%.5d.csv'%(CAS,CAS,P), delimiter='\t')[1:]
        else:
            newtable = np.genfromtxt('./%s/%s_%.5d.csv'%(CAS,CAS,P), delimiter='\t')[1:]
            table = np.append(table,newtable,axis=0)
    return table