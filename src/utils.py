import math as mt
import mediapipe as mp
import cv2

# Les modèles mediapipe, solutions pour la détection des mains
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def detect_hand(cap):
    hands = mp_hands.Hands(
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    )
    return hands.process(cap)

# Les modèles mediapipe, solutions pour la détection des mains
def detect_face(cap):
    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(
        min_detection_confidence=0.7
    )
    return face_detection.process(cap)
    

def finger_counter(results):
    stretched_finger_count = 0
    liste_handmarks = fill_list(results)
    for mark_index in range(1, 21, 4):
        if liste_handmarks[mark_index].y > liste_handmarks[mark_index+1].y > liste_handmarks[mark_index+2].y > liste_handmarks[mark_index+3].y:
            stretched_finger_count += 1
        if (mark_index == 1) & (distance(liste_handmarks[4], liste_handmarks[13]) < 42.0):
            stretched_finger_count -= 1
    return stretched_finger_count

def distance(landmark1, landmark2,frame):
    h, w, c = frame.shape
    return mt.sqrt(
        ((landmark2.x - landmark1.x) * w) ** 2 +
        ((landmark2.y - landmark1.y) * h) ** 2 +
        ((landmark2.z - landmark1.z) * c) ** 2
    )

def fill_list(results):
    liste_handmarks = []
    for id, landmark in enumerate(results.multi_hand_landmarks[0].landmark):
        liste_handmarks.append(landmark)
    return liste_handmarks

def draw_hand(results_hand,frame):
    drawing_styles = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=3)
    landmark_styles = mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=5)
    if results_hand.multi_hand_landmarks:
            for hand_landmarks in results_hand.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS, landmark_styles, drawing_styles)

def draw_blured_face(results_face, frame):
    well = False
    if results_face.detections:
        for detection in results_face.detections:
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = frame.shape  
            x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
            face_region = frame[y:y+h, x:x+w]
            blurred_face = cv2.blur(face_region, (30, 30))
            frame[y:y+h, x:x+w] = blurred_face    
            well = True
    return well
