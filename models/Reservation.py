import datetime

from util.Database import Database


class Reservation:
    def __init__(self, db: Database, reservation_id: int = None, customer_id: str = "",
                 location_id: int = -1, start: datetime.date = "", end: datetime.date = ""):
        self.__db = db
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.location_id = location_id
        self.start = start
        self.end = end
        self.__exists = False
        self.inserted = False
        if reservation_id is not None:
            self.__get_from_database()
        if not self.__exists and reservation_id is None:
            self.__write_to_db()

    def __get_from_database(self):
        rows = self.__db.read("SELECT * FROM Reservation WHERE id = ?",
                              (self.reservation_id,))
        if len(rows) > 0:
            self.customer_id = rows[0][1]
            self.location_id = rows[0][2]
            self.start = rows[0][3]
            self.end = rows[0][4]
            self.__exists = True

    def __write_to_db(self):
        query_string = "INSERT INTO Reservation (customerId, locationId, start, end) VALUES (?, ?, ?, ?)"
        self.__db.write(query_string,
                        (self.customer_id, self.location_id, self.start, self.end))
        self.__exists = True
        self.inserted = True

    def update_end(self, new_end):
        self.location_id = new_end
        if self.__exists:
            query_string = "UPDATE Reservation SET end = ?"
            self.__db.write(query_string, (self.end,))
