# Description
Project that demonstrates:
- Python automation to ingest data into SQLite database
- Usage of Python unit test framework using Pytest module
- Development of data models to fit real world data
- Ability to analyze data and create new data model for statistics
- Lightweight webservice using Flask to provide data from SQLite
- Provision of safe defaults via pagination method to avoid overload on backend
- Application of auto code formatter with isort python module
- Application of Linter with pylint utility and fixing the issues found
- Usage of coverage module to calcuate test coverage

## Caveats
- Limited tests just to showcase the methodology because of time constraints
    - The same framework used for ingester.py can be extended to Flask app as well
- While ingestion of data, ignored the entire row if any of the values has invalid entry -9999
- While fixed many linter warnings, didn't get chance to make it 100%, with more time it should be doable.
- Currently scripts print out errors and warnings(like duplicate row, missing values) etc to console, 
    with more time this will be handled using `logging` module.
- If the client doesn't specify any page parameters these are the defaults
    ```
    DEFAULT_PAGE = 1
    DEFAULT_PAGE_LIMIT = 10
    MAX_PAGE_LIMIT = 100
    ```
- Right now the ingestion script takes longer, because of instead of batching the weather records and doing
    one commit per station_id, doing an add and commit for each record within the station so that we can keep
    weather stats as well updated using the same routine. 
    This will take longer the first time, but if we have future entries where we need to add invididual records
    via an API, this will be quickest method.
    It's a tradeoff that I chose for this, it should be easily modified to make it a quick batch job but that would
    mean future ingestions of weather data will make weather stats computation more expensive. We have re-read all 
    the existing weather entries and calculate averages.
- Truncating the dataset that is being uploaded as part of the project to avoid repo bloat but still keep the functionality.

# Question Rubric

## Problem 1 - Data Modeling
- All the data models `Weather, WeatherStats, CornYield`can be found in [models.py](models.py)
    These were developed to work with SQLAlchemy ORM and SQLite as the DB.

## Problem 2 - Ingestion
- Using models from above file, [ingester.py](ingester.py) ingests data into SQLite DB
- If the script is run twice, it will ignore the duplicate entries as the primary key
    for Weather data is date + station_id, only first entry with this combo will be filled in
    successfully, if any more rows come with same combo, SQLIntegrity UNIQUE constraint exception
    will be raise, we just print a warning statement to console and proceed with next record.

## Problem 3 - Data Analysis
- `WeatherStats` table holds the stats associated with weather, all the stats are stored per year & station_id combo
    The data is filled in as Weather data is being populated, this way if there are any future additions, WeatherStats are updated as well without having a separate task to recalculate new averages from reading all the
    Weather entries again.
    Formula use to calculate new average: `new_avg = old_avg + ((new_value - old_avg)/(old_count + 1))`

## Problem 4 - REST API
Implemented 3 endpoints that return JSON
- `/api/weather`
    - Query parameters
        - date, station_id, page, per_page
    - All arguments are optional, data will be filtered appropriately when date and/or station_id are provided
    - If both date & station_id are absent, all the records will be returned with pagination
    - page & per_page arguments are honored as provided, if nothing is provided default value for page is 1 and  for per_page is 100
- `/api/weather/stats`
    - Query parameters
        - year, station_id, page, per_page
- `/api/yield`
    - Query parameters
        - year, page, per_page


# Setup to run
- Developed and tested the application on `Mac OSX 11` with `Python 3.8.12`
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## File layout
- [ingester.py](ingester.py) - script responsible for populating both Weather and Yield data sets.
    While populating Weather, it also takes care of updating the Weather stats table that carries the
    average minimum, maximum temperatures and total precipitation.
    Prints out the time taken(in seconds) for each data set ingestion at the end of the script run.

- [test_ingester.py](test_ingester.py) - pytest script that tests basic `ingester.py` functionality

- [app.py](app.py) - Main Flask App file that is responsible for serving all three Web APIs
    - `/api/weather`
    - `/api/weather/stats`
    - `/api/yield`
    This generates the data in JSON format with the main key being `data` that holds all the records
    in a list `{"data" ; [{....}, {......}]}`
    In case of any error or out of all the data while using pagination service returns empty list `{"data" ; []}`

- [database.py](database.py) - Contains code related to initial setup of SQLite DB

- [models.py](models.py) - Contains all the three data models Weather, WeatherStats & CornYield

- [config.py](config.py) - Contains the config that is shared across Flask app as well as the ingester script.

## Data Ingestion

```
(venv) shell % python ingester.py
Found missing values, skipping row
Found missing values, skipping row
.....
....
Found missing values, skipping row
Found missing values, skipping row
Time taken to run the update weather and weather stats data into DB in seconds:  9859.83139204979
Time taken to run the update corn yield data into DB in seconds:  0.14995193481445312
```

## Running web service
```
(venv) shell % flask run
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
127.0.0.1 - - [12/Aug/2022 12:15:06] "GET /api/weather/stats?page=1&per_page=10 HTTP/1.1" 200 -
127.0.0.1 - - [12/Aug/2022 12:15:29] "GET /api/weather/stats?year=1985&page=1&per_page=10 HTTP/1.1" 200 -
......
```

Screenshots of client invocations in browser can be found in [screenshots](screenshots) folder.

## Sample linter run
```
(venv) shell % pylint database.py

-------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 8.57/10, +1.43)


(venv) shell % pylint --load-plugins pylint_flask_sqlalchemy models.py 
************* Module models
....
....
```

## Sample code formatter run
```
(venv) shell % isort .
Fixing config.py
Fixing models.py
Fixing database.py
Fixing app.py
Fixing ingester.py
Skipped 2 files
```

## Sample coverage pytest run
```
(venv) shell % coverage run -m pytest
=========================================== test session starts ===========================================
platform darwin -- Python 3.8.12, pytest-7.1.2, pluggy-1.0.0
rootdir: /localdir/siri/python_data_analysis
collected 3 items                                                                                         

test_ingester.py ...                                                                                [100%]

```

## Sample coverage report run

```
(venv) shell % coverage report -m
Name               Stmts   Miss  Cover   Missing
------------------------------------------------
config.py             10      0   100%
database.py            7      0   100%
ingester.py           81     33    59%   25-26, 62-63, 81-82, 126-134, 142-150, 158-165, 170-173
models.py             42      5    88%   31, 66, 86-87, 90
test_ingester.py      31      0   100%
------------------------------------------------
TOTAL                171     38    78%


(venv) shell % coverage html
Wrote HTML report to htmlcov/index.html
```
