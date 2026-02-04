# ping_worker.py
import time
import requests

while True:
    try:
        requests.get("https://reading-t9nr.onrender.com")
        print("Pinged successfully!")
    except Exception as e:
        print(f"Error pinging: {e}")
    time.sleep(300)  
