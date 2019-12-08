import chart_studio.plotly as py
import chart_studio 
import pandas as pd
import plotly.graph_objs as go
import numpy as np
# All get data frame functions can be found in utilities.py
import utilities
from statistics import mean

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
    
    census2000['%WHITE'] = census2000['WHITE'] / census2000['TOTAL'].round( decimals=3 )

    return census2000
 
def createPerWhiteVar2010( census2010 ):    
    # Create %WHITE variable for census2010 data
    census2010['%WHITE'] = census2010['Total Non-Minority Population (White Not Hispanic)'] / census2010['Total Population'].round(decimals=3)
    return census2010 

def createPerBlackVar2000(census2000):
    # Crete %BLACK variable for census2000 data
    census2000['%BLACK'] = (census2000['BLACK'] / census2000['TOTAL']).round(decimals=3)
    
    return census2000

def createPerBlackVar2010(census2010):
    # Crete %BLACK variable for census2010 data
    census2010['%BLACK'] = ((census2010['Pop of 1 race: Black'] + census2010['Pop 2 or more races: Black and'])
        / census2010['Total Population']).round(decimals=3)
    
    return census2010

# Creates first plotly graph which will be a double bar chart of mean income
# in each clusters in the years 2000 and 2010.
def vis1(census2000, census2010):
    # The X-axis will be the cluster number (1-39)
    x_axis = []
    # The Y-axis will be the average income for each cluster in the years 2005 and 2015
    y_axis_2000 = []
    y_axis_2010 = []

    # Lists that will hold change in in come of clusters East and West of the Anacostia 
    diff_West = []
    diff_East = []
    
    for x in range(1,40):
        # Get all rows in census2000 dataframe where the cluster is equal to x 
        clusterRows = census2000.loc[census2000['NEIGHBORHOODCLUSTER'] == x]
        # Find the mean income of all the tracts in that cluster 
        avg2000 = round(clusterRows['FAGI_MEDIAN_2005'].mean(), 2)
        # Add it to the Y-axis list
        y_axis_2000.append(avg2000)
        
        # Get all rows in census2010 dataframe where the cluster is equal to x 
        clusterRows = census2010.loc[census2010['NEIGHBORHOODCLUSTER'] == x]
        # Find the mean income of all the tracts in that cluster 
        avg2010 = round(clusterRows['FAGI_MEDIAN_2015'].mean(), 2)
        # Add it to the Y-axis list
        y_axis_2010.append(avg2010)
        
        # Add value of x to X-axis list 
        x_axis.append(x)
        
        if x < 28:
            diff_West.append(avg2010-avg2000)
        elif x == 29:
            diff_East.append(0)
        else:
            diff_East.append(avg2010-avg2000)
	
    # Display average growth of the West and East side
    print('Average change West of the Anacostia:', round(mean(diff_West), 2))
    print('Average change East of the Anacostia:', round(mean(diff_East), 2))

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
    
def vis5(census2000):
    # Create trace with x-axis as % white and y-axis as median income
    trace = go.Scatter(
	x = census2000['%WHITE'],
	y = census2000['FAGI_MEDIAN_2005'],
    hovertext = census2000['NEIGHBORHOODCLUSTER'],
	mode = 'markers'
    )

    # Assign it to an trace object named myData
    myData = [trace]

    # Add axis and title
    myLayout = go.Layout(
	title = "Relationship Between Population of White People and Income in 2005",
	xaxis=dict(
		title = 'Population of White People in Tract'
	),
	yaxis=dict(
		title = 'Median Income (USD)'
           )
    )

    # Setup figure
    myFigure = go.Figure(data=myData, layout=myLayout)

    # Display the scatterplot
    py.plot(myFigure, filename='2005 ScatterPlot')
    
def vis6(census2010):
    # Create trace with x-axis as % white and y-axis as median income
    trace = go.Scatter(
	x = census2010['%WHITE'],
	y = census2010['FAGI_MEDIAN_2015'],
    hovertext = census2010['NEIGHBORHOODCLUSTER'],
	mode = 'markers'
    )

    # Assign it to an trace object named myData
    myData = [trace]

    # Add axis and title
    myLayout = go.Layout(
	title = "Relationship Between Population of White People and Income in 2015",
	xaxis=dict(
		title = 'Population of White People in Tract'
	),
	yaxis=dict(
		title = 'Median Income (USD)'
           )
    )

    # Setup figure
    myFigure = go.Figure(data=myData, layout=myLayout)

    # Display the scatterplot
    py.plot(myFigure, filename='2015 ScatterPlot')
    

def vis7(census2000, census2010):
    # Create new variable %BLACK in datasets
    census2000 = createPerBlackVar2000(census2000)
    census2010 = createPerBlackVar2010(census2010)
    
    # List for x-axis: difference in %BLACK between 2000 and 2010,
    # and y-axis: neighborhood cluster.
    x_cluster = []
    y_diff = []
    
    for x in range(1,40):
        # Get all rows in census2000 dataframe where the cluster is equal to x 
        clusterRows = census2000.loc[census2000['NEIGHBORHOODCLUSTER'] == x]
        # Find the mean income of all the tracts in that cluster 
        avg2000 = round(clusterRows['%BLACK'].mean(), 2)

        
        # Get all rows in census2010 dataframe where the cluster is equal to x 
        clusterRows = census2010.loc[census2010['NEIGHBORHOODCLUSTER'] == x]
        # Find the mean income of all the tracts in that cluster 
        avg2010 = round(clusterRows['%BLACK'].mean(), 2)
    
        y_diff.append((avg2010 - avg2000))
        x_cluster.append(x)
        
    
    # Create trace for  data
    trace = go.Bar(
            x = x_cluster,
            y = y_diff,
            name='Change in Population of Black People in Clusters Between 2000 and 2010'
            )
    
    # Assign data to trace objects named myData
    myData = [trace]

    # Add axis and title
    myLayout = go.Layout(
	title = "Change in Population of Black People in Clusters Between 2000 and 2010",
	xaxis=dict(
		title = 'Neighborhood Cluster'
	    ),
	yaxis=dict(
		title = 'Change in Population'
          )
    )

    # Setup figure
    myFigure = go.Figure(data=myData, layout=myLayout)

    # Display the scatterplot
    py.plot(myFigure, filename='Black Pop Bar')


def vis8(permits2018):
    # Get all rows where permit type is Construction
    constPermits = permits2018.loc[permits2018['PERMIT_TYPE_NAME'] == 'CONSTRUCTION']
    # The labels will be the cluser numbers (1-39)
    clusterLabels = []
    # The values will be the count permits in each cluster
    clusterValues = []

    for x in range(1, 40):
        # Get all rows in permits2010 dataframe where the cluster is equal to x
        clusterRows = constPermits.loc[constPermits['NEIGHBORHOODCLUSTER'] == x]
        clusterRows = clusterRows.dropna()

        # Finds the average amount of fees paid per cluster
        avg_fp = sum(clusterRows['FEES_PAID']) / len(clusterRows)

        # Add it to the values list
        clusterValues.append(avg_fp)

        # Add value of x to labels list
        clusterLabels.append(x)

    # Add title
    myLayout = go.Layout(
        title="Average Fees Paid of Construction Permits Filed in DC Clusters in 2018",
        yaxis=dict(nticks=4, range=[0, 7000])
    )

    # Assign data to appropriate axis on heatmap
    myData = go.Bar(
        x=clusterLabels,
        y=clusterValues,
        name='Average Fees Paid 2018'

    )

    # Setup figure
    myFigure = go.Figure(data=myData, layout=myLayout)

    # Display the bar graph
    py.plot(myFigure, filename='2018 Permits Fees Bar Graph')


def vis9(permits2010):
    # Get all rows where permit type is Construction
    constPermits = permits2010.loc[permits2010['PERMIT_TYPE_NAME'] == 'CONSTRUCTION']
    # The labels will be the cluster numbers (1-39)
    clusterLabels = []
    # The values will be the count permits in each cluster
    clusterValues = []

    for x in range(1, 40):
        # Get all rows in permits2010 dataframe where the cluster is equal to x
        clusterRows = constPermits.loc[constPermits['NEIGHBORHOODCLUSTER'] == x]
        clusterRows = clusterRows.dropna()

        # Finds the average amount of fees paid per cluster
        avg_fp = sum(clusterRows['FEES_PAID']) / len(clusterRows)

        # Add it to the values list
        clusterValues.append(avg_fp)

        # Add value of x to labels list
        clusterLabels.append(x)


    # Add title
    myLayout = go.Layout(
        title="Average Fees Paid of Construction Permits Filed in DC Clusters in 2010",
        yaxis=dict(nticks=4, range=[0, 7000])
    )

    # Assign data to appropriate axis on bar graph
    myData = go.Bar(
        x=clusterLabels,
        y=clusterValues,
        name='Average Fees Paid 2010'

    )

    # Setup figure
    myFigure = go.Figure(data=myData, layout=myLayout)

    # Display the bar graph
    py.plot(myFigure, filename='2010 Permits Fees Bar Graph')



def main(): 
    # Open all csvs and get pandas dataframe of the data. 
    census2000 = utilities.getCensus2000()
    census2000 = createPerWhiteVar2000( census2000 )
    census2010 = utilities.getCensus2010()
    census2010 = createPerWhiteVar2010( census2010 )
    permits2010 = utilities.getPermits2010()
    permits2018 = utilities.getPermits2018()
    
    vis1(census2000, census2010)
    vis2(census2000, census2010)
    vis3(permits2010)
    vis4(permits2018)
    vis5(census2000)
    vis6(census2010)
    vis7(census2000, census2010)
    vis8(permits2018)
    vis9(permits2010)

if __name__ == "__main__":
    main()
