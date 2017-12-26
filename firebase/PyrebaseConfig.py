
import pyrebase

class PyrebaseConfig:

    def __init__(self):
	'''
	    "serviceAccount": "D:/AutonomousDrivingAndy/firebaseAdminKey"
                                             +"/firebase-adminsdk.json"	
	'''
        config = {"apiKey": "YOUR_API_KEY",
                    "authDomain": "AAA.firebaseapp.com",
                    "databaseURL": "AAA.firebaseio.com",
                    "storageBucket": "AAA.appspot.com",
                    "serviceAccount": "YOUR_PATH"}   
        firebase = pyrebase.initialize_app(config=config)
        auth = firebase.auth()

        # Authenticate a User
        user = auth.sign_in_with_email_and_password("MAIL", "PASSWORDS")

        #Id Token shall be refresh in 1 hour.
        self.user = auth.refresh(user['refreshToken'])

	
        self.db = firebase.database()
        self.db.child("direction").set("ANN Connecting", self.user['idToken'])

    #POST method that set value on Firebase
    def postData(self, param):
        # Pass the user's id Token to the post method
        self.db.child("ANN").set(param, self.user['idToken'])