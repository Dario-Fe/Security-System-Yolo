import cv2
import time
import requests
from ultralytics import YOLO
from collections import deque
import numpy as np

# ===== CONFIGURAZIONE =====
TELEGRAM_TOKEN = "codice token"
TELEGRAM_CHAT_ID = "codice ID"

# Soglia di confidenza per il riconoscimento
CONFIDENCE_THRESHOLD = 0.4  # Leggermente più basso per essere più sensibile

# Tempo minimo tra un allarme e l'altro (secondi) - evita spam
ALARM_COOLDOWN = 10

# Tempo di "stabilizzazione" - se una persona è già presente all'avvio, non allarmare subito
STABILIZATION_TIME = 5  # secondi

# ===== FUNZIONI TELEGRAM =====
def send_telegram_message(message):
    """Invia un messaggio via Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    try:
        response = requests.post(url, data=payload)
        return response.ok
    except Exception as e:
        print(f"❌ Errore invio messaggio: {e}")
        return False

def send_telegram_photo(image, caption="🚨 Allarme sicurezza!"):
    """Invia una foto via Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    
    # Codifica l'immagine in JPEG
    _, img_encoded = cv2.imencode('.jpg', image)
    files = {'photo': ('alert.jpg', img_encoded.tobytes(), 'image/jpeg')}
    data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': caption}
    
    try:
        response = requests.post(url, files=files, data=data)
        return response.ok
    except Exception as e:
        print(f"❌ Errore invio foto: {e}")
        return False

# ===== FUNZIONI PRINCIPALI =====
def rileva_persone(results, frame_shape, threshold=CONFIDENCE_THRESHOLD):
    """
    Rileva tutte le persone nel frame.
    Restituisce: (lista_persone, numero_persone)
    """
    persone = []
    for box in results[0].boxes:
        class_id = int(box.cls[0])
        class_name = results[0].names[class_id]
        confidence = float(box.conf[0])
        
        # Controlla solo persone
        if class_name == 'person' and confidence >= threshold:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            
            persone.append({
                'bbox': (x1, y1, x2, y2),
                'center': (cx, cy),
                'confidence': confidence
            })
    
    return persone, len(persone)

def invia_allarme(frame, persone, counter):
    """
    Invia allarme con foto e dettagli
    """
    message = f"""
🚨 <b>ALLARME SICUREZZA!</b> 🚨

👤 <b>Persona rilevata nella stanza</b>
📊 Numero persone: {len(persone)}
🎯 Confidenza massima: {max([p['confidence'] for p in persone]):.2%}
⏰ Ora: {time.strftime('%H:%M:%S')}
📊 Allarme #{counter}
    """
    
    print(f"\n🔴 ALLARME #{counter} - {len(persone)} persona/e rilevata/e!")
    for i, p in enumerate(persone, 1):
        print(f"   Persona {i}: confidenza {p['confidence']:.2%} a posizione {p['center']}")
    
    # Invia Telegram
    if TELEGRAM_TOKEN != "IL_TUO_TOKEN_QUI":
        print("📤 Invio allarme su Telegram...")
        send_telegram_message(message)
        send_telegram_photo(frame, caption=f"🚨 Allarme #{counter} - {len(persone)} persona/e rilevata/e!")
        print("✅ Allarme inviato!")
    else:
        print("⚠️ Telegram non configurato - allarme solo a schermo")
    
    return True

# ===== MAIN =====
def main():
    # Carica il modello ONNX
    print("📦 Caricamento modello YOLO...")
    model = YOLO("yolov8n.onnx", task='detect')
    print("✅ Modello caricato!")
    
    # Apri la webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Errore: Impossibile aprire la webcam")
        return
    
    print("\n" + "="*50)
    print("🔒 SISTEMA DI SICUREZZA AVVIATO")
    print("="*50)
    print(f"📷 Webcam: attiva")
    print(f"🎯 Rilevazione: PERSONE (confidenza ≥ {CONFIDENCE_THRESHOLD:.0%})")
    print(f"⏱️  Cooldown allarme: {ALARM_COOLDOWN}s")
    print(f"📱 Telegram: {'✅ CONFIGURATO' if TELEGRAM_TOKEN != 'IL_TUO_TOKEN_QUI' else '❌ NON CONFIGURATO'}")
    print("="*50)
    print("Premi 'q' per uscire\n")
    
    last_alarm_time = 0
    alarm_counter = 0
    start_time = time.time()
    first_person_detected = False
    
    # Per il tracking delle persone (opzionale)
    person_history = deque(maxlen=30)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Errore: Impossibile leggere il frame")
            break
        
        # Esegui inferenza
        results = model(frame, device="cpu", conf=CONFIDENCE_THRESHOLD)
        
        # Rileva persone
        persone, num_persone = rileva_persone(results, frame.shape)
        
        # MOSTRA STATO CORRENTE
        current_time = time.time()
        elapsed = current_time - start_time
        
        # Determina lo stato
        if num_persone > 0:
            stato = "🔴 ALLARME!"
            stato_color = (0, 0, 255)  # Rosso
        else:
            stato = "✅ SICURO"
            stato_color = (0, 255, 0)  # Verde
        
        # Decidi se scatta l'allarme
        trigger_alarm = False
        
        # Solo se sono passati almeno STABILIZATION_TIME secondi dall'avvio
        if elapsed > STABILIZATION_TIME:
            # Se ci sono persone E non è scattato un allarme di recente
            if num_persone > 0 and (current_time - last_alarm_time > ALARM_COOLDOWN):
                trigger_alarm = True
        
        # Se è la prima persona rilevata dopo l'avvio, aspetta stabilizzazione
        if num_persone > 0 and not first_person_detected and elapsed > STABILIZATION_TIME:
            first_person_detected = True
        
        # Scatta l'allarme
        if trigger_alarm:
            # Marca il frame con i riquadri rossi per le persone
            frame_with_boxes = results[0].plot()
            
            # Aggiungi overlay di allarme
            h, w = frame_with_boxes.shape[:2]
            overlay = frame_with_boxes.copy()
            cv2.rectangle(overlay, (0, 0), (w, 60), (0, 0, 255), -1)
            cv2.addWeighted(overlay, 0.3, frame_with_boxes, 0.7, 0, frame_with_boxes)
            
            cv2.putText(frame_with_boxes, "🚨 ALLARME!", (10, 40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
            
            # Invia allarme
            alarm_counter += 1
            invia_allarme(frame_with_boxes, persone, alarm_counter)
            last_alarm_time = current_time
            
            # Usa il frame con i box per la visualizzazione
            display_frame = frame_with_boxes
        else:
            # Usa il frame annotato normale
            display_frame = results[0].plot()
        
        # AGGIUNGI OVERLAY INFORMAZIONI
        # Stato in alto a sinistra
        cv2.putText(display_frame, stato, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, stato_color, 2)
        
        # Contatore persone
        cv2.putText(display_frame, f"Persone: {num_persone}", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Contatore allarmi
        cv2.putText(display_frame, f"Allarmi: {alarm_counter}", (10, 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Tempo di cooldown rimanente
        if num_persone > 0:
            cooldown_left = max(0, ALARM_COOLDOWN - (current_time - last_alarm_time))
            if cooldown_left > 0:
                cv2.putText(display_frame, f"Cooldown: {cooldown_left:.0f}s", (10, 120), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        
        # Tempo di stabilizzazione
        if elapsed < STABILIZATION_TIME:
            stabil_left = STABILIZATION_TIME - elapsed
            cv2.putText(display_frame, f"Stabilizzazione: {stabil_left:.0f}s", 
                       (display_frame.shape[1] - 250, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
        
        # Mostra il frame
        cv2.imshow('Sistema di Sicurezza - Rilevazione Persone', display_frame)
        
        # Esci con 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print(f"\n{'='*50}")
    print(f"🔒 SISTEMA TERMINATO")
    print(f"📊 Allarmi totali scattati: {alarm_counter}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
