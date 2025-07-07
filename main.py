import pathlib
import cv2
import mediapipe as mp
import tkinter as tk
from tkinter import filedialog

# Inicialización de MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=2,
                       min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)

# Inicialización de MediaPipe Drawing
mp_drawing = mp.solutions.drawing_utils

# Función para iniciar la detección de caras y manos
def start_face_and_hand_detection(source):
    camera = cv2.VideoCapture(source)
    print("Detection >>> Press 'Q' to quit")
    while True:
        _, frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame.flags.writeable = False
        results = hands.process(frame)
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Detección de manos
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                    mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                 )

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = clf.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=7,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        coords_text = "No Faces"
        for (x, y, width, height) in faces:
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
            coords_text = f"Coords: X={x}, Y={y}, W={width}, H={height}"

        # Mostrar las coordenadas en el frame
        cv2.putText(frame, coords_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow("Detection", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()
    hands.close()

# Función para elegir usar la cámara
def use_camera():
    root.destroy()
    start_face_and_hand_detection(0)

# Función para elegir cargar un video
def load_video():
    video_path = filedialog.askopenfilename()
    if video_path:
        root.destroy()
        start_face_and_hand_detection(video_path)

# Cargar el clasificador de Haar
cascade_path = pathlib.Path(cv2.__file__).parent.absolute() / "data/haarcascade_frontalface_default.xml"
clf = cv2.CascadeClassifier(str(cascade_path))

# Crear la ventana principal
root = tk.Tk()
root.title("face-detection")
root.geometry('520x300')
root.resizable(0,0)

# Botón para usar la cámara
button_camera = tk.Button(root, text="Live Camera", command=use_camera, height=2, width=15)
button_camera.pack(pady=20)

# Botón para cargar un video
button_video = tk.Button(root, text="Load Video", command=load_video, height=2, width=15)
button_video.pack(pady=20)

# Ejecutar el bucle principal de Tkinter
root.mainloop()
