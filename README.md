# 🏠 Sistema di Sicurezza con YOLO e ONNX

> *"Da Times Square a casa mia: un sistema di allarme che riconosce le persone e ti avvisa su Telegram"*

Un sistema di sicurezza basato su intelligenza artificiale che:
- 🔍 Rileva le persone in tempo reale usando una webcam
- 📱 Invia notifiche con foto su Telegram
- ⚡ Funziona su CPU (40+ FPS)
- 🔒 100% locale: nessun dato inviato al cloud
- 💰 Gratis: software open source, nessun abbonamento

---

## 📸 Demo

| Times Square (test pubblico) | Allarme domestico |
|------------------------------|-------------------|
| *(inserisci screenshot)*     | *(inserisci screenshot)* |

---

## 🚀 Come funziona

1. La webcam cattura i frame
2. YOLOv8 (ottimizzato con ONNX) riconosce le persone
3. Se viene rilevata una persona, scatta l'allarme
4. Ricevi un messaggio e una foto su Telegram

---

## 🛠️ Cosa serve

### Hardware
- PC con Windows/Linux/Mac
- CPU: Intel i5 / AMD Ryzen 5 o superiore (consigliato)
- RAM: 8 GB (16 GB consigliati)
- Webcam USB (qualsiasi modello)

### Software
- Python 3.8+
- Account Telegram (gratis)

---

## 📦 Installazione

### 1. Clona il repository

```bash
git clone https://github.com/tuo-username/security-system-yolo.git
cd security-system-yolo

## Crea l'ambiente virtuale

python -m venv env

# Windows
env\Scripts\activate

# Linux/Mac
source env/bin/activate

## Installa le dipendenze
pip install -r requirements.txt

##Configura Telegram
Apri Telegram e cerca @BotFather

Invia /newbot e segui le istruzioni

Salva il TOKEN ricevuto

Ottieni il CHAT_ID:

    Invia un messaggio al bot

    Esegui: https://api.telegram.org/bot[TOKEN]/getUpdates

    Prendi il chat_id dalla risposta

## Configura il sistema
Apri index.py e inserisci:
TELEGRAM_TOKEN = "IL_TUO_TOKEN"
TELEGRAM_CHAT_ID = "IL_TUO_CHAT_ID"

## Avvio
python index.py

## Configurazione avanzata
Nel file index.py puoi modificare:
CONFIDENCE_THRESHOLD	0.4	Soglia di confidenza (più alto = più preciso, più basso = più sensibile)
ALARM_COOLDOWN	10	Secondi tra un allarme e l'altro (evita spam)
STABILIZATION_TIME	5	Secondi all'avvio prima di attivare gli allarmi

## Prestazioni
FPS medi	40-45 FPS (su CPU AMD Ryzen 7 7700)
Tempo inferenza	21-24 ms per frame
Dimensione modello	12 MB (ONNX)
Consumo RAM	~500 MB (incluso ambiente Python)
Tempo avvio	< 3 secondi

## Privacy e uso etico

Questo sistema è progettato per uso esclusivamente privato.
✅ Cosa puoi fare:

    Installarlo a casa tua

    Usarlo nel tuo ufficio personale

    Monitorare il tuo negozio in orari di chiusura

❌ Cosa NON devi fare:

    Puntare telecamere su spazi pubblici

    Registrare senza informare le persone

    Usare il sistema per sorvegliare persone senza il loro consenso

    Conservare i video più del necessario

Tutti i dati rimangono sul tuo PC. Nessuna immagine viene inviata al cloud.

## Tecnologie utilizzate

    YOLOv8 - Riconoscimento oggetti

    ONNX Runtime - Inferenza ottimizzata per CPU

    OpenCV - Elaborazione video

    Telegram Bot API - Notifiche

## Struttura del progetto
security-system-yolo/
│
├── index.py                # Script principale (tutto in uno)
├── yolov8n.onnx            # Modello ONNX (12 MB)
├── requirements.txt        # Dipendenze Python
├── .gitignore              # File esclusi da git
├── LICENSE                 # Licenza MIT
└── README.md               # Questo file

## Sviluppi futuri

    Riconoscimento facciale (distinguere residenti da intrusi)

    Salvataggio video degli eventi (10 secondi pre/post allarme)

    Dashboard web per monitoraggio remoto

    Supporto multi-camera

    Log in CSV per analisi storiche

    Integrazione con sensori PIR per ridurre i falsi allarmi

🧪 Test effettuati
Test 1: Times Square (New York)

    Scenario: Flusso video pubblico con centinaia di persone e veicoli

    Risultato: Riconoscimento stabile anche in scene affollate

    Performance: 40+ FPS senza degrado

Test 2: Ambiente domestico

    Scenario: Stanza vuota → persona entra

    Risultato: Allarme scattato in < 1 secondo

    Notifica: Messaggio + foto ricevuti su Telegram

⚠️ IMPORTANTE

Questo progetto è a scopo educativo e dimostrativo. Non sostituisce un sistema di sicurezza professionale.

    Usalo con responsabilità

    Rispetta sempre la privacy altrui

    Verifica le leggi locali sulla videosorveglianza prima dell'uso

📞 Domande?

Apri una issue su GitHub o contattami su [LinkedIn](https://www.linkedin.com/in/dario-ferrero-b12298388/?lipi=urn%3Ali%3Apage%3Ad_flagship3_feed%3BZDpcDVdCT%2BmOopA02P9SPQ%3D%3D).