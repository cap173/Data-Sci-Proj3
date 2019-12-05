import chart_studio.plotly as py
import chart_studio 
import pandas as pd
import plotly.graph_objs as go
import numpy as np
# All get data frame functions can be found in utilities.py
import utilities

# Credentials to send plotly graphs to my account 
chart_studio.tools.set_credentials_file(username='chrisp45', api_key='n1f5Z2OhEwVm9jUEgUxJ')

# Creates a new column in each dataframe that takes the total number of White
# people recorded and divdes it by the total population in that area.
def createPerWhiteVar2000(census2000):
    # Create variable for census2000 data
    # We found a row wehre TOTAL == 0 which is making %WHITE NaN and I tried 
    # this method and it didn't work so I decided to manually remove the row
    #census2000['TOTAL'].replace(0, np.nan, inplace=True)
    #census2000.dropna( axis='columns' )
    census2000 = census2000.drop( census2000.index[59] )
    
    census2000['%WHITE'] = census2000['WHITE'] / census2000['TOTAL']
    census2000['%WHITE'] = census2000['%WHITE'].round( decimals=3 )

    return census2000
 
def createPerWhiteVar2010( census2010 ):    
    # Create variable for census2010 data
    census2010['%WHITE'] = census2010['Total Non-Minority Population (White Not Hispanic)'] / census2010['Total Population'].round(decimals=3)
    return census2010 

# Creates first plotly graph which will be a double bar chart of mean income
# in each clusters in the years 2000 and 2010.
def vis1(census2000, census2010):
    # The X-axis will be the cluster number (1-39)
    x_axis = []
    # The Y-axis will be the average income for each cluster in the years 2005 and 2015
    y_axis_2000 = []
    y_axis_2010 = []
    
    for x in range(1,40):
        # Get all rows in census2000 dataframe where the cluster is equal to x 
        clusterRows = census2000.loc[census2000['NEIGHBORHOODCLUSTER'] == x]
        # Find the mean income of all the tracts in that cluster 
        avg = round(clusterRows['FAGI_MEDIAN_2005'].mean(), 2)
        # Add it to the Y-axis list
        y_axis_2000.append(avg)
        
        # Get all rows in census2010 dataframe where the cluster is equal to x 
        clusterRows = census2010.loc[census2010['NEIGHBORHOODCLUSTER'] == x]
        # Find the mean income of all the tracts in that cluster 
        avg = round(clusterRows['FAGI_MEDIAN_2015'].mean(), 2)
        # Add it to the Y-axis list
        y_axis_2010.append(avg)
        
        # Add value of x to X-axis list 
        x_axis.append(x)

    # Create trace for 2000 data        
    trace2000 = go.Bar(
            x = x_axis,
            y = y_axis_2000,
            name='Average Income in 2005'
            )
    
    # Create trace for 2010 data
    trace2010 = go.Bar(
            x = x_axis,
            y = y_axis_2010,
            name='Average Income in 2015'
            )
    
    # Assign data to trace objects named myData
    myData = [trace2000, trace2010]

    # Add axis and title
    myLayout = go.Layout(
	title = "Average Income in DC Neighborhood Clusters in 2005 and 2015",
	xaxis=dict(
		title = 'Neighborhood Cluster'
	    ),
	yaxis=dict(
		title = 'Average Income (USD)'
          )
    )

    # Setup figure
    myFigure = go.Figure(data=myData, layout=myLayout)

    # Display the scatterplot
    py.plot(myFigure, filename='Income Double Bar')
    

# Create second plotly graph which be a heatmap displaying the 
# percentage of white people in each cluster in 2000 and 2010.    
def vis2(census2000, census2010):
    # The X-axis will be the cluster number (1-39)
    x_axis = []
    # The Y-axis will be the average % of white people for each cluster in the years 2000 and 2010
    z_axis_2000 = []
    z_axis_2010 = []
    
    census2010 = census2010.fillna(0)
    
    for x in range(1,40):
        # Get all rows in census2000 dataframe where the cluster is equal to x 
        clusterRows = census2000.loc[census2000['NEIGHBORHOODCLUSTER'] == x]
        # Find the mean income of all the tracts in that cluster 
        avg = round(clusterRows['%WHITE'].mean(), 3)
        # Add it to the Y-axis list
        z_axis_2000.append(avg)
        
        # Get all rows in census2010 dataframe where the cluster is equal to x 
        clusterRows = census2010.loc[census2010['NEIGHBORHOODCLUSTER'] == x]
        # Find the mean income of all the tracts in that cluster 
        avg = round(clusterRows['%WHITE'].mean(), 3)
        # Add it to the Y-axis list
        z_axis_2010.append(avg)
        
        # Add value of x to X-axis list 
        x_axis.append(x)
        
    # Add title
    myLayout = go.Layout(
    title = "Average of Amount White People in DC Neighborhood Clusters in 2000 and 2010",
    xaxis=dict(
		title = 'Neighborhood Cluster'
	    )
    )
    
    # Assign data to appropriate axis on heatmap
    myData = go.Heatmap(
            x = x_axis,
            y = ['Year: 2000', 'Year: 2010'],
            z = [z_axis_2000, z_axis_2010]
            )
    
    # Setup figure
    myFigure = go.Figure(data=myData, layout=myLayout)

    # Display the scatterplot
    py.plot(myFigure, filename='White People Heat Map')
    
    
def vis3(permits2010):
    # Get all rows where permit type is Construction
    constPermits = permits2010.loc[permits2010['PERMIT_TYPE_NAME'] == 'CONSTRUCTION']
    # The labels will be the cluser numbers (1-39)
    clusterLabels = []
    # The values will be the count permits in each cluster
    clusterValues = []
    
    for x in range(1,40):
        # Get all rows in permits2010 dataframe where the cluster is equal to x
        clusterRows = constPermits.loc[constPermits['NEIGHBORHOODCLUSTER'] == x]
        # Count how many permits were filled in cluster x
        rowCount = clusterRows.shape[0]
        # Add it to the values list
        clusterValues.append(rowCount)
        
        # Add value of x to labels list
        clusterLabels.append(x)
        
    # Add title
    myLayout = go.Layout(
    title = "Percentage of Construction Permits Filed in DC Clusters in 2010",
    )
    
    # Assign data to appropriate axis on heatmap
    myData = go.Pie(
            labels = clusterLabels,
            values = clusterValues
            )
    
    # Setup figure
    myFigure = go.Figure(data=myData, layout=myLayout)

    # Display the scatterplot
    py.plot(myFigure, filename='2010 Permits Pie Chart')
    
def vis4(permits2018):
    # Get all rows where permit type is Construction
    constPermits = permits2018.loc[permits2018['PERMIT_TYPE_NAME'] == 'CONSTRUCTION']
    # The labels will be the cluser numbers (1-39)
    clusterLabels = []
    # The values will be the count permits in each cluster
    clusterValues = []
    
    for x in range(1,40):
        # Get all rows in permits2010 dataframe where the cluster is equal to x
        clusterRows = constPermits.loc[constPermits['NEIGHBORHOODCLUSTER'] == x]
        # Count how many permits were filled in cluster x
        rowCount = clusterRows.shape[0]
        # Add it to the values list
        clusterValues.append(rowCount)
        
        # Add value of x to labels list
        clusterLabels.append(x)
        
    # Add title
    myLayout = go.Layout(
    title = "Percentage of Construction Permits Filed in DC Clusters in 2018",
    )
    
    # Assign data to appropriate axis on heatmap
    myData = go.Pie(
            labels = clusterLabels,
            values = clusterValues
            )
    
    # Setup figure
    myFigure = go.Figure(data=myData, layout=myLayout)

    # Display the scatterplot
    py.plot(myFigure, filename='2018 Permits Pie Chart')    
    

def main(): 
    # Open all csvs and get pandas dataframe of the data. 
    census2000 = getCensus2000()
    census2000 = createPerWhiteVar2000( census2000 )
    census2010 = getCensus2010()
    createPerWhiteVar2010( census2010 )
    permits2010 = getPermits2010()
    permits2018 = getPermits2018()
    
    #vis1(census2000, census2010)
    #vis2(census2000, census2010)
    vis3(permits2010)
    vis4(permits2018)

if __name__ == "__main__":
    main()
