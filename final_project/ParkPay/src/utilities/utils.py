from random import randint

def build_payment_information(card_number, name_on_card, expiration_date, zip):
    return {"card": card_number,
            "name_on_card": name_on_card,
            "expiration_date": expiration_date,
            "zip": zip}

def build_vehicle_information(vid, state, plate, type):
    return {"state": state,
            "plate": plate,
            "type": type}

def generate_transaction_id():
    id = ''.join(["%s" % randint(0, 9) for num in range(0, 9)])
    id = id[:3] + '-' + id[3:7] + '-' + id[7:]
    return id

