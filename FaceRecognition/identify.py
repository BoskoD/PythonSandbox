import face_recognition
from PIL import Image, ImageDraw

KNOWN_FACES_DIR = './img/known/'
TEST_IMAGE_DIR = './img/groups/'
KNOWN_FACE_NAMES = ["Bill Gates", "Steve Jobs"]

def load_known_faces():
    known_face_encodings = []
    for name in KNOWN_FACE_NAMES:
        image_path = KNOWN_FACES_DIR + name + '.jpg'
        image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(face_encoding)
    return known_face_encodings

def recognize_faces(known_face_encodings, test_image_path):
    test_image = face_recognition.load_image_file(test_image_path)
    face_locations = face_recognition.face_locations(test_image)
    face_encodings = face_recognition.face_encodings(test_image, face_locations)
    pil_image = Image.fromarray(test_image)
    draw = ImageDraw.Draw(pil_image)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown Person"
        
        if True in matches:
            first_match_index = matches.index(True)
            name = KNOWN_FACE_NAMES[first_match_index]
        
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 0, 0))
        text_width, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 0), outline=(0, 0, 0))
        draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))
    
    del draw
    pil_image.show()

def main():
    known_face_encodings = load_known_faces()
    test_image_path = TEST_IMAGE_DIR + 'bill-steve.jpg'
    recognize_faces(known_face_encodings, test_image_path)

if __name__ == "__main__":
    main()