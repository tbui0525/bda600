import cv2
def picture(n):
    cap = cv2.VideoCapture(0) # CONNECT TO WEBCAM
    _, frame = cap.read() # TAKE PICTURE
    cv2.imwrite(f"photos/img_{n}.png", frame) # SAVE PICTURE
    cv2.destroyAllWindows() # DESTROY WINDOWS
    return