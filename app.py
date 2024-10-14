from flask import Flask, render_template, request, redirect, url_for, flash, session
from user import User  # Importing the User class
from quiz import Quiz  # Importing the Quiz class

def create_app():
    app = Flask(__name__)
    
    # Configurations (e.g., database setup)
    app.config.from_mapping(
        TESTING=True,
        SECRET_KEY="your-secret-key",
    )
    
    # Routes for the app
    @app.route('/')
    def home():
        if 'user_id' in session:
            user = User.get_user_by_id(session['user_id'])  # Fetch the user object using the session user_id
            user.return_watchlist()  # Retrieve the user's watchlist
            return render_template('home.html', user_email=user.email, watchlist=user.watchlist)  # Pass the watchlist to the template
        else:
            return redirect(url_for('signin'))

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            fname = request.form['fname']
            lname = request.form['lname']
            email = request.form['email']
            password = request.form['password']

            try:
                new_user = User(fname, lname, email, password) 
                flash('User created successfully!', 'success')
                return redirect(url_for('signin'))
            except ValueError as e:
                flash(str(e), 'danger')

        return render_template('signup.html')

    @app.route('/signin', methods=['GET', 'POST'])
    def signin():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            # Check if the user exists and password matches
            try:
                user = User.signin(email, password)
                session['user_id'] = user.id  # Store user ID in session
                flash('Signed in successfully!', 'success')
                return redirect(url_for('home'))  # Redirect to home page after sign-in
            except ValueError as e:
                flash(str(e), 'danger')

        return render_template('signin.html')
    
    @app.route('/signout')

    def signout():
        # Remove the user from the session if they are logged in
        session.pop('user_id', None)  # Remove the 'user_id' from the session
        flash('You have been signed out successfully.', 'success')
        return redirect(url_for('signin'))


    @app.route('/start_quiz')
    def start_quiz():
        if 'user_id' in session:
            quiz = Quiz(session['user_id'])
            user = User.get_user_by_id(session['user_id'])
            return render_template('quiz.html', quiz=quiz, user_email=user.email)  # Pass user_email to the template
        else:
            return redirect(url_for('signin'))
    
    @app.route('/end_quiz')
    def end_quiz():        
        return redirect(url_for('home'))

        

    @app.route('/submit_score', methods=['POST'])
    def submit_score():
        if 'user_id' in session:
            score = request.form['score']
            movie_id = request.form['movie_id']

            if score == "unwatched":
                flash('Movie marked as unwatched.', 'info')
            else:
                # Convert the score to an integer and save it
                quiz = Quiz(session['user_id'])
                quiz.current_movie_id = movie_id  # Set the movie being rated
                quiz.give_score(int(score))

            return redirect(url_for('start_quiz'))  # Redirect to the next quiz round
        else:
            return redirect(url_for('signin'))

    @app.route('/add_to_watchlist', methods=['POST'])
    def add_to_watchlist():
        if 'user_id' in session:
            quiz = Quiz(session['user_id'])
            quiz.add_to_watchlist()  # Call the method to add the movie to the watchlist
            return redirect(url_for('start_quiz'))  # Redirect to the next quiz round
        else:
            return redirect(url_for('signin'))

    @app.route('/add_to_unwatched', methods=['POST'])
    def add_to_unwatched():
        if 'user_id' in session:
            quiz = Quiz(session['user_id'])
            quiz.add_to_unwatched()  # Call the method to add the movie to the watchlist
            return redirect(url_for('start_quiz'))  # Redirect to the next quiz round
        else:
            return redirect(url_for('signin'))

    return app  # Return the app instance

if __name__ == '__main__':
    app = create_app()  # Initialize the app using the factory function
    app.run(debug=True)