# sqlalchemy-challenge

The script uses Python and SQLAlchemy to do a basic climate analysis and data exploration of a climate database. Specifically, using SQLAlchemy ORM queries, Pandas, and Matplotlib.

* Python is connected to database by creating a SQLAlchemy session.

Two types of analysis performed using SQLAlchemy (climate_starter.ipynb):
1. Precipitation Analysis - the percipitation information for the last 12 months is retrieved and plotted on a chart.
2. Station Analysis.
    2.1. Total # of stations is calculated.
    2.2. The list of the stations is displayed.
    2.3. Min, Max and Avg temperature is calculated for the most active station (station with the most observations).
    2.3. Histogram with the temperature observation (TOBS) for the past 12 months of data collected by the most active station is created. 

* Flask API is developed to display the analysis results, including the following routes:
1. / - home page.
2. /api/v1.0/precipitation - JSON representation of a dictionary where date is the key and prcp is the value
3. /api/v1.0/stations - JSON list of stations from the dataset.
4. /api/v1.0/tobs - list of temperature observations for the previous year.
5. /api/v1.0/<start> and /api/v1.0/<start>/<end> - JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.