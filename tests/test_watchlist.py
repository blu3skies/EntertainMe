from quiz import Quiz
from user import User

def test_user_can_get_watchlist():
    user8 = User("test", "testy", "test8@gmail.com", "!!password!01")
    quiz8 = Quiz(user8.id)

    film81 = quiz8.current_movie_id
    quiz8.add_to_watchlist()
    quiz8.give_score(9)
    film82 = quiz8.current_movie_id
    quiz8.add_to_watchlist()
    user8.return_watchlist()

    assert user8.watchlist == [film81, film82] 

