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
        self.user.projects = []
        res = self.db.child('users').child(self.user.id).child('projects').get().val()
        if res:
            if type(res) == dict:
                res = [res]
            for r in res:
                if r is not None:
                    self.user.projects.append(r)
            for project in self.user.projects:
                print(project)

    def create_user(self, first_name, last_name, email, password):
        db_user = self.auth.create_user_with_email_and_password(email, password)
        data = {"first_name": first_name, "last_name": last_name, "email": email}
        self.db.child("users").child(db_user['localId']).set(data)

    def create_project(self, name):
        time = str(datetime.datetime.now())
        id = self.user.generate_project_id()
        data = {"id": id, "user_id": self.user.id, "name": name, "current_goal_id": "None",
                "creation_date": time, "last_updated": time, "contributions": [], "goals": []}
        self.db.child("users").child(self.user.id).child("projects").child(id).set(data)
        # new_project = Project(len(self.user.projects), name, self.user.id, data["current_goal_id"],
        #                       data["creation_date"], data["creation_date"], data["words"], data["goals"])
        self.user.projects.append(data)
        print('Successful creation of a new project!', data)
        return id

    def delete_project(self, project_id):
        self.db.child("users").child(self.user.id).child("projects").child(project_id).remove()
        self.user.project_ids.remove(project_id)
        print('Successful removal of a project!')

    def create_goal(self, project_id, name, goal_type):
        print("creating goal for ", str(project_id))
        res = self.db.child('users').child(self.user.id).child('projects').child(project_id).child('goals').get().val()
        id = 0
        if res is not None:
            while id in [g['id'] for g in res]:
                id += 1
        print("id ", id)
        time = str(datetime.datetime.now())
        data = {"id": id, "user_id": self.user.id, "project_id": project_id, "name": name, "type": goal_type, "creation_date": time, "completed": False}
        self.db.child("users").child(self.user.id).child("projects").child(project_id).child("goals").child(id) \
            .set(data)
        print("set data in firebase")
        self.user.projects[project_id]['goals'][id] = data
        # self.user.projects.goals.append(data)
        # print("updated goals list: \n ", self.user.projects.project_id.goals)

    def complete_goal(self, project_id, goal_id):
        self.db.child("users").child(self.user.id).child("projects").child(project_id).child("goals").child(goal_id) \
            .child("completed").set(True)
        print('Successful completion of a goal!\n%s' % str(goal_id))

    def revert_goal(self, project_id, goal_id):
        self.db.child("users").child(self.user.id).child("projects").child(project_id).child("goals").child(goal_id) \
            .child("completed").set(False)
        print('Successful reverted a goal!\n%s' % str(goal_id))

    def create_contribution(self, project_id, goal_id, work_type, work_count):
        print("creating contribution for ", str(goal_id))
        res = self.db.child('users').child(self.user.id).child('projects') \
                    .child(project_id).child('goals').child(goal_id).child("contributions") \
                    .get().val()

        id = 0
        if res is not None:
            while id in [c['id'] for c in res]:
                id += 1
        print("id ", id)
        time = str(datetime.datetime.now())
        data = {"id": id, "user_id": self.user.id, "project_id": project_id, \
                "goal_id": goal_id, "creation_date": time, "work_count": work_count,
                 "work_type": work_type}
        self.db.child("users").child(self.user.id).child("projects").child(project_id) \
            .child("goals").child(goal_id).child("contributions").child(id) \
            .set(data)

        self.db.child("users").child(self.user.id).child("projects").child(project_id) \
            .child("last_updated")

        # self.db.child("users").child(self.user.id).child("projects").child(project_id) \
        #     .child("last_updated")

        print("set data in firebase")

    def project_for_id(self, id):
        print('finding project for id', id)
        for project in self.user.projects:
            if str(project['id']) == id:
                return project
        return None

    def weekDay(self, year, month, day):
        offset = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
        week   = ['Sunday', 
                  'Monday', 
                  'Tuesday', 
                  'Wednesday', 
                  'Thursday',  
                  'Friday', 
                  'Saturday']
        afterFeb = 1
        if month > 2: afterFeb = 0
        aux = year - 1700 - afterFeb
        # dayOfWeek for 1700/1/1 = 5, Friday
        dayOfWeek  = 5
        # partial sum of days betweem current date and 1700/1/1
        dayOfWeek += (aux + afterFeb) * 365                  
        # leap year correction    
        dayOfWeek += aux / 4 - aux / 100 + (aux + 100) / 400     
        # sum monthly and day offsets
        dayOfWeek += offset[month - 1] + (day - 1)               
        dayOfWeek %= 7
        return dayOfWeek, week[int(dayOfWeek)]

    def insights_for_project(self, project):
        goals = project['goals']
        contributions = []
        for g in goals:
            if 'contributions' in g:
                for c in g['contributions']:
                    contributions.append(c)
        
        insights = []

        
        for c  in contributions:

            t = int(c['creation_date'].split(' ')[-1].split(':')[0])

            # Time of day
            morning = 0
            afternoon = 0
            night = 0
            if 0 < t < 12:
                morning += 1
            elif 12 <= t < 17:
                afternoon += 1
            elif 17 <= t <= 24:
                night += 1

            # Day of week
            mon = 0
            tue = 0
            wed = 0
            thurs = 0
            fri = 0
            sat = 0
            sun = 0

            y = int(c['creation_date'].split(' ')[0].split('-')[0])
            m = int(c['creation_date'].split(' ')[0].split('-')[1])
            d = int(c['creation_date'].split(' ')[0].split('-')[2])
            print(y, m, d)
            day = self.weekDay(y, m, d)
            if day == 'Monday':
                mon += 1
            elif day == 'Tuesday':
                tue += 1
            elif day == 'Wednesday':
                wed += 1
            elif day == 'Thursday':
                thurs += 1
            elif day == 'Friday':
                fri += 1
            elif day == 'Saturday':
                sat += 1
            elif day == 'Sunday':
                sun += 1
            print(c)

            pages = 0
            words = 0
            paragraphs = 0
            if c['work_type'] == 'pages':
                pages += 1
            elif c['work_type'] == 'words':
                words += 1
            elif c['work_type'] == 'paragraphs':
                paragraphs += 1

        max_t = max([morning, afternoon, night])
        if max_t == morning:
            insights.append("You're most productive in the morning. Rise and shine!")
        elif max_t == afternoon:
            insights.append("You're most productive in the afternoon.")
        elif max_t == night:
            insights.append("You're most productive at night. Time to burn the midnight oil!")

        max_d = max([mon, tue, wed, thurs, fri, sat, sun])
        if max_d == mon:
            insights.append("Mondays are your best work days.")
        elif max_d == tue:
            insights.append("Tuesdays are your best work days.")
        elif max_d == wed:
            insights.append("Wednesdays are your best work days.")
        elif max_d == thurs:
            insights.append("Thursdays are your best work days.")
        elif max_d == fri:
            insights.append("Fridays are your best work days.")
        elif max_d == sat:
            insights.append("Saturdays are your best work days.")
        elif max_d == sun:
            insights.append("Sundays are your best work days.")

        max_w = max([pages, words, paragraphs])
        if max_w == pages:
            insights.append("You tend to contribute mostly in pages.")
        elif max_w == words:
            insights.append("You tend to contribute mostly in words.")
        elif max_w == paragraphs:
            insights.append("You tend to contribute mostly in paragraphs.")
        return insights

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

    def generate_project_id(self):
        i = 0
        while i in [p['id'] for p in self.projects]:
            i += 1
        return i

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
    def __init__(self, id, name, user_id, current_goal_id, goal_type, creation_date, last_updated, words, paragraphs, pages, completed):
        self.id = id
        self.name = name
        self.user_id = user_id
        self.current_goal_id = current_goal_id
        self.type = goal_type
        self.creation_date = creation_date
        self.last_updated = last_updated
        self.words = words
        self.paragraphs = paragraphs
        self.pages = pages
        self.completed = completed

    def __repr__(self):
        return 'id: {}\nname:{} \nuser_id: {}\ncurrent_goal_id: {}\ngoal_type: {}\ncreation_date: {}\nlast_updated: {}\nself.words: {}\nself.paragraphs: {}\nself.pages: {}\nself.completed: {}' \
            .format(self.id, self.name, self.user_id, self.current_goal_id, self.goal_type,
                    self.creation_date, self.last_updated, self.words, self.paragraphs, self.pages, self.completed)
