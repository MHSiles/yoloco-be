from firebase_admin import credentials, initialize_app, storage
import json

f = open('firebase.json')
# returns JSON object as 
# a dictionary
data = json.load(f)

# Init firebase with your credentials
cred = credentials.Certificate(data)
initialize_app(cred, {'storageBucket': 'yoloco-cbd6b.appspot.com'})

# Put your local file path 
fileName = "output7.pdf"
bucket = storage.bucket()
blob = bucket.blob(fileName)
blob.upload_from_filename(fileName)

# Opt : if you want to make public access from the URL
blob.make_public()

print("your file url", blob.public_url)