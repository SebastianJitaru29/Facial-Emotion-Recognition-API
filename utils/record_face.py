import cv2

def record_video(filename='output.mp4', duration=10):
    # Open the default camera
    cap = cv2.VideoCapture(0)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

    start_time = cv2.getTickCount()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Write the frame into the file
        out.write(frame)

        # Display the resulting frame
        cv2.imshow('frame', frame)

        # Break the loop if the duration exceeds
        if (cv2.getTickCount() - start_time) / cv2.getTickFrequency() > duration-2.25:
            break

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release everything when done
    cap.release()
    out.release()
    cv2.destroyAllWindows()

# Usage
record_video('my_face_video1.mp4', 10)
