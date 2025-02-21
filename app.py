import streamlit as st
import mediapipe as mp
import math as mt
import tempfile
import cv2

# Interface Streamlit
st.title("Application Floutage et Comptage ")

uploaded_file = st.file_uploader("Chargez une vidéo", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    
    video = cv2.VideoCapture(tfile.name)

    # Les modèles mediapipe, solutions pour la détection des mains

    mp_hands= mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    hands = mp_hands.Hands(
        max_num_hands = 2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    )

    drawing_styles = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=3)

    landmark_styles = mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=5)

    # Les modèles mediapipe, solutions pour la détection des mains

    mp_face_detection = mp.solutions.face_detection
    mp_drawing = mp.solutions.drawing_utils


    face_detection = mp_face_detection.FaceDetection(
        min_detection_confidence=0.7
        )
    
    # fonction pour compter les doigts tendus. 
    # Par simplification, Un doigt tendu est repéré en comparant les hauteurs des landmarks. Si le doigt est tendu 

    def finger_counter(results):
        stretched_finger_count=0
        liste_handmarks = fill_list(results)
        for mark_index in range(1,21,4):
            if liste_handmarks[mark_index].y > liste_handmarks[mark_index+1].y > liste_handmarks[mark_index+2].y > liste_handmarks[mark_index+3].y :
                stretched_finger_count+=1
            if (mark_index == 1) & (distance(liste_handmarks[4],liste_handmarks[13])< 42.0) :
                stretched_finger_count-=1
        return stretched_finger_count
    
    # fonction distance
    def distance(landmark1, landmark2):
        h, w, c = frame.shape
        return mt.sqrt(
            ((landmark2.x - landmark1.x)*w) ** 2 +
            ((landmark2.y - landmark1.y)*h) ** 2 +
            ((landmark2.z - landmark1.z)*c) ** 2
        )
    
    # fonction pour obtenir un format indexé des landmarks
    #en vue d'utiliser finger_counter
    def fill_list(results):
        liste_handmarks = []
        for id, landmark in enumerate (results_hand.multi_hand_landmarks[0].landmark):
            liste_handmarks.append(landmark)
        return liste_handmarks
    
    # Déssiner les lignes et points des mains. Utilisation standards de mediapipe
    def draw_hand(results_hand):
        if results_hand.multi_hand_landmarks:
            for hand_landmarks in results_hand.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(frame, hand_landmarks,mp_hands.HAND_CONNECTIONS, landmark_styles,drawing_styles)
    
    # fonction floutage
    # Utiliser mediapipe pour obtenir les limites du visage puis opencv pour flouter

    def draw_blured_face(results_face) :
            global frame
            well = False
            if results_face.detections:
                for detection in results_face.detections:
                    
                    bboxC = detection.location_data.relative_bounding_box
                    ih, iw, _ = frame.shape  
                    x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
        
                    
                    face_region = frame[y:y+h, x:x+w]
        
                    
                    blurred_face= cv2.blur(face_region, (30, 30))
        
                    
                    frame[y:y+h, x:x+w] = blurred_face    
                    well = True
            return well
    
    st.write("**⚠️VOIR LA NOUVELLE FENETRE VIDEO **")
    st.write("**Appuyer sur la touche 's' pour arrêter prématurément la video **")


    ret = True
    while ret:
        ret, frame = video.read()
        if ret:
            # Traitement de la vidéo
            cap = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results_hand = hands.process(cap)
            results_face = face_detection.process(cap)
            
            # Vérification si des mains ou visages sont détectés
            if results_hand.multi_hand_landmarks:
                stretched_finger_count = finger_counter(results_hand)
                cv2.putText(frame, f'We see : {stretched_finger_count} finger(s)', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
                draw_hand(results_hand)
            
            if results_face.detections:
                draw_blured_face(results_face)

            cv2.imshow('Visuel',frame)

            # Ajout d'une vérification pour s'assurer que la vidéo est bien écrite

            if cv2.waitKey(1) & 0xFF == ord('s'): 
              ret =False
              break
    
    video.release()
    
    cv2.destroyAllWindows()
   
    # Ajoutez cette ligne pour vérifier si la vidéo temporaire est bien accessible
    

    
    
