import pyrebase
firebaseConfig={'apiKey': "AIzaSyA6Z74zq2kRkWjYJcWXPS7LicKgxWxBs9o",
  'authDomain': "authfyp-b643c.firebaseapp.com",
    'databaseURL':"https://authfyp-b643c-default-rtdb.firebaseio.com/",
  'projectId': "authfyp-b643c",
  'storageBucket': "authfyp-b643c.appspot.com",
  'messagingSenderId': "441682951949",
  'appId': "1:441682951949:web:16e539cd911e7b0f49ba44",
  'measurementId': "G-22RT0ZLY2W"}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()


def signUp(email, password, name):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        print(user)
        id_token = user['idToken']
        print(id_token)

        # Store additional user data in the database
        user_data = {
            "name": name
        }
        db.child("users").child(user['localId']).set(user_data)

        return "Successfully Signed Up"
    except Exception as e:
        print("Error occurred:", str(e))


def login(email, password):
    try:
        login = auth.sign_in_with_email_and_password(email, password)
        print("Logged In")
        user_id = login['localId']

        # Retrieve the user data from the database
        user_data = db.child("users").child(user_id).get().val()
        name = user_data.get("name")
        return name
    except Exception as e:
        print("Error occurred:", str(e))



