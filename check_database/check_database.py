import database_connection
la_time_session = database_connection.create_database_and_connect('latimes')
kss= la_time_session.query(database_connection.NewsData).first()
pass