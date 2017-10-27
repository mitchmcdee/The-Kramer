import cognitive_face as CF
from PIL import Image
import requests

KEY = '923e32c414a04b14a2ecaec74190760a'
CF.Key.set(KEY)

BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/'
CF.BaseUrl.set(BASE_URL)

url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
# url = 'https://ae01.alicdn.com/kf/HTB1InjoJFXXXXaeXpXXq6xXFXXX9/P0434-seinfeld-kramer-TV-Wallpaper-Poster-Wall-Art-for-Home-Decor-Canvas-Printings-24x36inch.jpg'
result = CF.face.detect(url)
x1, y1, x2, y2 = tuple(result[0]['faceRectangle'].values())
im = Image.open(requests.get(url, stream=True).raw)
face = im.crop((y1,x1,y1+y2,x1+x2))
face.thumbnail((210, 210), Image.ANTIALIAS)

maskedKramer = Image.open('maskedKramer.png')
croppedKramer = Image.open('croppedKramer.png')
background = Image.new("RGBA", maskedKramer.size)
background.paste(face, (180,310))
final = Image.new("RGBA", maskedKramer.size)
final = Image.alpha_composite(final, croppedKramer)
final = Image.alpha_composite(final, background)
final = Image.alpha_composite(final, maskedKramer)

final.show()