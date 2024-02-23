import hashlib

def get_hash(name, algorithm='sha256'):
    calculated_hash = hashlib.new(algorithm)

    with open(name, 'rb') as file:
        block = file.read(4096)
        while len(block) > 0:
            calculated_hash.update(block)
            block = file.read(4096)

    return calculated_hash.hexdigest()

'''
file_path = 'C:/Users/Ignacio/Desktop/Universidad/I.informatica/4º/SSII/Recursos/GIF2.gif'
file_hash = get_hash(file_path)
print(f'The hash of the file {file_path} is: {file_hash}')
'''