import cv2
import numpy as np
import imutils
import os
import time

Datos = "p"       # Carpeta para las imágenes positivas del chaleco
if not os.path.exists(Datos):
    print('Carpeta creada: ', Datos)
    os.makedirs(Datos)

cap = cv2.VideoCapture("http://10.217.192.93:4747/video") # Conexión a DroidCam via IP

x1, y1 = 120, 40
x2, y2 = 620, 520  # Ancho = 500, Alto = 480

count = 0
max_imagenes = 250       # Límite aumentado a 250 fotos positivas
tiempo_espera = 0.1      # Intervalo reducido a 0.1 segundos
capturando = False       # Bandera para esperar la tecla 'k'

print("Coloca el chaleco dentro del recuadro azul.")
print("Presiona la tecla 'k' en la ventana del video para comenzar la captura automática.")

while True:

    ret, frame = cap.read()
    if ret == False: break
    imAux = frame.copy()
    cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,0),2)

    objeto = imAux[y1:y2,x1:x2]
    objeto = cv2.resize(objeto, (200, 200), interpolation=cv2.INTER_CUBIC)

    k = cv2.waitKey(1)

    # Iniciar captura al presionar 'k' o 'K'
    if k == ord('k') or k == ord('K'):
        capturando = True
        ultimo_tiempo = time.time()
        print("¡Iniciando captura automática del Chaleco Ing Civil (UTP)...")

    # Guardado automático cada 0.1 segundos hasta llegar a 250
    if capturando:
        tiempo_actual = time.time()
        if (tiempo_actual - ultimo_tiempo) >= tiempo_espera:
            if count < max_imagenes:
                cv2.imwrite(Datos+'/chaleco_utp_{}.jpg'.format(count), objeto)
                print('Imagen guardada [{}/{}]: '.format(count+1, max_imagenes) + Datos+'/chaleco_utp_{}.jpg'.format(count))
                count = count + 1
                ultimo_tiempo = tiempo_actual
            else:
                print("¡Proceso finalizado! Se han tomado las 250 fotos positivas del Chaleco Ing Civil (UTP).")
                break

    if k == 27:
        break

    cv2.imshow('frame', frame)
    cv2.imshow('objeto', objeto)

cap.release()
cv2.destroyAllWindows()
