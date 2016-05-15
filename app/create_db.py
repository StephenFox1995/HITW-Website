import sqlite3
import sys
import config
import os
# Creates all the tabe within the database.

CREATE_EVENT_TABLE_STMT = '''CREATE TABLE 'Event' (
	event_id INTEGER PRIMARY KEY NOT NULL,
	event_title VARCHAR,
	event_location VARCHAR NOT NULL,
	event_date DATE NOT NULL,
	event_time TIME NOT NULL
);'''

CREATE_MEMBER_TABLE_STMT = '''CREATE TABLE 'Member' (
	member_id INTEGER PRIMARY KEY  NOT NULL,
	member_f_name VARCHAR NOT NULL,
	member_l_name VARCHAR NOT NULL,
	member_handicap VARCHAR NOT NULL
);'''

CREATE_RESULT_TABLE_STMT = '''CREATE TABLE 'Result' (
	event_id INTEGER,
	member_id INTEGER,
    score INTEGER,
	FOREIGN KEY(event_id) REFERENCES EVENT(event_id),
	FOREIGN KEY(member_id) REFERENCES Member(member_id)
);'''

CREATE_EVENT_IMAGE_TABLE_STMT = '''CREATE TABLE 'EventImage' (
	event_id INTEGER,
	image_data STRING,
	FOREIGN KEY(event_id) REFERENCES EVENT(event_id)
);'''


# TRIGGERS
# --------------
# Removes all results for a member if that member was deleted from the database
DELETE_MEMBER_FROM_RESULTS_TRIGGER = '''CREATE TRIGGER delete_member_from_results
BEFORE DELETE ON Member
FOR EACH ROW
BEGIN
    DELETE FROM Result WHERE member_id = OLD.member_id;
END'''

DELETE_RESULT_FOR_EVENT_TRIGGER = '''CREATE TRIGGER delete_results_from_event
BEFORE DELETE ON Event
FOR EACH ROW
BEGIN
    DELETE FROM Result WHERE event_id = OLD.event_id;
END'''




def create_event_table(connection):
    try:
        cursor = None
        cursor = connection.cursor()
        cursor.execute(CREATE_EVENT_TABLE_STMT)
    except sqlite3.Error, e:
        print "ERORR: There was an error creating table 'Event'"
    else:
        print "TABLE: 'Event' created successfully"


def create_member_table(connection):
    try:
        cursor = None
        cursor = connection.cursor()
        cursor.execute(CREATE_MEMBER_TABLE_STMT)
    except sqlite3.Error, e:
        print "ERORR: There was an error creating table 'Member'"
    else:
        print "TABLE: 'Member' created successfully"


def create_result_table(connection):
    try:
        cursor = None
        cursor = connection.cursor()
        cursor.execute(CREATE_RESULT_TABLE_STMT)
    except sqlite3.Error, e:
        print "ERORR: There was an error creating table 'Result'"
    else:
        print "TABLE: 'Result' created successfully"

def create_event_image_table(connection):
	try:
		cursor = None
		cursor = connection.cursor()
		cursor.execute(CREATE_EVENT_IMAGE_TABLE_STMT)
	except sqlite3.Error, e:
		print "ERROR: There was an error creating table 'EventImage'"
	else:
		print "TABLE: 'EventImage' create successfully"




def create_triggers(connection):
	try:
		cursor = connection.cursor()
		cursor.execute(DELETE_MEMBER_FROM_RESULTS_TRIGGER)
		cursor.execute(DELETE_RESULT_FOR_EVENT_TRIGGER)
	except sqlite3.Error, e:
		print 'ERROR: There was a errror creating triggers.'
		print "Reason: ", e
	else:
		print 'Trigges created successfully.'




# TODO: if a table already exists in the etc/hitw/config
# 		remeber to delete that entry so there's no duplicates.

# Creates the database and all the tables needed.
def create_sqlite_db(filepath):
	connection = None
	connection = sqlite3.connect(filepath)

	# Change so we can write to as
	# the script is needed to be executed in superuser mode.
	os.system('sudo chmod g+w ' + filepath)

	create_event_table(connection)
	create_member_table(connection)
	create_result_table(connection)
	create_event_image_table(connection)
	create_triggers(connection)
	connection.close()


def parse_args():
	args = ()
	db_filepath = sys.argv[1]
	fbapp_key = sys.argv[2]
	# return the filepath and facebook key from the arguments.
	args = (db_filepath, fbapp_key)
	return args

# Parse the filepath so the db can be create there.
args = parse_args()

config.write_db_filepath(args[0])
# config.write_fb_app_key(args[1])

# Now create the sqlite db at that filepath.
create_sqlite_db(args[0])
