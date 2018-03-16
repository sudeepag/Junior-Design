from flask import render_template, request, redirect, url_for, session
from app import app
from app.model import DatabaseHelper, User
from flask.ext.login import LoginManager, UserMixin, login_required, login_user, logout_user 

db = DatabaseHelper()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            db.sign_in(email, password)
            login_user(db.user)
            return redirect(url_for('main'))
        except Exception as e:
            return render_template("error.html", error = str(e))
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/main')
@login_required
def main():
    return render_template('homepage.html', page_name="Projects", projects=db.user.projects)

@app.route('/new_project', methods=['POST'])
@login_required
def new_project():
    if request.method == 'POST':
        project_name = request.form['project_name']
        try:
            db.create_project(project_name)
            return project_name
        except Exception as e:
            return render_template("error.html", error = str(e))

@app.route('/new_goal', methods=['POST'])
def new_goal():
	if request.method == 'POST':
		project_name = request.form['project_name']
		goal_name = request.form['goal_name']
		try:
			db.create_goal(project_name, goal_name)
			return goal_name
		except Exception as e:
			return render_template("error.html", error = str(e))

@app.route('/complete_goal', methods=['POST'])
def complete_goal():
	if request.method == 'POST':
		project_name = request.form['project_name']
		goal_name = request.form['goal_name']
		try:
			db.complete_goal(project_name, goal_name)
			return goal_name
		except Exception as e:
			return render_template("error.html", error = str(e))

@app.route('/revert_goal', methods=['POST'])
def revert_goal():
	if request.method == 'POST':
		project_name = request.form['project_name']
		goal_name = request.form['goal_name']
		try:
			db.revert_goal(project_name, goal_name)
			return goal_name
		except Exception as e:
			return render_template("error.html", error = str(e))

@app.route('/projects/<project_id>')
@login_required
def project_management(project_id):
    print(project_id)
    project = db.project_for_id(project_id)
    print(project)
    return render_template('project_management.html', page_name=project['name'], project=project)

@app.route('/analytics')
@login_required
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
    return render_template('register.html', page_name="Create New User")

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    return render_template('forgot_password.html', page_name="Forgot Password?")

# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    try:
        return db.user
    except:
        return None