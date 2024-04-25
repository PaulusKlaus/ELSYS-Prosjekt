 import RPi.GPIO as GPIO
 from mfrc522 import SimpleMFRC522

# Function to read the card id and data
def read():
    try:
        reader = SimpleMFRC522() # Create an object of the class SimpleMFRC522
        id, data = reader.read() # Read the card id and data
        return id, data 
    except Exception as e:
        print("An error occurred:", e)
        return None, None
    finally:
        GPIO.cleanup() # Clean up the GPIO pins

GPIO.setwarnings(False)  # Suppress GPIO warnings

# Function to get the card id
def getCardId():
    global id
    functionID = None
    while not id:
        id = read()
    functionID = id
    id = None
    return functionID
