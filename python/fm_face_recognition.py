import cv2
import base64
import os
import face_recognition
import numpy as np
from flask import Flask, request, jsonify
import random
import string
import shutil

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


@app.route("/")
def hello():
    return "ok"


@app.route('/basedir')
def basedir():
    return jsonify(BASE_DIR)


@app.route('/compare', methods=['POST'])
def compare():
    body = request.get_json()

    name = randomString(9)

    master_str = body['master']
    face_str = body['face']

    face_data = base64.b64decode(face_str)
    master_data = base64.b64decode(master_str)

    master_np = np.fromstring(master_data, np.uint8)
    face_np = np.fromstring(face_data, np.uint8)
    face_image = cv2.imdecode(face_np, cv2.IMREAD_COLOR)
    master_image = cv2.imdecode(master_np, cv2.IMREAD_COLOR)

    if face_image is None:
        return jsonify(status=0, message="fail parse face")

    master_rgb_frame = master_image[:, :, ::-1]

    # Find all the faces in the image using the default HOG-based model.
    # This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
    # See also: find_faces_in_picture_cnn.py
    master_face_locations = face_recognition.face_locations(master_rgb_frame)

    print("I found {} face(s) in this photograph.".format(len(master_face_locations)))

    for face_location in master_face_locations:
        # Print the location of each face in this image
        top, right, bottom, left = face_location
        print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom,
                                                                                                    right))
        padding = 50
        top = top - padding
        left = left - padding
        right = right + padding
        bottom = bottom + padding
        # You can access the actual face itself like this:
        master_data = master_image[top:bottom, left:right]

    if len(master_face_locations) == 0:
        return jsonify(status=0, message='No face detected in master')

    master_save_dir = BASE_DIR + "/" + name
    if not os.path.exists(master_save_dir):
        os.mkdir(master_save_dir)

    img_name = name + ".jpg"

    master_path = master_save_dir + "/" + img_name
    cv2.imwrite(master_path, master_data)

    # Load some sample pictures and learn how to recognize them.
    image_recog = face_recognition.load_image_file(master_path)

    known_faces_master = []
    try:
        image_face_encoding = face_recognition.face_encodings(image_recog)[0]
        known_faces_master.append(image_face_encoding)
    except:
        return jsonify(status=0, message="Error face encoding")

    face_rgb_frame = face_image[:, :, ::-1]

    face_locations = face_recognition.face_locations(face_rgb_frame)

    face_encodings = face_recognition.face_encodings(face_rgb_frame, face_locations)

    if len(face_encodings) == 0:
        return jsonify(status=0, message="No face in request")

    for face_encoding in face_encodings:
        distance = face_recognition.face_distance(known_faces_master, face_encoding)
        shutil.rmtree(master_save_dir, ignore_errors=True)

        if distance[0] <= 0.6:
            acc = 100 - (distance[0] / 0.6 * 100) + 13
            return jsonify(status=1, is_match=1, similarity=acc)
        else:
            return jsonify(status=1, is_match=0, similarity=0)


# if __name__ == "__main__":
#     app.run(host='0.0.0.0')

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0',port=5000)
