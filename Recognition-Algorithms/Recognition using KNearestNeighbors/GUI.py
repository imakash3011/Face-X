import cv2
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from tkinter import Tk, Label, Frame


data = np.load("face_data.npy")
# Name = input("Whom you want to search: \n")

# print(data.shape, data.dtype)

X = data[:, 1:].astype(int)
y = data[:, 0]
model = KNeighborsClassifier()
model.fit(X, y)
cap = cv2.VideoCapture(0)
detector = cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")
while True:

    ret, frame = cap.read()

    if ret:
        faces = detector.detectMultiScale(frame, 1.1, 4)

        for face in faces:
            x, y, w, h = face

            cut = frame[y:y + h, x:x + w]

            fix = cv2.resize(cut, (100, 100))
            gray = cv2.cvtColor(fix, cv2.COLOR_BGR2GRAY)

            out = model.predict([gray.flatten()])

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(
                frame,
                str(f"User Identified:{out[0]}"),
                (x,
                 y - 10),
                cv2.FONT_HERSHEY_COMPLEX,
                2,
                (255,
                 0,
                 0),
                2)

            cv2.imshow("My Face", gray)

        cv2.imshow("My Screen", frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()

root = Tk()

root.geometry("400x200")
root.maxsize(400, 200)
root.minsize(350, 180)
root.configure(background='Azure')
root.title("Recogniser")
my = Label(text="Image Recogniser Result", bg="Azure",
           fg='Black', font=('comicsansms', 19, 'bold'))
my.pack()
my3 = Label(
    text=f'User Identified: {out}',
    bg="Beige",
    fg='Black',
    font=(
        'comicsansms',
        15),
    relief="sunken")
my3.pack(pady=50)
root.mainloop()
