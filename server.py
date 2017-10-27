from flask import Flask, render_template
from waitress import serve
from PIL import Image
import requests
import time

KEY = '923e32c414a04b14a2ecaec74190760a'
BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'
HEADER = {'Content-Type': 'application/octet-stream', 'Ocp-Apim-Subscription-Key': KEY}

THE_KRAMER = 'static/images/theKramer.png'
LEFT_CROPPED_KRAMER = 'static/images/leftCroppedKramer.png'
RIGHT_MASKED_KRAMER = Image.open('static/images/rightMaskedKramer.png')
RIGHT_CROPPED_KRAMER = Image.open('static/images/rightCroppedKramer.png')
CENTRE_MASKED_KRAMER = Image.open('static/images/centreMaskedKramer.png')
CENTRE_CROPPED_KRAMER = Image.open('static/images/centreCroppedKramer.png')

app = Flask(__name__)
faces = []
images = {}

testImage = open('static/images/smiling.png', 'rb')
r = requests.post(BASE_URL, headers=HEADER, data=testImage)
x1, y1, x2, y2 = tuple(r.json()[0]['faceRectangle'].values())
im = Image.open(testImage)
face = im.crop((y1,x1,y1+y2,x1+x2))
face.thumbnail((210, 210), Image.ANTIALIAS)
faces.append(['smiling', face])
faces.append(['smiling', face])
faces.append(['smiling', face])
faces.append(['smiling', face])

################################################################################

# Get kramer image
def getKramer(faceInfo, position):
    name, face = faceInfo
    faceHash = tuple([name, position])
    if faceHash in images:
        return images[faceHash]

    masked = RIGHT_MASKED_KRAMER if position == 'r' else CENTRE_MASKED_KRAMER
    cropped = RIGHT_CROPPED_KRAMER if position == 'r' else CENTRE_CROPPED_KRAMER

    background = Image.new("RGBA", masked.size)
    background.paste(face, (180,310))
    final = Image.new("RGBA", masked.size)
    final = Image.alpha_composite(final, cropped)
    final = Image.alpha_composite(final, background)
    final = Image.alpha_composite(final, masked)

    filename = 'static/images/' + str(time.time()) + '.png'
    final.save(filename)
    images[faceHash] = filename
    return images[faceHash]

# Webhook to add face to server log
@app.route('/_addFace')
def addFace():
    pass

# Catch all
@app.route("/")
def index():
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

    return render_template('index.html', kramers=kramers)

if __name__ == "__main__":
    serve(app)