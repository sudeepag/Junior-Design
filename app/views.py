from flask import Flask, render_template
from app import app

# app = Flask(__name__)
# app.config.update(TEMPLATES_AUTO_RELOAD=True)

@app.route('/')
def root():
    return render_template('homepage.html', page_name="Projects")

@app.route('/projects/<project_name>')
def project_management(project_name):
	return render_template('project_management.html', page_name=project_name)

@app.route('/analytics')
def dashboard():
	return render_template('dashboard.html', page_name="Analytics")

@app.route('/login')
def login():
	return render_template('login.html', page_name="Login")

@app.route('/newUser')
def newUser():
	return render_template('newUser.html', page_name="Create New User")