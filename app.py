
import numpy as np

import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# 1. import Flask
from flask import Flask

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)



##########################

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/tCalc/start_date/end_date<br/>"
        f"/api/v1.0/tCalc/start_date<br/>"

    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return aprecipitation data for last 1 year"""
    maxDate = session.query(Measurement).order_by(Measurement.date.desc()).limit(1)

    for date in maxDate:
        maxDate1 = date.date

    maxDate1 = dt.datetime.strptime(maxDate1, "%Y-%m-%d")

    ## Calculate the date 1 year ago from the last data point in the database
    startDate = maxDate1 - dt.timedelta(days=365)

    avgprcp = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= startDate).\
    order_by(Measurement.date).all()

    # Create a dictionary from the row data and append to a list 
    all_prcp= []
    for eachRow in avgprcp:
        prcp_dict = {}
        prcp_dict["date"] =eachRow.date
        prcp_dict["prcp"] =eachRow.prcp
        all_prcp.append(prcp_dict)
    session.close()
    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def listStation():
    """List all Stations"""
    
    listStn = session.query(Station.id, Station.name).all()
    
    # Create a dictionary from the row data and append to a list 
    all_stn= []
    for eachRow in listStn:
        stn_dict = {}
        stn_dict["id"] =eachRow.id
        stn_dict["name"] =eachRow.name
        all_stn.append(stn_dict)
    session.close()
    return jsonify(all_stn)

@app.route("/api/v1.0/tobs")
def listTobs():

    """Return aprecipitation data for last 1 year"""
    maxDate = session.query(Measurement).order_by(Measurement.date.desc()).limit(1)

    for date in maxDate:
        maxDate1 = date.date

    maxDate1 = dt.datetime.strptime(maxDate1, "%Y-%m-%d")

    ## Calculate the date 1 year ago from the last data point in the database
    startDate = maxDate1 - dt.timedelta(days=365)
    """List all Tobs"""
    
    tempData = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= startDate).\
    order_by(Measurement.date).all()

    
    # Create a dictionary from the row data and append to a list 
    all_tobs= []
    for eachRow in tempData:
        tobs_dict = {}
        tobs_dict["date"] =eachRow.date
        tobs_dict["tobs"] =eachRow.tobs
        all_tobs.append(tobs_dict)
    session.close()
    return jsonify(all_tobs)


@app.route("/api/v1.0/tCalc/<start_date>/<end_date>")
def tempCalc(start_date,end_date):
    tempList= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    
    # Create a dictionary from the row data and append to a list 
    
    all_tempCals= []
    t_dict = {}
    t_dict["min"] =tempList[0][0]
    t_dict["avg"] =tempList[0][1]
    t_dict["max"] =tempList[0][2]
    all_tempCals.append(t_dict)       
    session.close()
    return jsonify(all_tempCals)

@app.route("/api/v1.0/tCalc/<start_date>")
def tempCalcStart(start_date):
    tempList=  session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date).all()
    
    # Create a dictionary from the row data and append to a list 
    
    all_tempCals= []
    t_dict = {}
    t_dict["min"] =tempList[0][0]
    t_dict["avg"] =tempList[0][1]
    t_dict["max"] =tempList[0][2]
    all_tempCals.append(t_dict)       
    session.close()
    return jsonify(all_tempCals)

if __name__ == "__main__":
    app.run(debug=True)
