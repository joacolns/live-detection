import pathlib
import cv2
import tkinter as tk
from tkinter import filedialog

# Función para iniciar la detección de caras
def start_face_detection(source):
    camera = cv2.VideoCapture(source)
    print("face-detection >>> Press 'Q' to quit")
    while True:
        _, frame = camera.read()
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

        cv2.imshow("face-detection", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

# Función para elegir usar la cámara
def use_camera():
    root.destroy()
    start_face_detection(0)

# Función para elegir cargar un video
def load_video():
    video_path = filedialog.askopenfilename()
    if video_path:
        root.destroy()
        start_face_detection(video_path)

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
