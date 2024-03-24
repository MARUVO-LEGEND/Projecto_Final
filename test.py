import face_recognition
import cv2
import numpy as np
import os

# Função para carregar as imagens da pasta e seus respectivos nomes
def carregar_imagens_pasta(pasta):
    imagens_conhecidas = []
    nomes = []

    for nome_arquivo in os.listdir(pasta):
        nome, extensao = os.path.splitext(nome_arquivo)
        if extensao in ['.jpg', '.png']:
            imagem = face_recognition.load_image_file(os.path.join(pasta, nome_arquivo))
            encoding = face_recognition.face_encodings(imagem)[0]
            imagens_conhecidas.append(encoding)
            nomes.append(nome)

    return imagens_conhecidas, nomes

# Pasta onde as imagens das faces conhecidas estão localizadas
pasta_faces_conhecidas = 'codigo_mario/source_code/images'

# Carregar as imagens e nomes das faces conhecidas
faces_conhecidas, nomes_conhecidos = carregar_imagens_pasta(pasta_faces_conhecidas)

# Inicializar a webcam
video_capture = cv2.VideoCapture(0)

while True:
    # Capturar o quadro da webcam
    ret, frame = video_capture.read()

    # Converter o quadro de BGR (OpenCV) para RGB (face_recognition)
    rgb_frame = frame[:, :, ::-1]

    # Encontrar as localizações das faces na imagem capturada
    face_locations = face_recognition.face_locations(rgb_frame)

    # Percorrer cada localização de face encontrada na imagem capturada
    for face_location in face_locations:
        # Recortar a face da imagem capturada
        top, right, bottom, left = face_location
        face_image = rgb_frame[top:bottom, left:right]

        # Codificar a face recortada
        face_encoding =face_image

        # Comparar a face encontrada com as faces conhecidas
        matches = face_recognition.compare_faces(faces_conhecidas, face_encoding)

        # Verificar se alguma face conhecida corresponde à face encontrada
        nome_encontrado = "Desconhecido"
        if True in matches:
            index = matches.index(True)
            nome_encontrado = nomes_conhecidos[index]

        # Desenhar um retângulo em torno da face e mostrar o nome
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, nome_encontrado, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    # Mostrar o quadro resultante
    cv2.imshow('Video', frame)

    # Se pressionar 'q', sair do loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar a captura da webcam e fechar todas as janelas
video_capture.release()
cv2.destroyAllWindows()
