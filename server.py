from flask import Flask, render_template, redirect, jsonify, request
from waitress import serve
import cognitive_face as CF
from PIL import Image
from collections import OrderedDict
import requests
import time
import os
import glob

KEY      = '923e32c414a04b14a2ecaec74190760a' # This is test account so meh if its stolen lel
BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/'
CF.Key.set(KEY)
CF.BaseUrl.set(BASE_URL)

THE_KRAMER            = 'static/images/theKramer.png'
LEFT_CROPPED_KRAMER   = 'static/images/leftCroppedKramer.png'
RIGHT_MASKED_KRAMER   = 'static/images/rightMaskedKramer.png'
RIGHT_CROPPED_KRAMER  = 'static/images/rightCroppedKramer.png'
CENTRE_MASKED_KRAMER  = 'static/images/centreMaskedKramer.png'
CENTRE_CROPPED_KRAMER = 'static/images/centreCroppedKramer.png'

app = Flask(__name__)
faces = OrderedDict()
users = {}

# Remove all old files
for f in glob.glob(os.path.join('static/images', "user_*")):
    os.remove(f)

################################################################################

# Get kramer image
def getKramer(faceInfo, position):
    user, face = faceInfo
    faceHash = tuple([user, position])
    if faceHash in users:
        return users[faceHash]

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
            pass
        else:
            break

    filename = 'static/images/user_' + str(time.time()) + '.png'
    final.save(filename)
    users[faceHash] = filename
    return filename

# Webhook to add face to server log
@app.route('/_stream')
def streamKramer():
    return render_template('stream.html')

# Webhook to add face to server log
@app.route('/_getKramers', methods=['POST'])
def getKramers():
    kramers = []

    if len(faces) == 0:
        kramers.append(THE_KRAMER)
    else:
        kramers.append(LEFT_CROPPED_KRAMER)

    for i, faceInfo in enumerate(list(faces.items())):
        if i == len(faces) - 1: # If last
            kramers.append(getKramer(faceInfo, 'r')) # Get right kramer
        else:
            kramers.append(getKramer(faceInfo, 'c')) # Get centre kramer

    return jsonify(kramers=kramers)

# Webhook to add face to server log
@app.route('/_clockIn', methods=['POST'])
def addFace():
    r = request.get_json()['payload']['body']
    user = str(r['user_id'])
    print(r)

    # Add/Remove user
    if r['type'] == 'clockin':
        url = r['photo']
        result = CF.face.detect(url)
        if len(result) == 0:
            print('bad photo, try again')
            return 'NOT OK'

        print(result)
        x1, y1, x2, y2 = tuple(result[0]['faceRectangle'].values())
        person = Image.open(requests.get(url, stream=True).raw)
        face = person.crop((y1,x1,y1+y2,x1+x2))
        faces[user] = face.resize((160,210), Image.ANTIALIAS)
    elif user in faces:
        del faces[user]

    return 'OK'

# Catch all
@app.route("/")
def index():
    return render_template('index.html')

# Start server
if __name__ == "__main__":
    serve(app, port=80)