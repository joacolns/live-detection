import pathlib
import cv2

cascade_path=pathlib.Path(cv2.__file__).parent.absolute() / "data/haarcascade_frontalface_default.xml"
#print(cascade_path)

clf = cv2.CascadeClassifier(str(cascade_path))
camera = cv2.VideoCapture(0) #Linea para camara // Numeros de camaras // 0 - Camara default
camera = cv2.VideoCapture("VideoTest.mp4") #Linea para videos // Numeros de camaras // 0 - Camara default
print("face-detection >>> Press 'Q' to quit")

while True:
    _, frame=camera.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces=clf.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE  
    )
    for (x, y, width, height) in faces:
        cv2.rectangle(frame, (x, y), (x+width, y+width), (0, 255, 0), 2)

    cv2.imshow("face-detection", frame)
    if cv2.waitKey(1) == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()