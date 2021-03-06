{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "import datetime as dt\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "\n",
    "import sqlalchemy\n",
    "from sqlalchemy.ext.automap import automap_base\n",
    "from sqlalchemy.orm import Session\n",
    "from sqlalchemy import create_engine, func\n",
    "from flask import Flask, jsonify"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Setup database\n",
    "\n",
    "engine = create_engine(\"sqlite:///hawaii.sqlite\")\n",
    "\n",
    "# reflect an existing database into a new model\n",
    "Base = automap_base()\n",
    "\n",
    "# reflect the tables\n",
    "\n",
    "Base.prepare(engine, reflect = True)\n",
    "\n",
    "# Save references to each table\n",
    "measurement = Base.classes.measurement\n",
    "\n",
    "station = Base.classes.station\n",
    "\n",
    "# Create our session (link) from Python to the DB\n",
    "session = Session(engine)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Flask Setup\n",
    "app = Flask(__name__)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Flask Route\n",
    "@app.route(\"/\")\n",
    "def welcome():\n",
    "    return(\n",
    "    f\"Hawaii Climate Analysis<br/>\"\n",
    "    f\"Available Routes: <br/>\"\n",
    "    f\"/api/v1.0/precipitation<br/>\"\n",
    "    f\"/api/v1.0/stations<br/>\"\n",
    "    f\"/api/v1.0/tobs<br/>\"\n",
    "    f\"/api/v1.0/start/end\"\n",
    ")\n",
    "\n",
    "@app.route(\"/api/v1.0/precipitation\")\n",
    "def precipitation():\n",
    "    \n",
    "    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days = 365)\n",
    "    \n",
    "    target_scores = session.query(measurement.date, measurement.prcp).\\\n",
    "        filter(measurement.date > year_ago).all()\n",
    "    \n",
    "    #Dictionary with date as key and precipitation as value\n",
    "    \n",
    "    precipitation = {date:prcp for date, prcp in precipitation}\n",
    "    return jsonify(precipitation)\n",
    "\n",
    "@app.route(\"/api/v1.0/stations\")\n",
    "def stations():\n",
    "    results = session.query(station.station).all()\n",
    "    \n",
    "    stations = list(np.ravel(results))\n",
    "    return jsonify(stations=stations)\n",
    "\n",
    "@app.route(\"/api/v1.0/tobs\")\n",
    "def tobs():\n",
    "    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days = 365)\n",
    "    \n",
    "    results = session.query(measurement.tobs).\\\n",
    "        filter(measurement.stations == 'USC00519281').\\\n",
    "        filter(measurement.date >= year_ago).all()\n",
    "    \n",
    "    temperature = list(np.ravel(results))\n",
    "        \n",
    "    return jsonify(temperature = temperature)\n",
    "\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
