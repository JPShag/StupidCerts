import binascii
import sys
import shutil
import os
import logging
from asn1crypto import pkcs12
import argparse

def read_pfx_file(filename):
    """
    Read the contents of a PFX file.
    
    Args:
        filename (str): Path to the PFX file.
    
    Returns:
        bytes: The content of the PFX file.
    """
    with open(filename, "rb") as file:
        return file.read()

def move_incorrect_file(filename):
    """
    Move an incorrect PFX file to a designated 'deleted' directory.
    
    Args:
        filename (str): Path to the PFX file.
    """
    destination = filename.replace('certs', 'certs_deleted')
    shutil.move(filename, destination)
    logging.error(f'File moved to {destination}')

def extract_mac_data(pfx):
    """
    Extract MAC data from the PFX structure.
    
    Args:
        pfx (PKCS12): PFX structure loaded from asn1crypto.
    
    Returns:
        tuple: Contains MAC algorithm, salt, iterations, and digest.
    """
    mac_data = pfx['mac_data']
    return (
        mac_data['mac']['digest_algorithm']['algorithm'].native,
        mac_data['mac_salt'].native,
        mac_data['iterations'].native if mac_data['iterations'].native else 1,  # Default to 1 if not specified
        mac_data['mac']['digest'].native
    )

def print_pfx_info(filename, mac_algo, key_length, iterations, salt, data, stored_hmac):
    """
    Print information about the PFX file in a formatted string suitable for password cracking tools.
    
    Args:
        filename (str): Path to the PFX file.
        mac_algo (str): MAC algorithm used.
        key_length (int): Key length of the MAC algorithm.
        iterations (int): Number of iterations used in MAC processing.
        salt (bytes): Salt used in MAC processing.
        data (bytes): Encoded data from PFX.
        stored_hmac (bytes): Stored HMAC value from PFX.
    """
    size = len(salt)
    sys.stdout.write(
        f"{os.path.basename(filename)}:$pfxng${mac_algo}${key_length}${iterations}${size}$"
        f"{binascii.hexlify(salt).decode()}${binascii.hexlify(data).decode()}${binascii.hexlify(stored_hmac).decode()}:::::{filename}\n"
    )

def parse_pkcs12(filename):
    """
    Parse a PFX file to extract and print PKCS#12 data.
    
    Args:
        filename (str): Path to the PFX file.
    """
    try:
        data = read_pfx_file(filename)
        pfx = pkcs12.Pfx.load(data)
        auth_safe = pfx['auth_safe']
        
        if auth_safe['content_type'].native != 'data':
            raise ValueError('Auth safe content type is not data')

        mac_algo, salt, iterations, stored_hmac = extract_mac_data(pfx)
        key_length = {
            'sha1': 20, 'sha224': 28, 'sha256': 32,
            'sha384': 48, 'sha512': 64, 'sha512_224': 28, 'sha512_256': 32
        }.get(mac_algo)

        if key_length is None:
            raise ValueError(f"Unsupported MAC algorithm: {mac_algo}")

        data = auth_safe['content'].contents
        print_pfx_info(filename, mac_algo, key_length, iterations, salt, data, stored_hmac)

    except Exception as e:
        logging.error(f"{filename} is incorrect: {str(e)}")
        move_incorrect_file(filename)

def parse_arguments():
    """
    Parse command-line arguments.
    
    Returns:
        Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Process PFX files to extract and verify PKCS#12 data.')
    parser.add_argument('filenames', nargs='+', help='PFX file paths to process')
    parser.add_argument('--log-level', default='ERROR', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], help='Set the logging level')
    return parser.parse_args()

def main():
    """
    Main function to process command-line arguments and handle PFX files.
    """
    args = parse_arguments()
    logging.basicConfig(level=args.log_level.upper())
    for filename in args.filenames:
        parse_pkcs12(filename)

if __name__ == "__main__":
    main()
