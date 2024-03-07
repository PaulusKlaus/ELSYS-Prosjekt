import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

def read(trailer_block, key, block_addrs):
    try:
        reader = SimpleMFRC522()
        id, data = reader.read()
        return id, data
    except Exception as e:
        print("An error occurred:", e)
        return None, None
    finally:
        GPIO.cleanup()

trailer_block = 11
key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
block_addrs = [8, 9, 10]

GPIO.setwarnings(False)  # Suppress GPIO warnings
id, text = read(trailer_block, key, block_addrs)
while True: 
    while not id:
        id, text = read(trailer_block, key, block_addrs)
        print(id)
        id = None