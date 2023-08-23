# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
# create an engine for the hawaii.sqllite database
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
# ---STATIC ROUTES---
@app.route("/")
def homepage():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create a session from Python to the DB
    session = Session(engine)

    """Return results of precipitation analysis (retrieve only the last 12 months of data) to a dictionary using date as the 'key' and 'prcp' as the value"""

    # Query the last years precipitation
    last_12_months = session.query(Measurement.date, Measurement.prcp).\
        order_by(Measurement.date).\
        filter(Measurement.date >= '2016-08-23').all()

    session.close()

    # Create a dictionary from the row data and append to a list of date_precip
    date_precip = []
    for date, prcp in last_12_months:
        date_prcp_dict = {}
        date_prcp_dict["date"] = date
        date_prcp_dict["prcp"] = prcp
        date_precip.append(date_prcp_dict)

    return jsonify(date_precip)

@app.route("/api/v1.0/stations")
def stations():
    # Create a session from Python to the DB
    session = Session(engine)

    """Return jsonified data of all stations in the database"""

    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    all_stations = []
    for station, name, lat, lon, elev in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = lat
        station_dict["longitude"] = lon
        station_dict["elevation"] = elev
        all_stations.append(station_dict)

    return jsonify(all_stations)


# @app.route("/api/v1.0/tobs")
# def tobs():
#     # Create a session from Python to the DB
#     session = Session(engine)

#     # Query the dates and temperature observations of the most-active station for the previous year of data.

#     # Return a JSON list of temperature observations for the previous year.


# # ---DYNAMIC ROUTES---
# @app.route("/api/v1.0/<start>")
# def tobs():
#     # Create a session from Python to the DB
#     session = Session(engine)

#     """
#         Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

#         For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

#         For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
#     """


# @app.route("/api/v1.0/<start>/<end>")
# def tobs():
#     # Create a session from Python to the DB
#     session = Session(engine)

#     """
#         Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

#         For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

#         For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
#     """

if __name__ == '__main__':
    app.run(debug=True)