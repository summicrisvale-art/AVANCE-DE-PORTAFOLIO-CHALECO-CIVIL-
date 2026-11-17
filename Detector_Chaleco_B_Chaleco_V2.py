import cv2

cap = cv2.VideoCapture("http://10.217.192.93:4747/video")

# Clasificador entrenado para el chaleco
ChalecoClassif = cv2.CascadeClassifier('cascade.xml')

while True:
    ret, frame = cap.read()
    if not ret: 
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    chalecos = ChalecoClassif.detectMultiScale(
        gray,
        scaleFactor=1.1,  # Define qué tan rápido cambia el tamaño de la ventana de búsqueda.
        minNeighbors=70,  # Detectada varias veces al mismo tiempo para confirmar que realmente es el objeto.
        minSize=(230, 230)  # Tamaño mínimo ajustado para objetos más grandes (ancho, alto).
    )

    for (x, y, w, h) in chalecos:
        # Márgenes adaptados para cubrir correctamente el torso con el chaleco
        margen_x = int(w * 0.15)
        margen_y = int(margen_x * 0.15)

        x1 = max(x - margen_x, 0)
        y1 = max(y - margen_y, 0)
        x2 = x + w + margen_x
        y2 = y + h + margen_y

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            frame, 'Chaleco Ing Civil (UTP)', (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA
        )

    cv2.imshow('Deteccion - Chaleco Ing Civil UTP', frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
