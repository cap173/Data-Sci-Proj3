import pandas as pd 

def getCensus2000():
    myData = pd.read_csv( 'census_2000_CLEAN.csv', sep=',', encoding='latin1')
    return myData

def getCensus2010():
    myData = pd.read_csv( 'census_2010_CLEAN.csv', sep=',', encoding='latin1')
    return myData

def getPermits2010():
    myData = pd.read_csv( 'permits_2010_CLEAN.csv', sep=',', encoding='latin1')
    return myData

def getPermits2018():
    myData = pd.read_csv( 'permits_2018_CLEAN.csv', sep=',', encoding='latin1')
    return myData
