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

@app.route('/main', methods=['GET', 'POST'])
@login_required
def main():
    db.fetch_projects()
    render_template('dashboard.html', username=db.user.first_name)
    return render_template('homepage.html', page_name="Projects", user_id=str(db.user.id), projects=db.user.projects, username=db.user.first_name)

@app.route('/new_project', methods=['POST'])
@login_required
def new_project():
    if request.method == 'POST':
        project_name = request.form['project_name']
        try:
            project_id = db.create_project(project_name)
            print('project id', project_id)
            return str(project_id)
        except Exception as e:
            return render_template("error.html", error = str(e))

@app.route('/delete_project', methods=['POST'])
def delete_project():
    if request.method == 'POST':
        project_id = request.form['project_id']
        print("deleting project " + str(project_id))
        try:
            print("deleting project")
            db.delete_project(project_id)
            return project_id
        except Exception as e:
            return render_template("error.html", error = str(e))

@app.route('/new_goal', methods=['POST'])
def new_goal():
    if request.method == 'POST':
        project_id = request.form['project']
        print("project name", project_id)
        goal_name = request.form['goal_name']
        print("goal name ", goal_name)
        goal_type = request.form['goal_type']
        print("goal type ", goal_type)
        try:
            db.create_goal(int(project_id), goal_name, goal_type)
            return goal_name
        except Exception as e:
            return render_template("error.html", error = str(e))

@app.route('/complete_goal', methods=['POST'])
def complete_goal():
    if request.method == 'POST':
        project_id = request.form['project_id']
        goal_id = request.form['goal_id']
        try:
            db.complete_goal(project_id, goal_id)
            return goal_id
        except Exception as e:
            return render_template("error.html", error = str(e))

@app.route('/revert_goal', methods=['POST'])
def revert_goal():
    if request.method == 'POST':
        project_id = request.form['project_id']
        goal_id = request.form['goal_id']
        try:
            db.revert_goal(project_id, goal_id)
            return goal_id
        except Exception as e:
            print(e)
            return render_template("error.html", error = str(e))

@app.route('/add_work', methods=['POST'])
def add_work():
    if request.method == 'POST':
        project_id = request.form['project_id']
        goal_id = request.form['goal_id']
        work_type = request.form['work_type']
        work_count = request.form['work_count']
        try:
            db.create_contribution(project_id, goal_id, work_type, work_count)
            return work_count
        except Exception as e:
            print(e)
            return render_template("error.html", error = str(e))
    return 0

@app.route('/projects/<project_id>')
@login_required
def project_management(project_id):
    project = db.project_for_id(project_id)
    print(project)
    try:
        return render_template('project_management.html', page_name=project['name'], project=project, username=db.user.first_name, num_goals=len(project['goals']))

    except:
        return render_template('project_management.html', page_name=project['name'], project=project, username=db.user.first_name, num_goals=0)

@app.route('/analytics/<project_id>')
@login_required
def analytics(project_id):
    db.fetch_projects()
    project = db.project_for_id(project_id)
    print(project)
    return render_template('analytics.html', page_name=project['name'], project=project, username=db.user.first_name)

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
