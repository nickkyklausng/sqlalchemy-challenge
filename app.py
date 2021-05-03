#!/usr/bin/env python
# coding: utf-8

# In[3]:


import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


# In[4]:


#Setup database

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables

Base.prepare(engine, reflect = True)

# Save references to each table
measurement = Base.classes.measurement

station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


# In[5]:


#Flask Setup
app = Flask(__name__)

# In[ ]:


#Flask Route
@app.route("/")
def welcome():
    return(
    f"Hawaii Climate Analysis<br/>"
    f"Available Routes: <br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/start/end"
)

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    
    target_scores = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date > year_ago).all()
    
    #Dictionary with date as key and precipitation as value
    
    precipitation = {date:prcp for date, prcp in precipitation}
    return jsonify(precipitation)

session.close()

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(station.station).all()
 
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

session.close()

@app.route("/api/v1.0/tobs")
def tobs():
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    
    results = session.query(measurement.tobs).filter(measurement.stations == 'USC00519281').filter(measurement.date >= year_ago).all()

    temperature = list(np.ravel(results))
        
    return jsonify(temperature = temperature)

session.close()

#@app.route("/api/v1.0/start/end")
if __name__ == "__main__":
    app.debug = True
    app.run()