# Import the dependencies.

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

import numpy as np
import datetime as dt


#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")
Base = automap_base() 

# reflect the tables
Base.prepare(autoload_with= engine)

# Save references to each table
Station= Base.classes.station
Measurement= Base.classes.measurement

# Create our session (link) from Python to the DB
session= Session(engine)

#################################################
# Flask Setup
#################################################

app= Flask(__name__)


#################################################
# Flask Routes
#################################################

# Homepage
@app.route("/")
def welcome():
    '''List all the available routes.'''
    return(
        f"Avilable Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/(start)<br/>"
        f"/api/v1.0/(start)/(end)<br/>"
        
    )

# Query results from your precipitation analysis (i.e. retrieve only the last 12 months of data)

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)
    # Calculate the date one year from the last date in data set.
    start_date= dt.datetime(2017,8,23)- dt.timedelta(days=365)

    # Set query to get precipitation data for last 12 months
    prcp_filter= session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= start_date).all()
    
    # Dictionary using date as the key and prcp as the value.
    precipitation_list=[]
    
    for date, prcp in prcp_filter:
       prcp_dict={}
       prcp_dict['Date']= date
       prcp_dict['Prcipitation']= prcp
       precipitation_list.append(prcp_dict)
    session.close()

    # Return the JSON representation of your dictionary.
    return jsonify(precipitation_list) 

# Query stations route: jsonified data of all the stations in the database

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    # Querry the stations data
    sel=[Station.station,
         Station.name,
         Station.longitude,
         Station.latitude,
         Station.elevation]
    station_list= session.query(*sel).all()

    # Create a dictionary for the Station_list
    station_dict = []
    for station,name, longitude, latitude, elevation in station_list:
        prcp_dict = {}
        prcp_dict["station"] = station
        prcp_dict["name"] = name
        prcp_dict["longitude"] = longitude
        prcp_dict["latitude"] = latitude
        prcp_dict["latitude"] = elevation
        station_dict.append(prcp_dict)

    session.close()

    # Return stations data dictionary as JSON file.

    return jsonify(station_dict)

# Query the Temprature Observation (tobs) endpoint

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    # Query the date and tobs of the most active station for the previous year
    sel=[Measurement.station, func.count(Measurement.station)]   
   
    # Most action station
    most_active_station= session.query(*sel).group_by(Measurement.station).\
                            order_by(func.count(Measurement.station).desc()).first()
    
    # Active stations count and their list.
    stations_list= session.query(*sel).group_by(Measurement.station).\
                      order_by(func.count(Measurement.station).desc()).all()  
    
    as_id= stations_list[0][0]

    temp_obs = session.query(Measurement.date, Measurement.tobs).\
                    filter(Measurement.date >= '2016-08-24').\
                    filter(Measurement.date <= '2017-08-23').\
                    filter(Measurement.station ==as_id).all()
    
    # Create a Dictionary for the date and tobs 
    date_tobs=[]
    for date, tobs in temp_obs:
        tobs_dict={}
        tobs_dict['Date']= date
        tobs_dict['Temperature']= tobs
        date_tobs.append(tobs_dict)

    session.close()
    
    # Return a json list of temperature observations.

    return jsonify(date_tobs)

# Query the Minimum, Average, Maximum temperature for a specified (start date)
    
@app.route('/api/v1.0/<start_dates>')   
def start(start_dates):
    session=Session(engine)

    tob_stats= session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), 
                func.avg(Measurement.tobs)).filter(Measurement.station >= start_dates).all()
    
    # Create a Dictionary
    tobs_stats_list=[]
    for min,avg,max in tob_stats:
        tob_stats_dict={}
        tob_stats_dict['min']=min
        tob_stats_dict['avg']=avg
        tob_stats_dict['max']=max
        tobs_stats_list.append(tob_stats_dict)

    session.close()

    # Return dictionary to a json file

    return jsonify(tobs_stats_list)

# Query the Minimum, Average, Maximum temperature for a specified (start-end date)

@app.route('/api/v1.0/<start_dates>/<end_dates>')
def start_end(start_dates, end_dates):
    session = Session(engine)

    # Query for minimum, average, and maximum tobs

    sel = [func.min(Measurement.tobs),
           func.avg(Measurement.tobs),
           func.max(Measurement.tobs)]
    tobs_range_stats = session.query(*sel).filter(Measurement.date >= start_dates).\
        filter(Measurement.date <= end_dates).all()

    # Create a dictionary

    tobs_stats_list1 = []
    for min, avg, max in tobs_range_stats:
        tobs_stats_dict1 = {}
        tobs_stats_dict1["min"] = min
        tobs_stats_dict1["avg"] = avg
        tobs_stats_dict1["max"] = max
        tobs_stats_list1.append(tobs_stats_dict1)

    session.close()

    # Return dictionary to a json file

    return jsonify(tobs_stats_list1)

     
if __name__ == "__main__":
    app.run(debug=True)

        

