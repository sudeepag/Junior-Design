import pyrebase

FIREBASE_CREDENTIALS = {
	apiKey: "AIzaSyDpcs6rtT7S0e0W8u5tYrhHZWvaW7P_gUE",
    authDomain: "writers-bloc.firebaseapp.com",
    databaseURL: "https://writers-bloc.firebaseio.com",
    projectId: "writers-bloc",
    storageBucket: "writers-bloc.appspot.com",
    messagingSenderId: "59932670136"
}

class DatabaseHelper:

	def __init(self):
		self.firebase = pyrebase.initialize_app(FIREBASE_CREDENTIALS)
		self.db = self.firebase.database()
		self.auth = self.firebase.auth()
		self.storage = self.firebase.storage()

	def sign_in(self, email, password):
		dbuser = self.auth.sign_in_with_email_and_password(email, password)
		self.user = User(dbuser['localId'], dbuser['idToken'])
		print('Successful login: %s' % email)

	def sign_out(self):
		self.user = None

class User:

	def __init__(self, id, token):
		self.id = id
		self.token = token