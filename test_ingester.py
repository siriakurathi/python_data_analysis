from config import TEST_WEATHER_DATA_DIR
from database import db
from models import Weather, WeatherStats
from ingester import ingest_weather_data
from sqlalchemy import or_

def clean_test_data():
    recs = Weather.query.filter(or_(Weather.station_id=="test1", Weather.station_id=="test2")).all()
    for rec in recs:
        db.session.delete(rec)
    db.session.commit()
    recs = WeatherStats.query.filter(or_(WeatherStats.year=="1915", WeatherStats.year=="1916")).all()
    for rec in recs:
        db.session.delete(rec)
    db.session.commit()


def setup_function():
    clean_test_data()
    db.create_all()
    ingest_weather_data(TEST_WEATHER_DATA_DIR)

def test_weather_total_entries():
    '''
    Tests whether all the test data is ingested into weather table
    '''
    recs = Weather.query.filter(or_(Weather.station_id=="test1", Weather.station_id=="test2")).all()
    # test1 station has 10 entries but one has invalid value -9999 so 9 should've been inserted
    # test2 station has 20 entries
    assert len(recs) == 29

def test_weather_stats_total_entries():
    '''
    Tests whether all the test data is ingested into weather stats table
    '''
    recs = WeatherStats.query.filter(or_(WeatherStats.year=="1915", WeatherStats.year=="1916")).all()
    # 1915, test1 should've one average entry
    # 1915, test2 should've one average entry
    # 1916, test2 should've one more average entry
    assert len(recs) == 3

def test_correct_stats_are_stored():
    '''
    Tests whether the averages are calculated correctly
    '''
    rec = WeatherStats.query.filter(or_(WeatherStats.year=="1915", WeatherStats.station_id=="test1")).first()
    assert (rec.avg_max_temp - 2.4) < 0.000000000009 # Floats are difficult to compare
    rec = WeatherStats.query.filter(or_(WeatherStats.year=="1915", WeatherStats.station_id=="test2")).first()
    assert (rec.total_precipitation - 0.51) < 0.000000000009 # Floats are difficult to compare


def teardown_function():
    clean_test_data()

