import streamlit as st
import mediapipe as mp
import math as mt
import tempfile
import cv2
from utils import finger_counter, draw_hand, draw_blured_face, detect_face, detect_hand

# Interface Streamlit
st.title("Application Floutage et Comptage")

def main():
    uploaded_file = st.file_uploader("Chargez une vidéo", type=["mp4", "avi", "mov"])

    if uploaded_file is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())
        
        video = cv2.VideoCapture(tfile.name)

        # Instructions pour l'utilisateur
        st.write("**⚠️ VOIR LA NOUVELLE FENÊTRE VIDEO **")
        st.write("**Appuyez sur 's' pour arrêter prématurément la vidéo**")

        # Lire la vidéo frame par frame
        ret = True
        while ret:
            ret, frame = video.read()
            if ret:
                # Traitement de la vidéo
                cap = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results_hand = detect_hand(cap)
                results_face = detect_face(cap)
                
                # Vérification si des mains ou visages sont détectés
                if results_hand.multi_hand_landmarks:
                    stretched_finger_count = finger_counter(results_hand)
                    cv2.putText(frame, f'We see: {stretched_finger_count} finger(s)', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
                    draw_hand(results_hand)
                
                if results_face.detections:
                    draw_blured_face(results_face,frame)

                # Affichage de la vidéo dans Streamlit
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Re-conversion à chaque frame

                # Afficher la frame dans Streamlit
                st.image(frame_rgb, channels="RGB", use_column_width=True)

        video.release()

# Appel de main() lorsque ce fichier est exécuté
if __name__ == "__main__":
    main()
