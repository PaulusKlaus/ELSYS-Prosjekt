from mfrc522 import MFRC522

reader = MFRC522()

# Legger til en liste med autoriserte ID-er
authorized_ids = [
    (0x04, 0xA5, 0xB6, 0xC7),  # Eksempel ID, bytt ut med faktiske ID-er
    (0x12, 0x34, 0x56, 0x78)   # Et annet eksempel, endre dette også
]

def read(trailer_block, key, block_addrs):
    (status, TagType) = reader.Request(reader.PICC_REQIDL)
    if status != reader.MI_OK:
        return None, None
    (status, uid) = reader.Anticoll()
    if status != reader.MI_OK:
        return None, None
    id = tuple(uid)  # Konverterer uid til en tuple for sammenligning
    reader.SelectTag(uid)
    status = reader.Authenticate(
        reader.PICC_AUTHENT1A, trailer_block, key, uid)
    data = []
    text_read = ''
    if status == reader.MI_OK:
        for block_num in block_addrs:
            block = reader.ReadTag(block_num)
            if block:
                data += block
        if data:
            text_read = ''.join(chr(i) for i in data)
    reader.StopAuth()
    return id, text_read

def check_access(id):
    if id in authorized_ids:
        return True
    return False

trailer_block = 11
key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
block_addrs = [8,9,10]
id, text = read(trailer_block, key, block_addrs)

while not id:
    id, text = read(trailer_block, key, block_addrs)

if check_access(id):
    print(f"ID {id} har tilgang.")
    # Aktiver knappen her
else:
    print(f"ID {id} har ikke tilgang.")
    # Knappen forblir deaktivert

print(id)
print(text)
