import hashlib
import os




if __name__ == '__main__':
    file_path = r'../resources\compressed_files\DUMMY_compressed_files - copia.txt'
    file_hash = get_hash(file_path)
    print(f'The hash of the file {file_path} is: {file_hash}')
