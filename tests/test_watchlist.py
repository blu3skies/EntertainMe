from quiz import Quiz
from user import User

def test_user_can_get_watchlist():
    user8 = User("test", "testy", "test8@gmail.com", "!!password!01")
    quiz8 = Quiz(user8.id)

    # Step 1: Add the first movie to the watchlist
    film81 = quiz8.current_movie_id  # Save the current movie ID
    quiz8.add_to_watchlist()  # Add the first movie to the watchlist

    # Step 2: Add the second movie to the watchlist
    quiz8.give_score(9)  # Score the first movie and move to the next movie
    film82 = quiz8.current_movie_id  # Save the second movie ID
    quiz8.add_to_watchlist()  # Add the second movie to the watchlist

    # Step 3: Retrieve the watchlist
    user8.return_watchlist()

    # Verify that the movie IDs match the movies in the watchlist
    watchlist_movie_ids = [movie['id'] for movie in user8.watchlist]  # Extract movie IDs from the watchlist
    assert watchlist_movie_ids == [film81, film82]  # Check if the IDs match

