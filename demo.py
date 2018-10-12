import requests
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import patches
from io import BytesIO

subscription_key = 'a53090b5bb3748679637a70b3a0cb6f9'  # Replace with a valid Subscription Key here.
assert subscription_key

BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'  # Replace with your regional Base URL
# image_url = 'https://snn.bz/wp-content/uploads/2016/03/MelaniaKnauss09-1.jpg'
headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
# Default content-type is json if not specified, octet stream for local file

params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,' +
    'emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
}
# Image from local file
image_path = "images/Vancouver.jpg"  # Replace with local file
image_data = open(image_path, 'rb').read()
image = Image.open(BytesIO(image_data))

# Image from image_url
# image_data = {'url': image_url}
# image = Image.open(BytesIO(requests.get(image_url).content))

response = requests.post(BASE_URL, params=params, headers=headers, data=image_data)  # Use json=image_data for URL image
faces = response.json()

# Display the original image and overlay it with the face information.
plt.figure(figsize=(8, 8))
ax = plt.imshow(image, alpha=0.6)
for face in faces:
    fr = face["faceRectangle"]
    fa = face["faceAttributes"]
    origin = (fr["left"], fr["top"])
    origin2 = (fr["left"], fr["top"]+fr["height"])
    p = patches.Rectangle(
        origin, fr["width"], fr["height"], fill=False, linewidth=2, color='b')
    ax.axes.add_patch(p)
    plt.text(origin[0], origin[1], "%s, %d" % (fa["gender"].capitalize(), fa["age"]),
             fontsize=20, weight="bold", va="bottom")
    plt.text(origin2[0], origin2[1], "%s, Smile:%d" % (fa["glasses"].capitalize(), fa["smile"]),
             fontsize=8, weight="bold", va="top")
_ = plt.axis('off')

plt.show()

