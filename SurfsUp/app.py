# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
# create an engine
engine = create_engine("sqlite:///SurfsUp\Resources\hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Calculate the date one year from the last date in data set.
year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

# List the operations to calculate - min, max, avg
temp_stats = [func.min(measurement.tobs), 
func.max(measurement.tobs), 
func.avg(measurement.tobs)]


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Create list of all API routes
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/YYYY-MM-DD<br/>"
        f"Replace with the desired start date. Please note that the latest date available is 2017-08-23<br/>"
        f"/api/v1.0/YYYY-MM-DD/YYYY-MM-DD<br/>"
        f"Replace with the desired start date, followed by end date."
    )

# Create API route to retrieve data about percipitation within the last 12 months
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the date and precipitation scores
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= year_ago).all()
    
    # Close the session
    session.close()

    # Create a dictionary from the row data using date as the key and prcp as the value, and append to a list of percipitation data
    percipitation_data = []

    for date, prcp in results:
        percipitation_dict = {}
        percipitation_dict[date] = prcp
        percipitation_data.append(percipitation_dict)

    return jsonify(percipitation_data)


# Create API route to retrieve JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the list of stations
    results = session.query(station.station).all()
   
    # Close the session
    session.close()

    # Convert list of tuples into normal list
    stations_list = list(np.ravel(results))

    return jsonify(stations_list)


# Create API route to retrieve dates and temperature observations of the most-active station for the previous year of data.
@app.route("/api/v1.0/tobs")
def temperature():
    # Create session (link) from Python to the DB
    session = Session(engine)

    # List all the stations
    active_stations = session.query(station.station).all()

    # Perform a query to retrieve the date and temperature
    results = session.query(measurement.date, measurement.tobs).\
    filter(and_(measurement.date>=year_ago,measurement.station == active_stations[0][0])).all()
    
    # Close the session
    session.close()

    # Create a dictionary from the row data using date and append to a list of temperature data
    temperature_data = []

    for date, tobs in results:
        temperature_dict = {}
        temperature_dict['date'] = date
        temperature_dict['tobs'] = tobs
        temperature_data.append(temperature_dict)

    return jsonify(temperature_data)    


# Create API route to retrieve data for min, avg and max temp for a specified start date.
@app.route("/api/v1.0/<start>")
def start(start):
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve min, avg and max temp for a specified start date
    results = session.query(*temp_stats).filter(measurement.date >= start).all()
    
    # Close the session
    session.close()

    # Create a dictionary from the row data using date and append to a list of temperature data
    start_temperature_data = []

    for TMIN, TMAX, TAVG in results:
        start_temperature_dict = {}
        start_temperature_dict['TMIN'] = TMIN
        start_temperature_dict['TMAX'] = TMAX
        start_temperature_dict['TAVG'] = TAVG
        start_temperature_data.append(start_temperature_dict)

    return jsonify(start_temperature_data)    


# Create API route to retrieve data for min, avg and max temp for a specified start-end range.
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve min, avg and max temp for a specified start-end range
    results = session.query(*temp_stats).filter(and_(measurement.date >= start, measurement.date <= end)).all()
    
    # Close the session
    session.close()

    # Create a dictionary from the row data using date and append to a list of temperature data
    st_end_temperature_data = []

    for TMIN, TMAX, TAVG in results:
        st_end_temperature_dict = {}
        st_end_temperature_dict['TMIN'] = TMIN
        st_end_temperature_dict['TMAX'] = TMAX
        st_end_temperature_dict['TAVG'] = TAVG
        st_end_temperature_data.append(st_end_temperature_dict)

    return jsonify(st_end_temperature_data)    

if __name__ == '__main__':
    app.run(debug=True)