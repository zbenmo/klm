from dataclasses import dataclass
from datetime import datetime
from typing import List, Generator
from doctest import testmod


@dataclass
class Booking:
    """
    A single flight booking.
    """
    passenger_name: str # AKA: Pax name
    departure: datetime # given in UTC 
    itenerary: List[str] # a list of IATA codes

    def __repr__(self) -> str:
        itenerary_nice = '->'.join(self.itenerary)
        return f'Passenger name: {self.passenger_name}, departure: {self.departure}, itenerary: "{itenerary_nice}"'


def sublist_in_list(sublist: List, test_list: List) -> bool:
    """
    Helper function to check a sublist is in a test list or not (used below in select_bookings_by_sequential_airports_couple).

    >>> sublist_in_list([1, 2], [4, 1, 2])
    True
    >>> sublist_in_list([1, 2], [4, 2, 1])
    False
    >>> sublist_in_list([1, 2], [1, 4, 2])
    False
    """

    return any(test_list[idx : idx + len(sublist)] == sublist
        for idx in range(len(test_list) - len(sublist) + 1))


class FlightsSchedule:
    pass


class FlightsSchedule:
    """
    A collection of Bookings, with some facilities to add/query the bookings.
    Disclaimer: current implementation is linear in the number of bookings,
    and assumes not a very long itenerary. 
    """
    def __init__(self):
        self.bookings = []

    def add_booking(self, booking:Booking) -> FlightsSchedule:
        "Adds a single booking to the collection."
        "This call is chainable."

        assert f"received itenerary with length {len(booking.itenerary)}", len(booking.itenerary) < 10 
        assert f"booking length is already {len(self.bookings)}", len(self.bookings) < 1000
        self.bookings.append(booking)
        return self

        # TODO: if turns out to be used when a bigger number of bookings, prepare and maintain a few data structures,
        # and keep those updated on each insertion, as an idea (or cache the results).
        # For example, keep a dict (defaultdict(list)) from each possible sequence pair of airports -
        # to a list of bookings for which this pair is found as a sequence:
        # for booking in self.booking:
        #   for idx in range(len(booking) - 2 + 1)):
        #       d[(booking[idx], booking[idx + 1])].append(booking)    
        # or (in addition) sort the bookings by departure date
        # (do that with some caching mechanism that forces it to sort after each addition or at least before next query),
        # and do a binary search when asked based on departure.   

    def select_bookings_by_latest_departure_time(self, departs_before:datetime) -> Generator[FlightsSchedule, None, None]:
        "Assumes the departs_before as UTC."

        yield from (booking for booking in self.bookings if booking.departure < departs_before)

    def select_bookings_by_sequential_airports_couple(self, airport1:str, airport2:str) -> Generator[FlightsSchedule, None, None]:
        "Assumes airport1 and airport2 are IATA codes."

        sequence_to_search = [airport1, airport2]
        yield from (booking for booking in self.bookings if sublist_in_list(sequence_to_search, booking.itenerary))

def date_from_string(input_str: str) -> datetime:
    "helper function for below test (main)"

    return datetime.strptime(
        input_str, r'%b-%d %H:%M %Y')


def test1():
    """
    Tests some the code above.

    >>> test1()
    1
    Passenger name: Alice, departure: 2020-05-26 06:45:00, itenerary: "LHR->AMS"
    2
    Passenger name: Alice, departure: 2020-05-26 06:45:00, itenerary: "LHR->AMS"
    3
    Passenger name: Alice, departure: 2020-05-26 06:45:00, itenerary: "LHR->AMS"
    Passenger name: Bruce, departure: 2020-06-04 11:04:00, itenerary: "GVA->AMS->LHR"
    Passenger name: Cindy, departure: 2020-06-06 10:00:00, itenerary: "AAL->AMS->LHR->JFK->SFO"
    Passenger name: Derek, departure: 2020-06-12 08:09:00, itenerary: "AMS->LHR"
    """

    flights_schedule = FlightsSchedule()

    example_flights = """Alice, May-26 06:45 2020, LHR->AMS
    Bruce, Jun-04 11:04 2020, GVA->AMS->LHR
    Cindy, Jun-06 10:00 2020, AAL->AMS->LHR->JFK->SFO
    Derek, Jun-12 08:09 2020, AMS->LHR
    Erica, Jun-13 20:40 2020, ATL->AMS->AAL
    Fred, Jun-14 09:10 2020, AMS->CDG->LHR"""

    for line in example_flights.split('\n'):
        parts = [x.strip() for x in line.split(',')]
        assert 3 == len(parts)
        flights_schedule.add_booking(Booking(parts[0], date_from_string(parts[1]), parts[2].split('->')))

    print(1)
    for booking in flights_schedule.select_bookings_by_sequential_airports_couple("LHR", "AMS"):
        print(booking)

    print(2)
    for booking in flights_schedule.select_bookings_by_sequential_airports_couple("LHR", "AMS"):
        print(booking)

    print(3)
    for booking in flights_schedule.select_bookings_by_latest_departure_time(date_from_string("Jun-12 08:15 2020")):
        print(booking)


if __name__ == "__main__":
    testmod(name ='test1', verbose = True)