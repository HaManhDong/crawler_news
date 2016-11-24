import database_connection
la_time_session = database_connection.create_database_and_connect('latimes')

first_entry= la_time_session.query(database_connection.NewsData).first()
print first_entry.content
pass
