'''
Flask Application module that serves API endpoints
'''
from flask import jsonify, request

from config import DEFAULT_PAGE, DEFAULT_PAGE_LIMIT, MAX_PAGE_LIMIT, app
from models import CornYield, Weather, WeatherStats


def get_paging_args(args):
    '''
    Function that parses page & per_page query parmeters within the HTTP GET request
    '''
    page = int(args.get("page")) if args.get("page") else DEFAULT_PAGE
    per_page = min(MAX_PAGE_LIMIT,
        int(args.get("per_page")) if args.get("per_page") else DEFAULT_PAGE_LIMIT)
    return (page, per_page)

def get_weather_api_args(args):
    '''
    Function to parse request query parmeters for /api/weather route
    '''
    date = args.get("date")
    station_id = args.get("station_id")
    (page, per_page) = get_paging_args(args)
    return (date, station_id, page, per_page)

def get_weather_stats_api_args(args):
    '''
    Function to parse request query parmeters for /api/weather/stats route
    '''
    year = args.get("year")
    station_id = args.get("station_id")
    (page, per_page) = get_paging_args(args)
    return (year, station_id, page, per_page)

def get_corn_yield_api_args(args):
    '''
    Function to parse request query parmeters for /api/yield route
    '''
    year = args.get("year")
    (page, per_page) = get_paging_args(args)
    return (year, page, per_page)


@app.route("/api/weather", methods=['GET'])
def get_weather():
    '''
    Function that handles weather API
    '''
    (date, station_id, page, per_page) = get_weather_api_args(request.args)
    qry = None
    if date and station_id:
        qry = Weather.query.filter(Weather.date == date, Weather.station_id == station_id)
    elif date:
        qry = Weather.query.filter(Weather.date == date)
    elif station_id:
        qry = Weather.query.filter(Weather.station_id == station_id)
    else:
        qry = Weather.query

    records = []
    res_dict = {
        "data" : records
    }
    recs = None
    try:
        recs = qry.paginate(page=page, per_page=per_page)
    except Exception as err:
        print("Invalid request", err)
        return jsonify(res_dict)

    for rec in recs.items:
        records.append({
            "date" : rec.date,
            "station_id" : rec.station_id,
            "max_temp" : rec.max_temp,
            "min_temp" : rec.min_temp,
            "precipitation" : rec.precipitation,
        })
    res_dict["data"] = records
    return jsonify(res_dict)


@app.route("/api/weather/stats", methods=['GET'])
def get_weather_stats():
    '''
    Function that handles weather stats API
    '''
    (year, station_id, page, per_page) = get_weather_stats_api_args(request.args)
    qry = None
    if year and station_id:
        qry = WeatherStats.query.\
            filter(WeatherStats.year == year, WeatherStats.station_id == station_id)
    elif year:
        qry = WeatherStats.query.filter(WeatherStats.year == year)
    elif station_id:
        qry = WeatherStats.query.filter(WeatherStats.station_id == station_id)
    else:
        qry = WeatherStats.query

    records = []
    res_dict = {
        "data" : records
    }
    recs = None
    try:
        recs = qry.paginate(page=page, per_page=per_page)
    except Exception as err:
        print("Invalid request", err)
        return jsonify(res_dict)

    for rec in recs.items:
        records.append({
            "year" : rec.year,
            "station_id" : rec.station_id,
            "avg_max_temp" : rec.avg_max_temp,
            "avg_min_temp" : rec.avg_min_temp,
            "total_precipitation" : rec.total_precipitation,
        })
    res_dict["data"] = records
    return jsonify(res_dict)


@app.route("/api/yield", methods=['GET'])
def get_corn_yield():
    '''
    Function that handles yield API
    '''
    (year, page, per_page) = get_corn_yield_api_args(request.args)
    qry = None
    if year:
        qry = CornYield.query.filter(CornYield.year == year)
    else:
        qry = CornYield.query

    records = []
    res_dict = {
        "data" : records
    }
    recs = None
    try:
        recs = qry.paginate(page=page, per_page=per_page)
    except Exception as err:
        print("Invalid request", err)
        return jsonify(res_dict)

    for rec in recs.items:
        records.append({
            "year" : rec.year,
            "corn_yield" : rec.corn_yield,
        })
    res_dict["data"] = records
    return jsonify(res_dict)
