from flask import Flask, render_template

app = Flask(__name__)
app.config.update(TEMPLATES_AUTO_RELOAD=True)

@app.route('/')
def root():
    return render_template('homepage.html', page_name="Projects")


@app.route('/projects/<project_name>')
def project_management(project_name):
	return render_template('project_management.html', page_name=project_name)

@app.route('/analytics')
def dashboard():
	return render_template('dashboard.html', page_name="Analytics")