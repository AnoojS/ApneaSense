import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Initialize Firebase Admin SDK with the service account credentials
cred = credentials.Certificate("apneasense-firebase-adminsdk-qnoel-f8581c7b8f.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://apneasense-default-rtdb.firebaseio.com/'
})

# Get a reference to the Firebase Realtime Database
ref = db.reference('/')

# Push data to the database
data = {
    'name': 'John Doe',
    'age': 30,
    'email': 'john@example.com'
}
ref.push(data)

# Retrieve data from the database
snapshot = ref.get()
print(snapshot)