# Imports

from venv import create
import psycopg
import hackw.noteTranslation as noteTranslation
from .utils import execute, executeMulti, reinit

# Global variables
slides = {}
audio = {}


# Creates an event and adds it to the database
def createEvent(eventName, slide):
    # Connect to db
    conn = psycopg.connect(
        "postgresql://fdurca:5kk6SvI9LGmNRosjvP03CA@hackwestern9-6731.5xj.cockroachlabs.cloud:26257/HackWestern9?sslmode=verify-full",
        application_name="$ init_db")

    # Create DB
    query = "INSERT INTO event (meetingName, slide) VALUES ('" + eventName + "', '" + slide + "')"

    # Run queries
    execute(conn, query)

    # Get eventID
    query = "SELECT meetingID FROM event WHERE meetingName='" + eventName + "' AND slide='" + slide + "'"

    # Run queries
    meetingID = execute(conn, query)

    # Insert into slide count
    slides[meetingID] = 0

    # TO DO - audio[meetingID] =

    # Close connection
    conn.close()

    return getEventDetails(meetingID)

# Get all for testing purposes
def getAll():
    # Connect to db
    conn = psycopg.connect(
        "postgresql://fdurca:5kk6SvI9LGmNRosjvP03CA@hackwestern9-6731.5xj.cockroachlabs.cloud:26257/HackWestern9?sslmode=verify-full",
        application_name="$ init_db")

    # Get eventID
    query = "SELECT * FROM event"

    # Run queries
    reply = executeMulti(conn, query)

    # Close connection
    conn.close()

    return reply


# Creates an event and adds it to the database
def getEventDetails(eventID):
    # Connect to db
    conn = psycopg.connect(
        "postgresql://fdurca:5kk6SvI9LGmNRosjvP03CA@hackwestern9-6731.5xj.cockroachlabs.cloud:26257/HackWestern9?sslmode=verify-full",
        application_name="$ select_db")

    # Create DB
    query = "SELECT meetingName, slide FROM event WHERE meetingID='" + str(eventID) + "'"

    # Run queries
    reply = execute(conn, query)

    # Close connection
    conn.close()

    # Return reply
    return reply


# Create note summary
def summarySlide(meetingID, audio):
    # Summarize slide
    summary = noteTranslation.summary(audio)

    # Increment slide count
    slides[meetingID] = slides[meetingID] + 1

    # Add text
    audio[meetingID].append(summary)

    # Add to db
    # Connect to db
    conn = psycopg.connect(
        "postgresql://fdurca:5kk6SvI9LGmNRosjvP03CA@hackwestern9-6731.5xj.cockroachlabs.cloud:26257/HackWestern9?sslmode=verify-full",
        application_name="$ select_db")

    # Create DB
    query = "INSERT INTO slide (meetingID, slideNum, note) VALUES (" + meetingID + ", " + slides[meetingID] + ", " + summary + ")"

    # Run queries
    execute(conn, query)

    # Close connection
    conn.close()


# Test DB
def tester():
    reinit()
    print("Success")
    createEvent("tester1", "tester2")
    print(getEventDetails('3cbd3999-c314-409b-bac0-4cca90d1b6ec'))

