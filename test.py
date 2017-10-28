import cognitive_face as CF
from PIL import Image
import requests

KEY = '923e32c414a04b14a2ecaec74190760a'
header = {'Content-Type': 'application/octet-stream', 'Ocp-Apim-Subscription-Key': KEY}
api_url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect"

testImage = open('static/images/theKramer.png', 'rb')
r = requests.post(api_url, headers=header, data=testImage)

x1, y1, x2, y2 = tuple(r.json()[0]['faceRectangle'].values())
im = Image.open(testImage)
face = im.crop((y1,x1,y1+y2,x1+x2))
face.thumbnail((210, 210), Image.ANTIALIAS)

maskedKramer = Image.open('static/images/centreMaskedKramer.png')
croppedKramer = Image.open('static/images/centreCroppedKramer.png')
background = Image.new("RGBA", maskedKramer.size)
background.paste(face, (180,310))
final = Image.new("RGBA", maskedKramer.size)
final = Image.alpha_composite(final, croppedKramer)
final = Image.alpha_composite(final, background)
final = Image.alpha_composite(final, maskedKramer)

final.show()