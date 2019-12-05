import pandas as pd 

# Opens Census 2000 csv and converts data into pandas dataframe
def getCensus2000():
    myData = pd.read_csv( 'census_2000_CLEAN.csv', sep=',', encoding='latin1')
    return myData

# Opens Census 2010 csv and converts data into pandas dataframe
def getCensus2010():
    myData = pd.read_csv( 'census_2010_CLEAN.csv', sep=',', encoding='latin1')
    return myData

# Opens Permits 2010 csv and converts data into pandas dataframe
def getPermits2010():
    myData = pd.read_csv( 'permits_2010_CLEAN.csv', sep=',', encoding='latin1')
    return myData

# Opens Permits 2018 csv and converts data into pandas dataframe
def getPermits2018():
    myData = pd.read_csv( 'permits_2018_CLEAN.csv', sep=',', encoding='latin1')
    return myData
