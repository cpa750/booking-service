import os
import sqlite3
from typing import Iterable


class Database:
    def __init__(self, db_name: str):
        if not os.path.exists(db_name):
            self.__connection = sqlite3.connect(db_name)
            self.__cursor = self.__connection.cursor()
            self.__create_tables()
        else:
            self.__connection = sqlite3.connect(db_name)
            self.__cursor = self.__connection.cursor()

    def __del__(self):
        self.__connection.close()

    def __create_tables(self):
        statements = (
            """
            CREATE TABLE Customer
            (id TEXT PRIMARY KEY UNIQUE,
            custName TEXT,
            phoneNo TEXT)
            """,
            """
            CREATE TABLE Location
            (id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
            name TEXT,
            address TEXT,
            email TEXT)
            """,
            """
            CREATE TABLE Bookmark
            (customerId TEXT,
            locationId INT,
            FOREIGN KEY(customerId) REFERENCES Customer(id),
            FOREIGN KEY(locationId) REFERENCES Location(id),
            PRIMARY KEY (customerId, locationId)) 
            """,
            """
            CREATE TABLE Reservation
            (id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
            customerId TEXT,
            locationId INT,
            start TEXT,
            end TEXT,
            FOREIGN KEY(customerId) REFERENCES Customer(id),
            FOREIGN KEY(locationId) REFERENCES Location(id))
            """
        )
        for statement in statements:
            self.__cursor.execute(statement)
        self.__connection.commit()
        self.__insert_dummy_locations()

    def __insert_dummy_locations(self):
        # Normally this wouldn't be done. However, in the context of a
        # case study, dummy values for locations are needed.
        locations = (
            ("name1", "address1", "email1"),
            ("name2", "address2", "email2"),
            ("name3", "address3", "email3"),
            ("name4", "address4", "email4")
        )
        for location in locations:
            query_string = "INSERT INTO Location (name, address, email) VALUES (?, ?, ?)"
            self.write(query_string, location)

    def reset_db(self):
        # This is only to make taking measurements for the case study easier
        # DO NOT DO THIS IN A PRODUCTION SERVICE
        tables = ("Customer", "Location", "Bookmark", "Reservation")
        query_string = "DROP TABLE "
        for table in tables:
            self.__cursor.execute(query_string + table)
        self.__connection.commit()
        self.__create_tables()

    def get_last_insert_id(self):
        return self.__cursor.lastrowid

    def write(self, query_string: str, arguments: Iterable):
        self.__cursor.execute(query_string, arguments)
        self.__connection.commit()

    def read(self, query_string: str, arguments: Iterable):
        self.__cursor.execute(query_string, arguments)
        return self.__cursor.fetchall()
