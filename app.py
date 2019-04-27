import io
import os
import json
from flask import Flask, render_template, request, redirect, jsonify
from werkzeug import secure_filename
from google.oauth2 import service_account
from google.cloud import vision
from google.cloud.vision import types
from google.cloud import translate

# Pycharm local env
# from pathlib import Path
# from dotenv import load_dotenv
# load_dotenv()
# env_path = Path('.') / '.env'
# load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

# Gets credentials
# May have to comment out to get to work locally
credentials_raw = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
service_account_info = json.loads(credentials_raw)
credentials = service_account.Credentials.from_service_account_info(service_account_info)

# Vision client
vision_client = vision.ImageAnnotatorClient(credentials=credentials)
# Translate client
translate_client = translate.Client(credentials=credentials)

@app.route('/')
def index():
	languages = translate_client.get_languages()
	return render_template("index.html", languages=languages)

@app.route('/image', methods=['POST'])
def vision_api():
	if request.method == 'POST':
		f = request.files['file']
		content = f.read()

	# Reads in image to object
	image = types.Image(content=content)

	# Performs label detection on the image object
	response = vision_client.label_detection(image=image)
	labels = response.label_annotations

	# TODO: return proper json object with keys and values
	label_str = ""
	for label in labels:
		label_str += label.description

	#return render_template("index.html")
	return label_str

def translate_api(word, translate_to):
	result = translate_client.translate(word, target_language=translate_to, source_language="en")
	return result

if __name__ == '__main__':
	app.run()
