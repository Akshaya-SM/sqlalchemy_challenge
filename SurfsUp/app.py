# Import the dependencies.

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

import numpy as np
import datetime as dt


#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base() 

# reflect the tables
Base.prepare(autoload_with= engine)

# Save references to each table
Station= Base.classes.station
Measurement= Base.classes.measurement

# Create our session (link) from Python to the DB
session= session(engine)

#################################################
# Flask Setup
#################################################

app= Flask(__name__)


#################################################
# Flask Routes
#################################################
