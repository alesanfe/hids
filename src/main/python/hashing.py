import hashlib
import os


def get_hash(name, date):
    # Selecciona el algoritmo de hash basándose en el día de la fecha
    day = int(date.today().strftime('%d'))
    if day % 2 == 0:
        algorithm = 'sha256'
    else:
        algorithm = 'md5'

    calculated_hash = hashlib.new(algorithm)

    # Agrega la fecha al cálculo del hash
    calculated_hash.update(date.today().strftime('%Y-%m-%d').encode('utf-8'))

    # Codifica el día de manera más compleja y aplicando otra función hash
    encoded_day = hashlib.sha256(str(day).encode('utf-8')).hexdigest()
    calculated_hash.update(encoded_day.encode('utf-8'))

    with open(name, 'rb') as file:
        for block in iter(lambda: file.read(4096), b""):
            calculated_hash.update(block)

    return calculated_hash.hexdigest()



