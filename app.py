from flask import Flask, render_template, request, redirect, url_for, flash, session
from user import User  # Importing the User class
from quiz import Quiz  # Importing the Quiz class

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Route for the home page after sign-in
@app.route('/')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('signin'))

# Route for sign-up
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

# Route for sign-in
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

# Route for starting a quiz
@app.route('/start_quiz')
def start_quiz():
    if 'user_id' in session:
        quiz = Quiz(session['user_id'])
        return render_template('quiz.html', quiz=quiz)
    else:
        return redirect(url_for('signin'))

# Route to submit the movie score
@app.route('/submit_score', methods=['POST'])
def submit_score():
    if 'user_id' in session:
        score = request.form['score']
        quiz = Quiz(session['user_id'])
        quiz.give_score(int(score))
        flash('Score submitted!', 'success')
        return redirect(url_for('start_quiz'))  # Redirect to the next quiz round
    else:
        return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(debug=True)