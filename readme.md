<h1>Release Notes</h1>

<h2>New Features</h2>

1. Track progress of goal completion for each project.
2. Distinguish between Drafting and Revising goals.
3. Delete projects you may no longer need.

<h2>Bug Fixes</h2>

1. Fixed an issue where different types of work were not being tracked correctly.
2. Fixed an issue where the goals were not being added to "in progress" properly.

<h2>Known Issues</h2>

1. When there are two projects, a "None" goal appears when deleting the first project in the list.
2. When adding work to a new goal and immediately clicking on "Analysis" you may be sent to an error page.
3. Goals and work backend are not updating as quickly as the frontend, requiring a refresh.
4. Deleting contribution does not work.

<h1>Install Guide</h1>

The site is hosted on Heroku and can be accessed with this link:

https://writers-bloc.herokuapp.com/login

If you want to run it locally, first clone the repository:

https://github.com/sudeepag/Junior-Design.git

View the [Flask setup guide](http://flask.pocoo.org/docs/0.12/installation/) to install flask and pip.

Before working on the project, type `. venv/bin/activate`.

For first time setup, in your terminal:

1. Run `pip install -r requirements.txt` once the virtual environment has been activated.
2. Type `export FLASK_APP=main.py`
3. Type `py run.py`, must be using python 3
4. Visit localhost:5000
