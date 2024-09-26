from flask import Flask, render_template, request, redirect, url_for, flash
from user import User  # Importing the User class

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for sign-up
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']

        try:
            # Create a new user
            new_user = User(fname, lname, email, password)
            flash('User created successfully!', 'success')
            return redirect(url_for('index'))  # Redirect to home page after successful sign-up
        except ValueError as e:
            # Flash error message if validation fails
            flash(str(e), 'danger')

    return render_template('signup.html')

# Placeholder for sign-in route (to be implemented later)
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    flash('Sign-in functionality will be added soon!', 'info')
    return render_template('signin.html')

if __name__ == '__main__':
    app.run(debug=True)