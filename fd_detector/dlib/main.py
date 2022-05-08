import cv2
import dlib
import numpy as np

# import time


def landmarks_to_np(landmarks, dtype="int"):
    # Get the number of landmarks
    num = landmarks.num_parts

    # initialize the list of (x, y)-coordinates
    coords = np.zeros((num, 2), dtype=dtype)

    # loop over the 68 facial landmarks and convert them
    # to a 2-tuple of (x, y)-coordinates
    for i in range(num):
        coords[i] = (landmarks.part(i).x, landmarks.part(i).y)
    # return the list of (x, y)-coordinates
    return coords


if __name__ == "__main__":
    predictor_path = "fd_detector/dlib/data/shape_predictor_68_face_landmarks.dat"
    detector = dlib.get_frontal_face_detector()  # Face detector
    predictor = dlib.shape_predictor(predictor_path)  # Face landmark predictor

    cap = cv2.VideoCapture(0)

    fps = cap.get(cv2.CAP_PROP_FPS)
    print("Frames per second using cv2.CAP_PROP_FPS: {0}".format(fps))

    cap.set(3, 480)  # set Width
    cap.set(4, 270)  # set Height
    cap.set(5, 50)  # set frame rate

    queue = np.zeros(30, dtype=int)  # 初始化时间序列 queue
    queue = queue.tolist()

    while cap.isOpened():
        # Read video frames
        _, img = cap.read()

        # Convert to greyscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Face detection
        rects = detector(gray, 1)

        # Operate on each detected face
        for i, rect in enumerate(rects):
            # Get the coordinates
            x = rect.left()
            y = rect.top()
            w = rect.right() - x
            h = rect.bottom() - y

            # Draw borders, add text labels
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(
                img, f"Face #{i + 1}", (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA
            )

            # Detect landmarks
            landmarks = predictor(gray, rect)
            landmarks = landmarks_to_np(landmarks)

            # Marked landmarks
            for (x, y) in landmarks:
                cv2.circle(img, (x, y), 2, (0, 255, 0), -1)

            # Calculate Euclidean distance
            d1 = np.linalg.norm(landmarks[37] - landmarks[41])
            d2 = np.linalg.norm(landmarks[38] - landmarks[40])
            d3 = np.linalg.norm(landmarks[43] - landmarks[47])
            d4 = np.linalg.norm(landmarks[44] - landmarks[46])
            d_mean = (d1 + d2 + d3 + d4) / 4
            d5 = np.linalg.norm(landmarks[36] - landmarks[39])
            d6 = np.linalg.norm(landmarks[42] - landmarks[45])
            d_reference = (d5 + d6) / 2
            d_judge = d_mean / d_reference
            print(d_judge)

            # Open/closed eyes flag: based on the threshold to determine whether the eyes are closed,
            # closed eyes flag=1, open eyes flag=0 (the threshold is adjustable)
            flag = int(d_judge < 0.27)

            # flag 入队
            queue = queue[1:] + [flag]

            # Determination of fatigue: based on whether more than half the number of elements in the time series are below the threshold
            if sum(queue) > len(queue) / 2:
                cv2.putText(
                    img,
                    "WARNING !",
                    (100, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA,
                )
            else:
                cv2.putText(
                    img,
                    "SAFE",
                    (100, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2,
                    cv2.LINE_AA,
                )

        # Show Result
        cv2.imshow("Result", img)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:  # press 'ESC' to quit
            break

    cap.release()
    cv2.destroyAllWindows()
