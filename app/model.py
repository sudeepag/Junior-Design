import pyrebase
import datetime


FIREBASE_CREDENTIALS = {
    'apiKey': "AIzaSyDpcs6rtT7S0e0W8u5tYrhHZWvaW7P_gUE",
    'authDomain': "writers-bloc.firebaseapp.com",
    'databaseURL': "https://writers-bloc.firebaseio.com",
    'projectId': "writers-bloc",
    'storageBucket': "writers-bloc.appspot.com",
    'messagingSenderId': "59932670136",
    'serviceAccount': 'app/writers-bloc-firebase-adminsdk-0pw3s-3084128171.json'
}

class DatabaseHelper:
    def __init__(self):
        self.firebase = pyrebase.initialize_app(FIREBASE_CREDENTIALS)
        self.db = self.firebase.database()
        self.auth = self.firebase.auth()
        self.storage = self.firebase.storage()

    def sign_in(self, email, password):
        auth_user = self.auth.sign_in_with_email_and_password(email, password)
        db_user = self.db.child("users").child(auth_user['localId']).get()
        # TODO: Add better error handling here
        if db_user:
            self.user = User(auth_user['localId'], auth_user['idToken'], db_user.val()['first_name'],
                             db_user.val()['last_name'], db_user.val()['email'])
            print('Successful login!\n%s' % str(self.user))
        self.fetch_projects()

    def sign_out(self):
        self.user = None

    def fetch_projects(self):
        res = self.db.child('users').child(self.user.id).child('projects').get().val()
        if res:
            if type(res) == dict:
                res = [res]
            for r in res:
                self.user.projects.append(r)
            for project in self.user.projects:
                print(project)

    def create_user(self, first_name, last_name, email, password):
        db_user = self.auth.create_user_with_email_and_password(email, password)
        data = {"first_name": first_name, "last_name": last_name, "email": email}
        self.db.child("users").child(db_user['localId']).set(data)

    def create_project(self, name):
        time = str(datetime.datetime.now())
        id = len(self.user.projects)
        data = {"id": id, "user_id": self.user.id, "name": name, "current_goal_id": "None",
                "creation_date": time, "last_updated": time, "contributions": [], "goals": []}
        self.db.child("users").child(self.user.id).child("projects").child(id).set(data)
        # new_project = Project(len(self.user.projects), name, self.user.id, data["current_goal_id"],
        #                       data["creation_date"], data["creation_date"], data["words"], data["goals"])
        self.user.projects.append(data)
        print('Successful creation of a new project!')

    def delete_project(self, project_id):
        # time = str(datetime.datetime.now())
        # id = len(self.user.projects)
        # data = {"id": id, "user_id": self.user.id, "name": name, "current_goal_id": "None",
        #         "creation_date": time, "last_updated": time, "contributions": [], "goals": []}
        # self.db.child("users").child(self.user.id).child("projects").child(id).set(data)
        # new_project = Project(len(self.user.projects), name, self.user.id, data["current_goal_id"],
        #                       data["creation_date"], data["creation_date"], data["words"], data["goals"])
        # self.user.projects.remove(project_id)
        # print("project id", project_id)
        # print(self.user.projects)
        # for p in self.user.projects:
        #     print(p.get('id'))
        #     if p.get('id') == project_id:
        #         self.user.projects.remove(p)
        # print(self.user.projects)
        self.db.child("users").child(self.user.id).child("projects").child(project_id).remove()
        print('Successful removal of a project!')

    def create_goal(self, project_id, name):
        print("creating goal for ", str(project_id))
        res = self.db.child('users').child(self.user.id).child('projects').child(project_id).child('goals').get().val()
        if res is None:
            id = 0
        else:
            id = len(res)
        print("id ", id)
        time = str(datetime.datetime.now())
        data = {"id": id, "user_id": self.user.id, "project_id": project_id, "name": name, "creation_date": time, "completed": False}
        self.db.child("users").child(self.user.id).child("projects").child(project_id).child("goals").child(id) \
            .set(data)
        print("set data in firebase")
        # self.user.projects.goals.append(data)
        # print("updated goals list: \n ", self.user.projects.project_id.goals)


    def complete_goal(self, project_id, goal_id):
        self.db.child("users").child(self.user.id).child("projects").child(project_id).child("goals").child(goal_id) \
            .child("completed").set(True)
        print('Successful completion of a goal!\n%s' % str(new_goal))

    def revert_goal(self, project_id, goal_id):
        self.db.child("users").child(self.user.id).child("projects").child(project_id).child("goals").child(goal_id) \
            .child("completed").set(False)
        print('Successful reverted a goal!\n%s' % str(new_goal))

    def project_for_id(self, id):
        for project in self.user.projects:
            if str(project['id']) == id:
                return project
        return None


class User:
    def __init__(self, id, token, first_name, last_name, email):
        self.id = id
        self.token = token
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.projects = []

        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return self.id

    def __repr__(self):
        return 'id: {}\ntoken: {}\nfirst_name: {}\nlast_name: {}\nemail: {}' \
            .format(self.id, self.token, self.first_name, self.last_name, self.email)


class Project:
    def __init__(self, id, name, user_id, current_goal_id, creation_date, last_updated, words, paragraphs, pages):
        self.id = id
        self.name = name
        self.user_id = user_id
        self.current_goal_id = current_goal_id
        self.creation_date = creation_date
        self.last_updated = last_updated
        self.words = words
        self.paragraphs = paragraphs
        self.pages = pages
        self.goals = []

    def __repr__(self):
        return 'id: {}\nname:{} \nuser_id: {}\ncurrent_goal_id: {}\ncreation_date: {}\nlast_updated: {}\nself.words: {}\nself.paragraphs: {}\nself.pages: {}\nself.goals: {}' \
            .format(self.id, self.name, self.user_id, self.current_goal_id, self.creation_date, self.last_updated,
                    self.words, self.paragraphs, self.pages, self.goals)


class Goal:
    def __init__(self, id, name, user_id, current_goal_id, creation_date, last_updated, words, paragraphs, pages, completed):
        self.id = id
        self.name = name
        self.user_id = user_id
        self.current_goal_id = current_goal_id
        self.creation_date = creation_date
        self.last_updated = last_updated
        self.words = words
        self.paragraphs = paragraphs
        self.pages = pages
        self.completed = completed

    def __repr__(self):
        return 'id: {}\nname:{} \nuser_id: {}\ncurrent_goal_id: {}\ncreation_date: {}\nlast_updated: {}\nself.words: {}\nself.paragraphs: {}\nself.pages: {}\nself.completed: {}' \
            .format(self.id, self.name, self.user_id, self.current_goal_id,
                    self.creation_date, self.last_updated, self.words, self.paragraphs, self.pages, self.completed)