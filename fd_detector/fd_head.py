import cv2
import dlib
from imutils import face_utils
import numpy as np

face_landmark_path = "./model/shape_predictor_68_face_landmarks.dat"

object_pts = np.float32(
    [
        [6.825897, 6.760612, 4.402142],  # 33左眉左上角
        [1.330353, 7.122144, 6.903745],  # 29左眉右角
        [-1.330353, 7.122144, 6.903745],  # 34右眉左角
        [-6.825897, 6.760612, 4.402142],  # 38右眉右上角
        [5.311432, 5.485328, 3.987654],  # 13左眼左上角
        [1.789930, 5.393625, 4.413414],  # 17左眼右上角
        [-1.789930, 5.393625, 4.413414],  # 25右眼左上角
        [-5.311432, 5.485328, 3.987654],  # 21右眼右上角
        [2.005628, 1.409845, 6.165652],  # 55鼻子左上角
        [-2.005628, 1.409845, 6.165652],  # 49鼻子右上角
        [2.774015, -2.080775, 5.048531],  # 43嘴左上角
        [-2.774015, -2.080775, 5.048531],  # 39嘴右上角
        [0.000000, -3.116408, 6.097667],  # 45嘴中央下角
        [0.000000, -7.415691, 4.070434],
    ]
)

K = [
    6.5308391993466671e002,
    0.0,
    3.1950000000000000e002,
    0.0,
    6.5308391993466671e002,
    2.3950000000000000e002,
    0.0,
    0.0,
    1.0,
]

D = [7.0834633684407095e-002, 6.9140193737175351e-002, 0.0, 0.0, -1.3073460323689292e000]


cam_matrix = np.array(K).reshape(3, 3).astype(np.float32)
dist_coeffs = np.array(D).reshape(5, 1).astype(np.float32)


reprojectsrc = np.float32(
    [
        [10.0, 10.0, 10.0],
        [10.0, 10.0, -10.0],
        [10.0, -10.0, -10.0],
        [10.0, -10.0, 10.0],
        [-10.0, 10.0, 10.0],
        [-10.0, 10.0, -10.0],
        [-10.0, -10.0, -10.0],
        [-10.0, -10.0, 10.0],
    ]
)
line_pairs = [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]]


def get_head_pose(shape):
    image_pts = np.float32(
        [
            shape[17],
            shape[21],
            shape[22],
            shape[26],
            shape[36],
            shape[39],
            shape[42],
            shape[45],
            shape[31],
            shape[35],
            shape[48],
            shape[54],
            shape[57],
            shape[8],
        ]
    )

    _, rotation_vec, translation_vec = cv2.solvePnP(object_pts, image_pts, cam_matrix, dist_coeffs)
    reprojectdst, _ = cv2.projectPoints(reprojectsrc, rotation_vec, translation_vec, cam_matrix, dist_coeffs)

    reprojectdst = tuple(map(tuple, reprojectdst.reshape(8, 2)))  # 以8行2列显示

    rotation_mat, _ = cv2.Rodrigues(rotation_vec)  # 罗德里格斯公式（将旋转矩阵转换为旋转向量）
    pose_mat = cv2.hconcat((rotation_mat, translation_vec))  # 水平拼接，vconcat垂直拼接

    _, _, _, _, _, _, euler_angle = cv2.decomposeProjectionMatrix(pose_mat)  # 将投影矩阵分解为旋转矩阵和相机矩阵

    return reprojectdst, euler_angle


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Unable to connect to camera.")
        return
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(face_landmark_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            face_rects = detector(frame, 0)

            if len(face_rects) > 0:
                shape = predictor(frame, face_rects[0])
                shape = face_utils.shape_to_np(shape)
                reprojectdst, euler_angle = get_head_pose(shape)
                pitch = format(euler_angle[0, 0])
                yaw = format(euler_angle[1, 0])
                roll = format(euler_angle[2, 0])
                print(f"pitch:{pitch}, yaw:{yaw}, roll:{roll}")

                for (x, y) in shape:
                    cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

                for start, end in line_pairs:
                    cv2.line(frame, reprojectdst[start], reprojectdst[end], (0, 0, 255))

                cv2.putText(
                    frame,
                    "X: " + "{:7.2f}".format(euler_angle[0, 0]),
                    (20, 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    (0, 0, 255),
                    thickness=2,
                )
                cv2.putText(
                    frame,
                    "Y: " + "{:7.2f}".format(euler_angle[1, 0]),
                    (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    (0, 0, 255),
                    thickness=2,
                )
                cv2.putText(
                    frame,
                    "Z: " + "{:7.2f}".format(euler_angle[2, 0]),
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    (0, 0, 255),
                    thickness=2,
                )

            cv2.putText(frame, "Press 'q': Quit", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (84, 255, 159), 2)

            cv2.imshow("Head_Posture", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
