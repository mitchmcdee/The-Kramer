from flask import Flask, render_template, redirect, jsonify, request
from waitress import serve
from PIL import Image
import requests
import time
import os

KEY = '923e32c414a04b14a2ecaec74190760a'
BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'
HEADER = {'Content-Type': 'application/octet-stream', 'Ocp-Apim-Subscription-Key': KEY}

THE_KRAMER            = 'static/images/theKramer.png'
LEFT_CROPPED_KRAMER   = 'static/images/leftCroppedKramer.png'
RIGHT_MASKED_KRAMER   = 'static/images/rightMaskedKramer.png'
RIGHT_CROPPED_KRAMER  = 'static/images/rightCroppedKramer.png'
CENTRE_MASKED_KRAMER  = 'static/images/centreMaskedKramer.png'
CENTRE_CROPPED_KRAMER = 'static/images/centreCroppedKramer.png'

app = Flask(__name__)
faces = []

# Testing, pls remove
testImage = open('static/images/smiling.png', 'rb')
r = requests.post(BASE_URL, headers=HEADER, data=testImage)
x1, y1, x2, y2 = tuple(r.json()[0]['faceRectangle'].values())
im = Image.open(testImage)
face = im.crop((y1,x1,y1+y2,x1+x2))
face.thumbnail((210, 210), Image.ANTIALIAS)

################################################################################

# Get kramer image
def getKramer(faceInfo, position):
    user, face = faceInfo
    faceHash = tuple([user, position])
    filename = 'static/images/' + ''.join(faceHash) + '.png'
    if os.path.exists(filename):
        return filename

    masked = Image.open(RIGHT_MASKED_KRAMER if position == 'r' else CENTRE_MASKED_KRAMER)
    cropped = Image.open(RIGHT_CROPPED_KRAMER if position == 'r' else CENTRE_CROPPED_KRAMER)

    background = Image.new("RGBA", masked.size)
    background.paste(face, (180,310))
    final = Image.new("RGBA", masked.size)
    while (True):
        try:
            final = Image.alpha_composite(final, cropped)
            final = Image.alpha_composite(final, background)
            final = Image.alpha_composite(final, masked)
        except:
            print('fek')
            pass
        else:
            break

    final.save(filename)
    return filename

# Webhook to add face to server log
@app.route('/_getKramers', methods=['POST'])
def getKramers():
    kramers = []

    if len(faces) == 0:
        kramers.append(THE_KRAMER)
    else:
        kramers.append(LEFT_CROPPED_KRAMER)

    for i, face in enumerate(faces):
        if i == len(faces) - 1: # If last
            kramers.append(getKramer(face, 'r')) # Get right kramer

        else:
            kramers.append(getKramer(face, 'c')) # Get centre kramer

    return jsonify(kramers=kramers)

# Webhook to add face to server log
@app.route('/_clockIn', methods=['GET', 'POST'])
def addFace():
    print('got webhook!')
    faces.append(['smiling', face]) # get from webhook, get face, add to faces with id
    return redirect('/') # Remove this

# Catch all
@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    serve(app)