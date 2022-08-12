'''
Script that ingests both the weather & yield data from text files
into database.
'''
import time
from os import listdir
from os.path import isfile, join, splitext
from re import split

from config import WEATHER_DATA_DIR, YIELD_DATA_FILE
from database import db
from models import CornYield, Weather, WeatherStats


def get_weather_values(line):
    '''
    Function to parse the line from weather data file
    and get the date, max temp, min temp & precipitation values.
    In case there are any invalid values or a line with more than two columns,
    entire row is ignored
    '''
    line = line.strip()
    cols = split(r'\s+', line)
    if len(cols) != 4:
        print("Found invalid row, continuing with next")
        return (False, None, None, None, None)
    if '-9999' in cols:
        print("Found missing values, skipping row")
        return (False, None, None, None, None)
    return (True, cols[0], cols[1], cols[2], cols[3])


def update_weather_stats(station_id, year, max_temp, min_temp, precipitation):
    '''
    Function to populate weather_stats table.
    If there is already an existing year & station_id row, we will get it first
    and update the cols with updated averages and commit the updated row.
    If there is no existing row, a new entry will be inserted.
    '''
    try:
        rec = WeatherStats.query.\
            filter(WeatherStats.year == year, WeatherStats.station_id == station_id).first()
        if rec:
            # Record already exists for the given year and station_id, update the stats
            # Formula to update the average with a new value
            # new_avg = old_avg + ((new_value - old_avg)/(old_count + 1))
            rec.avg_max_temp += (max_temp - rec.avg_max_temp)/(rec.count + 1)
            rec.avg_min_temp += (min_temp - rec.avg_min_temp)/(rec.count + 1)
            rec.total_precipitation = rec.total_precipitation + precipitation
            rec.count += 1
        else:
            # No record exists, insert a new one.
            ws_rec = WeatherStats(
                station_id = station_id,
                year = year,
                avg_max_temp = max_temp,
                avg_min_temp = min_temp,
                total_precipitation = precipitation,
            )
            db.session.add(ws_rec)
        db.session.commit()
    except Exception as err: # pylint: disable=broad-except
        print("Error updating weather stats:", err)


def update_weather_tables(station_id, date, max_temp, min_temp, precipitation):
    '''
    Insert a new row in weather table with passed in input arguments
    Will skip inserting a new value for an already existing date & station_id combo.
    '''
    try:
        w_rec = Weather(
            station_id = station_id,
            date = date,
            max_temp = max_temp,
            min_temp = min_temp,
            precipitation = precipitation,
        )
        db.session.add(w_rec)
        db.session.commit()
    except Exception as err: # pylint: disable=broad-except
        print("Data already present in table, skipping:", err)
    else:
        # We update stats only when we successfully updated a weather etnry
        # Using /10 for precipation because we want to centimeters for average
        # whereas the data passed in is in millimeters
        update_weather_stats(station_id, date[:4], max_temp, min_temp, precipitation/10)


def ingest_weather_data(data_dir):
    '''
    Function that takes in the directory containing weather data files one for each
    station, file name without the prefix is considered as the station ID.
    '''
    start_time = time.time()
    files = [f for f in listdir(data_dir) if isfile(join(data_dir, f))]

    for file in files:
        station_id = splitext(file)[0]
        with open(join(data_dir,file), encoding='utf-8') as file_h:
            for line in file_h:
                (valid, date, max_temp, min_temp, precipitation) = get_weather_values(line)
                if not valid:
                    continue
                # we are using /10 for all measurements because
                # they are documented as tenths of degree celcius and tenths of millimeeters
                update_weather_tables(
                    station_id,
                    date,
                    float(max_temp)/10,
                    float(min_temp)/10,
                    float(precipitation)/10
                )

    print("Time taken to run the update weather and weather stats data into DB in seconds: ",
        time.time() - start_time)


def get_corn_yield_values(line):
    '''
    Function to parse the line from corn yield data file
    and get the year & yield values.
    In case there are any invalid values or a line with more than two columns,
    entire row is ignored
    '''
    line = line.strip()
    cols = split(r'\s+', line)
    if len(cols) != 2:
        print("Found invalid row, continuing with next")
        return (False, None, None)
    if '-9999' in cols:
        print("Found missing values, skipping row")
        return (False, None, None)
    return (True, cols[0], cols[1])


def update_corn_yield_tables(year, corn_yield):
    '''
    Insert a new row in corn_yield table with passed in input arguments
    Will skip inserting a new value for an already existing year.
    '''
    try:
        cy_rec = CornYield(
            year = year,
            corn_yield = corn_yield,
        )
        db.session.add(cy_rec)
        db.session.commit()
    except Exception as err: # pylint: disable=broad-except
        print("Data already present in table, skipping:", err)


def ingest_yield_data(yield_data_file):
    '''
    Function that reads corn yield data text file from file system and
    updates the table 'corn_yield' in database.
    '''
    start_time = time.time()
    with open(yield_data_file, encoding='utf-8') as file_h:
        for line in file_h:
            (valid, year, corn_yield) = get_corn_yield_values(line)
            if not valid:
                continue
            update_corn_yield_tables(year, int(corn_yield))
    print("Time taken to run the update corn yield data into DB in seconds: ",
        time.time() - start_time)


if __name__ == "__main__":
    db.drop_all() # TODO: Added this so the script can be run multiple times
    db.create_all()
    ingest_weather_data(WEATHER_DATA_DIR)
    ingest_yield_data(YIELD_DATA_FILE)
