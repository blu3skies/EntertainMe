import os
import pymysql
from dotenv import load_dotenv


# Determine which environment to load
env = os.getenv('FLASK_ENV', 'development')  # Default to development if not set

# Load the appropriate .env file based on the environment
if env == 'test':
    load_dotenv('.env.test')
else:
    load_dotenv('.env.development')

# Fetch database credentials from environment variables
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

# Establish the connection using environment variables
connection = pymysql.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name,
    port=3306  # Default port
)

# Create a cursor object to interact with the database
cursor = connection.cursor()
# Example: Create a users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS quiz_results (
        quiz_result_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        movie_id INT NOT NULL,
        score INT CHECK (score BETWEEN 1 AND 10),
        on_watchlist BOOLEAN DEFAULT FALSE,
        unwatched BOOLEAN DEFAULT FALSE,
        quiz_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (movie_id) REFERENCES movies(id)
        );     
''')

# Commit the changes to the database
connection.commit()

# Close the connection
cursor.close()
connection.close()


class Quiz:
    __user_id = ""
    __current_movie_id = ""
    __current_movie_poster = ""
    __current_movie_name = ""

    def __init__(self, user_id):

        self.user_id = user_id
        self.current_movie_id = self.get_movie()
        self.current_movie_poster = self.get_movie_poster()
        self.current_movie_name = self.get_movie_name()

    def get_movie(self):
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=3306
        )

        cursor = connection.cursor()
        cursor.execute('SELECT id FROM movies ORDER BY RAND() LIMIT 1')
        result = cursor.fetchone()
        connection.close()
        return result[0] 
    
    def get_movie_poster(self):
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=3306
        )

        cursor = connection.cursor()
        cursor.execute('SELECT poster_path FROM movies WHERE id =%s', (self.current_movie_id))
        result = cursor.fetchone()
        return "https://image.tmdb.org/t/p/original/" + result[0] 
    
    def get_movie_name(self):
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=3306
        )

        cursor = connection.cursor()
        cursor.execute('SELECT title FROM movies WHERE id =%s', (self.current_movie_id))
        result = cursor.fetchone()
        return result[0] 


    def give_score(self, score):
        # Establish the connection (or use a passed-in cursor/connection object)
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=3306
        )
        cursor = connection.cursor()

        try:
            # Insert the movie score into the quiz_results table
            cursor.execute('''
                INSERT INTO quiz_results (user_id, movie_id, score)
                VALUES (%s, %s, %s)
            ''', (self.user_id, self.current_movie_id, score))
            connection.commit()
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()
        
        self.current_movie_id = self.get_movie()

    def add_to_watchlist(self):
        # Establish the connection (or use a passed-in cursor/connection object)
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=3306
        )
        cursor = connection.cursor()

        try:
            # Insert the movie score into the quiz_results table
            cursor.execute('''
                INSERT INTO quiz_results (user_id, movie_id, on_watchlist)
                VALUES (%s, %s, %s)
            ''', (self.user_id, self.current_movie_id, True))
            connection.commit()
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()
        
        self.current_movie_id = self.get_movie()
        
    def add_to_unwatched(self):
        # Establish the connection (or use a passed-in cursor/connection object)
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=3306
        )
        cursor = connection.cursor()

        try:
            # Insert the movie score into the quiz_results table
            cursor.execute('''
                INSERT INTO quiz_results (user_id, movie_id, unwatched)
                VALUES (%s, %s, %s)
            ''', (self.user_id, self.current_movie_id, True))
            connection.commit()
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()
        
        self.current_movie_id = self.get_movie()

