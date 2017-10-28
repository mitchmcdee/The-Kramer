import cognitive_face as CF
from PIL import Image
import requests

KEY      = '923e32c414a04b14a2ecaec74190760a' # This is test account so meh if its stolen lel
BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/'
CF.Key.set(KEY)
CF.BaseUrl.set(BASE_URL)

url = 'https://s3.amazonaws.com/PayAus/logins/photos/050/337/809/original/login_1234_636448033080000000.png?1509170561'
result = CF.face.detect(url)
x1, y1, x2, y2 = tuple(result[0]['faceRectangle'].values())
person = Image.open(requests.get(url, stream=True).raw)
face = person.crop((y1,x1,y1+y2,x1+x2))
face = face.resize((210,210), Image.ANTIALIAS)

maskedKramer = Image.open('static/images/centreMaskedKramer.png')
croppedKramer = Image.open('static/images/centreCroppedKramer.png')
background = Image.new("RGBA", maskedKramer.size)
background.paste(face, (180,310))
final = Image.new("RGBA", maskedKramer.size)
final = Image.alpha_composite(final, croppedKramer)
final = Image.alpha_composite(final, background)
final = Image.alpha_composite(final, maskedKramer)

final.show()