from quiz import Quiz
from user import User

def test_user_can_get_watchlist(db_connection):
    connection, cursor = db_connection

    user9 = User("test", "testy", "test9@gmail.com", "!!password!01")
    quiz9 = Quiz(user9.id)

    movieid9 = quiz9.current_movie_id
    print(movieid9)
    moviename9 = quiz9.current_movie_name
    print(moviename9)

    cursor.execute('SELECT title FROM movies WHERE id = %s', (movieid9,))
    result = cursor.fetchone()
    assert result[0] == moviename9