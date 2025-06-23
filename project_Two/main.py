import cv2

# Replace with your IP Webcam URL
url = "http://192.168.100.50:8080/video"  # replace with your IP
cap = cv2.VideoCapture(url)

# Define VideoWriter
# Define codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame.")
        break
    print("The video is recording... Success !!!")
    frame = cv2.resize(frame, (640, 480))  # optional resize
    out.write(frame)
    # cv2.imshow('frame', frame) #Commented because Kubernetes + Docker don't have GUI Features

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Below is Commented because Kubernetes + Docker don't have GUI Features
# cap.release()
# out.release()
# cv2.destroyAllWindows()