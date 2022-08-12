'''
Module that hosts all the database models
'''
from database import db

class Weather(db.Model):
    '''
    Class to host Weather table
    '''
    __tablename__ = 'weather'
    date = db.Column(db.String(8), primary_key=True)
    station_id = db.Column(db.String(11), primary_key=True)
    max_temp = db.Column(db.Float, nullable=False)
    min_temp = db.Column(db.Float, nullable=False)
    precipitation = db.Column(db.Float, nullable=False)

    def __init__(self,
        date=None,
        station_id=None,
        max_temp=None,
        min_temp=None,
        precipitation=None
    ):
        self.date = date
        self.station_id = station_id
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.precipitation = precipitation

    def __repr__(self):
        return f'<Weather: \
            {self.date} \
            {self.station_id} \
            {self.max_temp} \
            {self.min_temp} \
            {self.precipitation}>'


class WeatherStats(db.Model):
    '''
    Class to host Weather Stats table
    '''
    __tablename__ = 'weather_stats'
    year = db.Column(db.String(4), primary_key=True)
    station_id = db.Column(db.String(11), primary_key=True)
    avg_max_temp = db.Column(db.Float, nullable=False)
    avg_min_temp = db.Column(db.Float, nullable=False)
    total_precipitation = db.Column(db.Float, nullable=False)
    count = db.Column(db.Integer, nullable=False)

    def __init__(self,
        year=None,
        station_id=None,
        avg_max_temp=None,
        avg_min_temp=None,
        total_precipitation=None
    ):
        self.year = year
        self.station_id = station_id
        self.avg_max_temp = avg_max_temp
        self.avg_min_temp = avg_min_temp
        self.total_precipitation = total_precipitation
        self.count = 1

    def __repr__(self):
        return f'<WeatherStats: \
            {self.year} \
            {self.station_id} \
            {self.avg_max_temp} \
            {self.avg_min_temp} \
            {self.total_precipitation}>'


class CornYield(db.Model):
    '''
    Class to host Corn Yield table
    '''
    __tablename__ = 'corn_yield'
    year = db.Column(db.String(4), primary_key=True)
    corn_yield = db.Column(db.Integer, nullable=False)

    def __init__(self,
        year=None,
        corn_yield=None
    ):
        self.year = year
        self.corn_yield = corn_yield

    def __repr__(self):
        return f'<CornYield: \
            {self.year} \
            {self.corn_yield}>'
