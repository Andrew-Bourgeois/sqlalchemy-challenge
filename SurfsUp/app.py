# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
from flask import Flask, jsonify

from datetime import datetime as dt, timedelta as td

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

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """List all available api routes."""
    return (
        f"Available Routes<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    """Return results of precipitation analysis (retrieve only the last 12 months of data) to a dictionary using date as the 'key' and 'prcp' as the value"""

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # find most recent observation
    most_recent = session.query(Measurement.date).\
        order_by(Measurement.date.desc()).first()
    
    # convert most recent to datetime obj and find date of one year prior
    most_recent_obs = dt.strptime(most_recent[0], '%Y-%m-%d')
    year_ago_date = most_recent_obs - td(days=365)

    # Query the last year's observation dates and precipitation
    last_12_months = session.query(Measurement.date, Measurement.prcp).\
        order_by(Measurement.date).\
            filter(Measurement.date >= year_ago_date).all()

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

    """Return jsonified data of all stations in the database"""

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # query for all the station data
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


@app.route("/api/v1.0/tobs")
def tobs():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the dates and temperature observations of the most-active station for the previous year of data.

    # Find the most active station
    most_active_station = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()

    session.close()

    # set the number of the most active station to a variable
    most_active_no = most_active_station[0]

    # find last observation date
    last_obs_date = session.query(Measurement.date).\
        order_by(Measurement.date.desc()).\
            filter(Measurement.station == most_active_no).first()

    # convert most recent to datetime obj and find date of one year prior using timedelta
    last_obs = dt.strptime(last_obs_date[0], '%Y-%m-%d')
    year_ago_date = last_obs - td(days=365)

    # query dates and temperatures
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= year_ago_date).\
            filter(Measurement.station == most_active_no).all()

    # create a list and append a dictionary with resutls information to append to the list
    most_active_tobs = [{"station": most_active_no}]
    for date, tobs in results:
        station_dict = {}
        station_dict["date"] = date
        station_dict["temperature"] = tobs
        most_active_tobs.append(station_dict)

    # Return a JSON list of temperature observations for the previous year.
    return jsonify(most_active_tobs)


# ---DYNAMIC ROUTES---
@app.route("/api/v1.0/<start>")
def start_var(start):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # validate exist and dates are in the range of the dataset
    date_check = session.query(func.min(Measurement.date), func.max(Measurement.date)).all()

    if start < date_check[0][0] or start > date_check[0][1]:
        session.close()
        return "ERROR: start is either not within range of the dataset, or not formatted as YYY-MM-DD"
    
    """
        Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

        For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

        If date is out of range, return a 404 error "no data found in this range"
    """
    
    # query the data and find min, max, avg from start date to end of data
    get_start_info = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    # create a resutls list adn append a dict of the results
    results = []

    start_dict = {
        "start_date": start,
        "TMIN": get_start_info[0][0],
        "TMAX": get_start_info[0][1],
        "TAVG": get_start_info[0][2]
    }
    results.append(start_dict)

    return jsonify(results)



@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

    # Validate start date is before end date, and they exist
    if start > end:
        return "Error: either start date is after end date or either date is not foramtted as YYY-MM-DD."

    """
        Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

        For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
    """

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # validate exist and dates are in the range of the dataset
    date_check = session.query(func.min(Measurement.date), func.max(Measurement.date)).all()

    if start < date_check[0][0] or start > date_check[0][1]:
        session.close()
        return "ERROR: start is either not within range of the dataset, or not formatted as YYY-MM-DD"
    elif end > date_check[0][1]:
        session.close()
        return "ERROR: end is either not within range of the dataset, or not formatted as YYY-MM-DD"

    # Query DB for min, max and avg of temps for dates between, inclusive of the provided start and end.
    get_tobs_info = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Close session
    session.close()

    # create results list
    results = []

    # add start and end dates to a dict for results
    dates = {
        "start_date": start,
        "end_date": end
    }

    results.append(dates)

    # create dict using query results
    start_end_results = {
        "TAVG": get_tobs_info[0][2],
        "TMAX": get_tobs_info[0][1],
        "TMIN": get_tobs_info[0][0]        
    }
    results.append(start_end_results)

    return jsonify(results)



if __name__ == '__main__':
    app.run(debug=True)