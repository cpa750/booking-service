from models.Bookmark import Bookmark
from models.Customer import Customer
from models.Location import Location
from models.Reservation import Reservation

from util.Database import Database

import Pyro5.server


@Pyro5.server.expose
class Service:
    def __init__(self):
        self.__db = Database("./data/database.db")
        self.current_customer_id = ""

    def create_customer(self, customer_id, name, phone_no):
        customer = Customer(self.__db, customer_id, name, phone_no)
        # Returns false if the customer already exists to inform the client.
        # Returns true for a successful creation.
        return not customer.in_db

    def set_customer(self, customer_id):
        customer = Customer(self.__db, customer_id)
        if customer.in_db:
            self.current_customer_id = customer.customer_id

    def make_bookmark(self, location_id):
        Bookmark(self.__db, self.current_customer_id, location_id)

    def make_reservation(self, location_id, start, end):
        reservation = Reservation(db=self.__db, customer_id=self.current_customer_id,
                                  location_id=location_id, start=start, end=end)
        if reservation.inserted:
            return self.__db.get_last_insert_id()
        else:
            return False

    def update_reservation_end(self, reservation_id, new_end):
        reservation = Reservation(db=self.__db, reservation_id=reservation_id)
        reservation.update_end(new_end)

    def get_location_details(self, location_id):
        location = Location(self.__db, location_id)
        if location.exists:
            return [location.name, location.address, location.email]
        else:
            return False

    def checkout(self):
        customer = Customer(self.__db, self.current_customer_id)
        if customer.get_no_of_reservations() > 0:
            return True
        else:
            return False

    def get_all_location_ids(self):
        query_string = "SELECT id FROM Location"
        return self.__db.read(query_string, ())

    def reset_db(self):
        self.__db.reset_db()


def get_args():
    import sys
    if len(sys.argv) < 3:
        return False
    else:
        return sys.argv[1], int(sys.argv[2])


if __name__ == "__main__":
    import Pyro5.core

    args = get_args()
    if args:
        daemon = Pyro5.server.Daemon(host=args[0], port=args[1])
    else:
        daemon = Pyro5.server.Daemon()

    nameserver = Pyro5.core.locate_ns()
    uri = daemon.register(Service)
    print(uri)
    nameserver.register("bookingservice", uri)
    daemon.requestLoop()
