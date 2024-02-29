import hashlib
from configparser import ConfigParser
from datetime import datetime


def select_hash_algorithm(day: int) -> str:
    """
    Selects the hash algorithm based on the day of the month.

    Args:
        day (int): The day of the month.

    Returns:
        str: The selected hash algorithm ('sha512' or 'sha3_384').
    """
    return 'sha512' if day % 2 == 0 else 'sha3_384'


def calculate_file_hash(file_path: str, day: int) -> str:
    """
    Calculates the hash of a file using the selected algorithm.

    Args:
        file_path (str): The path to the file.
        day (int): The day of the month.

    Returns:
        str: The calculated hash value.
    """
    calculated_hash = hashlib.new(select_hash_algorithm(day))

    with open(file_path, 'rb') as file:
        for block in iter(lambda: file.read(4096), b""):
            calculated_hash.update(block)

    return calculated_hash.hexdigest()


def calculate_mac(hash_value: str, token: str, day: int) -> str:
    """
    Calculates the Message Authentication Code (MAC) using the hash and token.

    Args:
        hash_value (str): The hash value of the file.
        token (str): The token read from the configuration file.
        day (int): The day of the month.

    Returns:
        str: The calculated MAC value.
    """
    calculated_mac = hashlib.new(select_hash_algorithm(day + 1))

    if day % 2 == 0:
        calculated_mac.update((hash_value + token).encode())
    else:
        calculated_mac.update((token + hash_value).encode())

    return calculated_mac.hexdigest()


def get_hash(name: str, date_today: datetime) -> str:
    """
    Calculates the hash of a file using different algorithms and applies a Message Authentication Code (MAC).

    Args:
        name (str): The name or path of the file.
        date_today (datetime): The current date.

    Returns:
        str: The final hash value after applying MAC.
    """
    day = int(date_today.strftime('%d'))

    # Calculate the file hash
    hash_value = calculate_file_hash(name, day)

    # Read the token from the configuration file
    config = ConfigParser()
    config.read("config.ini")
    token = config.get("HASHING", "token")

    # Calculate the MAC using the hash and token
    mac_value = calculate_mac(hash_value, token, day)

    return mac_value
