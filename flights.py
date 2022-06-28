from dataclasses import dataclass
from datetime import datetime
from typing import List, Generator
from doctest import testmod
from collections import defaultdict


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
        self.airport_sequence_dict = defaultdict(list)

    def add_booking(self, booking:Booking) -> FlightsSchedule:
        "Adds a single booking to the collection."
        "This call is chainable."

        # assumption it shouldn't happen. Iteneraries are not longer than 9.
        assert f"received itenerary with length {len(booking.itenerary)}", len(booking.itenerary) < 10

        self.bookings.append(booking)
        self.register_sequential_airport_couples(booking)

        return self

    def register_sequential_airport_couples(self, booking:Booking):
        seen = set()
        for airport1, airport2 in zip(booking.itenerary[:-1], booking.itenerary[1:]):
            pair = (airport1, airport2)
            assert pair not in seen # just to verify assumption of no duplications
            seen.add(pair)
            self.airport_sequence_dict[pair].append(booking)    

    def select_bookings_by_latest_departure_time(self, departs_before:datetime) -> Generator[FlightsSchedule, None, None]:
        "Assumes the departs_before as UTC."
        "Linear time with respect to number of bookings"

        yield from (booking for booking in self.bookings if booking.departure < departs_before)

    def select_bookings_by_sequential_airports_couple(self, airport1:str, airport2:str) -> Generator[FlightsSchedule, None, None]:
        "Assumes airport1 and airport2 are IATA codes."

        pair = (airport1, airport2)
        yield from self.airport_sequence_dict[pair]


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
    Passenger name: Bruce, departure: 2020-06-04 11:04:00, itenerary: "GVA->AMS->LHR"
    Passenger name: Cindy, departure: 2020-06-06 10:00:00, itenerary: "AAL->AMS->LHR->JFK->SFO"
    Passenger name: Derek, departure: 2020-06-12 08:09:00, itenerary: "AMS->LHR"
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
    for booking in flights_schedule.select_bookings_by_sequential_airports_couple("AMS", "LHR"):
        print(booking)

    print(3)
    for booking in flights_schedule.select_bookings_by_latest_departure_time(date_from_string("Jun-12 08:15 2020")):
        print(booking)


if __name__ == "__main__":
    testmod(name ='test1', verbose = True)