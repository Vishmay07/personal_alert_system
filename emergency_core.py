# emergency_core.py
import geocoder
import smtplib
from email.message import EmailMessage
import sounddevice as sd
from scipy.io.wavfile import write
import cv2
import datetime

def get_location():
    g = geocoder.ip('me')
    if g.ok:
        lat, lng = g.latlng
        return f"http://maps.google.com/?q={lat},{lng}"
    return "Location unavailable"

def send_email_alert(location_link, image_file="intruder.png", audio_file="pressing_alarm.mp3"):
    msg = EmailMessage()
    msg['Subject'] = '🚨 EMERGENCY ALERT'
    msg['From'] = 'vishmayparmar22@gmail.com'
    msg['To'] = 'receiver_email@gmail.com'
    msg.set_content(f"Emergency! I need help. Location: {location_link}")

    try:
        with open(image_file, 'rb') as img:
            msg.add_attachment(img.read(), maintype='image', subtype='png', filename=image_file)
        with open(audio_file, 'rb') as aud:
            msg.add_attachment(aud.read(), maintype='audio', subtype='mp3', filename=audio_file)
    except:
        pass  # Files might not exist yet

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('vishmayparmar22@gmail.com', 'zgix ulsq ybfq conw')
            smtp.send_message(msg)
        print("✅ Email sent!")
    except Exception as e:
        print("❌ Failed to send email:", e)

def record_audio(filename='alarm.wav', duration=5):
    fs = 44100
    print("🎙️ Recording Audio...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
    write(filename, fs, recording)

def capture_photo(filename='intruder.png'):
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if ret:
        cv2.imwrite(filename, frame)
    cam.release()
    cv2.destroyAllWindows()

def save_alert_log(location):
    with open("emergency_log.txt", "a") as log:
        log.write(f"{datetime.datetime.now()} - Emergency at: {location}\n")

def emergency_procedure():
    location = get_location()
    capture_photo()
    record_audio()
    send_email_alert(location)
    save_alert_log(location)
