# Imports
import psycopg
from psycopg import ProgrammingError


# SQL Call
def execute(conn, query):
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            row = cur.fetchone()
            conn.commit()
            if row:
                return row
    except ProgrammingError:
        return "Error"


# Execute sql query, return multiple rows
def executeMulti(conn, query):
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            row = cur.fetchall()
            conn.commit()
            if row:
                return row
    except ProgrammingError:
        return "Error"


# Init DB
def reinit():
    # Connect to db
    conn = psycopg.connect(
        "postgresql://fdurca:5kk6SvI9LGmNRosjvP03CA@hackwestern9-6731.5xj.cockroachlabs.cloud:26257/HackWestern9?sslmode=verify-full",
        application_name="$ init_db_UGH")

    # Create DB
    queries = [
        # Clear out any existing data
        "DROP TABLE IF EXISTS event CASCADE",
        # CREATE the messages table
        "CREATE TABLE IF NOT EXISTS event (meetingID UUID PRIMARY KEY DEFAULT gen_random_uuid(), meetingName STRING, slide STRING)",
        # INSERT a row into the messages table
        "INSERT INTO event (meetingID, meetingName, slide) VALUES ('3cbd3999-c314-409b-bac0-4cca90d1b6ec', 'gdfdf', 'TESTSLIDE')",
        # Clear out any existing data
        "DROP TABLE IF EXISTS slide",
        # CREATE the slide table
        "CREATE TABLE IF NOT EXISTS slide (meetingID UUID NOT NULL REFERENCES event (meetingID), slideNum INT, note STRING)",
        # INSERT a row into the slide table
        "INSERT INTO slide (meetingID, slideNum, note) VALUES('3cbd3999-c314-409b-bac0-4cca90d1b6ec', 1, 'testSlide')",
    ]

    # Run queries
    count = 0
    for query in queries:
        count += 1
        print(count, ": ", end="")
        print(execute(conn, query))

    # Close connection
    conn.close()