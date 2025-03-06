from utils.utils import create_trip_data
from _datetime import datetime

def test_create_trip_data():
    trip = create_trip_data("London", ["Afternoon", "Evening"], "Couple")

    assert (trip.date_created == datetime.now().strftime("%Y-%m-%d")
            and trip.date_of_trip == datetime.now().strftime("%Y-%m-%d")
            and trip.custom_name == "Trip to London"
            and trip.city == "London"
            and trip.time_of_day == "Afternoon,Evening"
            and trip.group == "Couple")
