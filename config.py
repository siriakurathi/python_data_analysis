'''
Module to store config that gets used across the
Flask App as well as the utility script that ingests
data into DB
'''
import os

from flask import Flask

SQL_DB_NAME = "app.db"

WEATHER_DATA_DIR = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "data", "wx_data"
)
TEST_WEATHER_DATA_DIR = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "data", "test_wx_data"
)
YIELD_DATA_FILE = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "data", "yld_data", "US_corn_grain_yield.txt"
)

DEFAULT_PAGE = 1
DEFAULT_PAGE_LIMIT = 10
MAX_PAGE_LIMIT = 100

app = Flask(__name__)
