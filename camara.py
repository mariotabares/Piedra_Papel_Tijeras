# *********************************************************************************************************************
# Libreías necesarias
import cv2
import random
import mediapipe as mp
import math


# *********************************************************************************************************************
# Inicializa el módulo de detección de manos de MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=True, max_num_hands=1
)  # Establece static_image_mode en True y max_num_hands=1

# Inicializa la cámara
cap = cv2.VideoCapture(0)
# *********************************************************************************************************************
# Variables de Juego 
contadorMayor = 25
contadorReinicio=20
bandera=0
ganador=0
# Configurar el contador
contador = 3  # El tiempo en segundos que deseas contar
font = cv2.FONT_HERSHEY_SIMPLEX
color_contador = (0, 255, 0)  # Color del contador (verde)
posicion_contador = (290, 300)  # Posición del contador en la pantalla
tamaño_fuente = 4
espaciado_fuente = 3

# *********************************************************************************************************************
while cap.isOpened():
    # *********************************************************************************************************************
    # Captura el frame de la cámara
    ret, frame = cap.read()
    if not ret:
        continue

    # Convierte la imagen a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Convierte la imagen en escala de grises a una imagen en color (blanco y negro)
    gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    # Detecta las manos en la imagen en color
    results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    # *********************************************************************************************************************
    # muestra el conteo en Pantalla

    contadorMayor = contadorMayor - 1
    if contadorMayor == 0:
        contador = contador - 1
        contadorMayor = 25
        if contador == 0:
            numero_aleatorio = random.randint(1, 3)
            if(numero_aleatorio==1):
                bandera = 1
                cv2.putText(
                    frame,
                    "Maquina saco:",
                    (100, 200),
                    font,
                    tamaño_fuente,
                    color_contador,
                    espaciado_fuente,
                    cv2.LINE_AA,                  
                )
                cv2.putText(
                    frame,
                    "Piedra",
                    (150, 300),
                    font,
                    tamaño_fuente,
                    color_contador,
                    espaciado_fuente,
                    cv2.LINE_AA,                  
                )
            elif(numero_aleatorio==2):
                bandera=1
                cv2.putText(
                    frame,
                    "Maquina saco:",
                    (100, 200),
                    font,
                    tamaño_fuente,
                    color_contador,
                    espaciado_fuente,
                    cv2.LINE_AA,                  
                )
                cv2.putText(
                    frame,
                    "Papel",
                    (150, 300),
                    font,
                    tamaño_fuente,
                    color_contador,
                    espaciado_fuente,
                    cv2.LINE_AA,                  
                )
            elif(numero_aleatorio==3):
                bandera==1
                cv2.putText(
                    frame,
                    "Maquina saco:",
                    (100, 200),
                    font,
                    tamaño_fuente,
                    color_contador,
                    espaciado_fuente,
                    cv2.LINE_AA,                  
                )
                cv2.putText(
                    frame,
                    "Tijeras",
                    (150, 300),
                    font,
                    tamaño_fuente,
                    color_contador,
                    espaciado_fuente,
                    cv2.LINE_AA,                  
                )
    if(contador>0):
        cv2.putText(
            frame,
            str(contador),
            posicion_contador,
            font,
            tamaño_fuente,
            color_contador,
            espaciado_fuente,
            cv2.LINE_AA,
        )



    #Cuando termina la cuenta 

    if(bandera==1):
        # *********************************************************************************************************************
        # Verifica si se detectaron manos
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Inicializa listas para las coordenadas X e Y de los puntos de referencia de la mano
                x_coords = []
                y_coords = []

                # Inicializa variables de las distancias de los dedos al centro de la mano
                distancia_pulgar = None
                distancia_indice = None
                distancia_corazon = None
                distancia_anular = None
                distancia_menique = None

                # Itera a través de los puntos de referencia de la mano derecha
                for idx, landmark in enumerate(hand_landmarks.landmark):
                    # Convierte las coordenadas normalizadas en coordenadas de píxeles
                    h, w, c = frame.shape
                    cx, cy = int(landmark.x * w), int(landmark.y * h)

                    # Agrega las coordenadas a las listas
                    x_coords.append(cx)
                    y_coords.append(cy)

                    # Calcula la distancia entre el punto de referencia (dedo) actual y el centro de la mano
                    if idx == 0:
                        center_x = cx
                        center_y = cy
                    distancia = math.sqrt((cx - center_x) ** 2 + (cy - center_y) ** 2)

                    # Asigna la distancia a la variable correspondiente según el dedo
                    if idx == mp_hands.HandLandmark.THUMB_TIP:
                        distancia_pulgar = distancia
                    elif idx == mp_hands.HandLandmark.INDEX_FINGER_TIP:
                        distancia_indice = distancia
                    elif idx == mp_hands.HandLandmark.MIDDLE_FINGER_TIP:
                        distancia_corazon = distancia
                    elif idx == mp_hands.HandLandmark.RING_FINGER_TIP:
                        distancia_anular = distancia
                    elif idx == mp_hands.HandLandmark.PINKY_TIP:
                        distancia_menique = distancia

                    # Dibuja un círculo en el punto de referencia (dedo) actual con un color diferente
                    if idx == mp_hands.HandLandmark.INDEX_FINGER_TIP:
                        cv2.circle(
                            frame, (cx, cy), 7, (0, 0, 255), -1
                        )  # Color rojo para el dedo índice
                    elif idx == mp_hands.HandLandmark.MIDDLE_FINGER_TIP:
                        cv2.circle(
                            frame, (cx, cy), 7, (0, 255, 0), -1
                        )  # Color verde para el dedo medio
                    elif idx == mp_hands.HandLandmark.RING_FINGER_TIP:
                        cv2.circle(
                            frame, (cx, cy), 7, (255, 0, 0), -1
                        )  # Color azul para el dedo anular
                    elif idx == mp_hands.HandLandmark.PINKY_TIP:
                        cv2.circle(
                         frame, (cx, cy), 7, (255, 255, 0), -1
                        )  # Color amarillo para el dedo meñique
                    # Dibuja un círculo blanco en el dedo gordo (pulgar)
                    elif idx == mp_hands.HandLandmark.THUMB_TIP:
                        cv2.circle(
                            frame, (cx, cy), 7, (0, 0, 0), -1
                        )  # Color blanco para el dedo gordo (pulgar)

                # Dibuja un círculo blanco en el centro de la mano
                cv2.circle(
                    frame, (center_x, center_y), 7, (255, 255, 255), -1
                )  # Color blanco para el centro de la mano

                # Muestra la distancia de cada dedo al centro de la mano en pantalla
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(
                    frame,
                    f"Pulgar: {distancia_pulgar:.2f}",
                    (20, 20),
                    font,
                    0.5,
                    (0, 0, 0),
                    1,
                    cv2.LINE_AA,
                )
                cv2.putText(
                    frame,
                    f"Índice: {distancia_indice:.2f}",
                    (20, 40),
                    font,
                    0.5,
                    (0, 0, 0),
                    1,
                    cv2.LINE_AA,
                )
                cv2.putText(
                    frame,
                    f"Medio: {distancia_corazon:.2f}",
                    (20, 60),
                    font,
                    0.5,
                    (0, 0, 0),
                    1,
                    cv2.LINE_AA,
                )
                cv2.putText(
                    frame,
                    f"Anular: {distancia_anular:.2f}",
                    (20, 80),
                    font,
                    0.5,
                    (0, 0, 0),
                    1,
                    cv2.LINE_AA,
                )
                cv2.putText(
                    frame,
                    f"Meñique: {distancia_menique:.2f}",
                    (20, 100),
                    font,
                    0.5,
                    (0, 0, 0),
                    1,
                    cv2.LINE_AA,
                )

                # Determina el gesto del jugador en función de las distancias de los dedos al centro de la mano
                if (
                    distancia_indice > 90
                    and distancia_pulgar > 100
                    and distancia_corazon > 90
                    and distancia_anular > 90
                    and distancia_menique > 90
                ):
                    resultado = "Papel"
                elif (
                    distancia_indice < 90
                    and distancia_pulgar < 90
                    and distancia_corazon < 90
                    and distancia_anular < 90
                    and distancia_menique < 90
                ):
                    resultado = "Piedra"
                elif (
                    distancia_indice > 90
                    and distancia_pulgar < 100
                    and distancia_corazon > 90
                    and distancia_anular < 90
                    and distancia_menique < 90
                ):
                    resultado = "Tijeras"
                else:
                    resultado = "esperando..."

                # Muestra el resultado en la pantalla
                cv2.putText(
                    frame, resultado, (20, 120), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA
                    
                )
                #Resultado ganador
                if(numero_aleatorio==1 and resultado=="Tijeras"):
                    ganador="Perdiste"
                elif(numero_aleatorio==1 and resultado=="Piedra"):
                    ganador="Empate"
                elif(numero_aleatorio==1 and resultado=="Papel"):
                    ganador="Ganaste"
                elif(numero_aleatorio==2 and resultado=="Tijeras"):
                    ganador="Ganaste"
                elif(numero_aleatorio==2 and resultado=="Piedra"):
                    ganador="Perdiste"
                elif(numero_aleatorio==2 and resultado=="Papel"):
                    ganador="Empate"
                elif(numero_aleatorio==3 and resultado=="Tijeras"):
                    ganador="Empate"
                elif(numero_aleatorio==3 and resultado=="Piedra"):
                    ganador="Gaanaste"
                elif(numero_aleatorio==3 and resultado=="Papel"):
                    ganador="Perdiste"
                
                                    
                cv2.putText(
                    frame, str(ganador), (150, 300), font, 3, (255, 255, 255), 1, cv2.LINE_AA
                )





    # Muestra la pantalla de la cámara
    cv2.imshow("", frame)
    # *********************************************************************************************************************
    # Sale del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    if cv2.waitKey(1) & 0xFF == ord("r"):
        bandera=0
        contador=3

# Libera la cámara y cierra la ventana
cap.release()
cv2.destroyAllWindows()
