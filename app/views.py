from flask import render_template, request, redirect, url_for, session
from app import app
from app.model import DatabaseHelper

db = DatabaseHelper()

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            db.sign_in(email, password)
            return redirect(url_for('main'))
        except Exception as e:
            return render_template("error.html", error = str(e))
    return render_template("login.html")

@app.route('/main')
def main():
    return render_template('homepage.html', page_name="Projects")

@app.route('/new_project', methods=['POST'])
def new_project():
    if request.method == 'POST':
        project_name = request.form['project_name']
        try:
            db.create_project(project_name)
            return project_name
        except Exception as e:
            return render_template("error.html", error = str(e))

@app.route('/projects/<project_name>')
def project_management(project_name):
    return render_template('project_management.html', page_name=project_name)

@app.route('/analytics')
def dashboard():
    return render_template('dashboard.html', page_name="Analytics")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        try:
            db.create_user(first_name, last_name, email, password)
            db.sign_in(email, password)
            return redirect(url_for('main'))
        except Exception as e:
            return render_template("error.html", error = str(e))
    return render_template('newUser.html', page_name="Create New User")

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    return render_template('forgot_password.html', page_name="Forgot Password?")