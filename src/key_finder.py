import bitcoin  # For conversions between private and public keys
import bitcoinlib  # For Bitcoin operations
from ecdsa import SECP256k1, numbertheory  # For elliptic curve operations
from ecdsa.ellipticcurve import Point  # To represent points on the curve
# from hashlib import sha256  # For hash functions
import math  # For mathematical operations
import time


class KeyFinder:
    """
    KeyFinder class to find the private key corresponding to a Bitcoin public address.

    This class implements the Baby-step Giant-step algorithm to efficiently search for the private key
    within a specified range. It provides methods to generate public addresses and WIF (Wallet Import Format)
    from private keys, as well as to calculate public key points on the elliptic curve.

    Methods:
        generate_public(private_key): Generates a public address from a private key.
        generate_wif(private_key): Converts a private key to Wallet Import Format (WIF).
        find_private_key(min_range, max_range, target_address): Searches for the private key that corresponds to the target address.
        find_public_key(private_key): Finds the public key corresponding to a given private key.
        calculate_public_key_point(target_public_key): Calculates the (x, y) point of the public key on the elliptic curve.
        bsgs(target_point, max_steps, start): Implements the Baby-step Giant-step algorithm to find the private key.
        solve_puzzle(target_public_key, target_address, start_range_hex, end_range_hex): Main method to solve the puzzle and find the private key.
    """

    @staticmethod
    def find_private_key(min_range, max_range, target_address):
        """Searches for the private key that corresponds to the target address."""
        start_time = time.time()  # Marks the start time
        keys_checked = 0  # Counter for checked keys

        # Iterates over the range of private keys
        for private_key in range(min_range, max_range + 1):
            private_key_hex = format(private_key, '064x')  # Converts the private key to hexadecimal
            public_address = KeyFinder.find_public_key(private_key_hex)  # Generates the public address

            keys_checked += 1  # Increments the counter
            # Prints progress every 1000 checked keys
            if keys_checked % 1000 == 0:
                elapsed_time = time.time() - start_time  # Calculates elapsed time
                print(f"Keys checked: {keys_checked}, Elapsed time: {elapsed_time:.2f} seconds")

            # Checks if the generated public address matches the target address
            if public_address == target_address:
                return private_key_hex  # Returns the found private key

        return None  # Returns None if the private key is not found

    @staticmethod
    def find_public_key(private_key):
        """Finds the public key corresponding to a given private key."""
        private_key_decimal = int(private_key, 16)  # Converts the private key from hexadecimal to decimal
        public_key = bitcoin.privkey_to_pubkey(private_key_decimal)  # Generates the public key
        return public_key  # Returns the public key

    @staticmethod
    def generate_wif(private_key):
        """Converts a private key to Wallet Import Format (WIF)."""
        key = bitcoinlib.keys.Key(private_key)  # Creates a key object
        return key.wif()  # Returns the WIF format of the private key

    def __init__(self):
        # Elliptic curve SECP256k1 and its generator
        self.curve = SECP256k1.curve
        self.G = SECP256k1.generator

    def calculate_public_key_point(self, target_public_key):
        """Calculates the (x, y) point of the public key on the elliptic curve."""
        public_key_x = int(target_public_key[2:], 16)  # Extracts the x coordinate from the public key
        # Calculates y^2 using the elliptic curve equation
        y_square = (public_key_x ** 3 + self.curve.a() * public_key_x + self.curve.b()) % self.curve.p()
        public_key_y = numbertheory.square_root_mod_prime(y_square, self.curve.p())  # Calculates the square root

        # Adjusts y depending on the prefix of the public key
        if (target_public_key.startswith('02') and public_key_y % 2 != 0) or (
                target_public_key.startswith('03') and public_key_y % 2 == 0):
            public_key_y = self.curve.p() - public_key_y  # Adjusts y to the correct value

        # Returns the (x, y) point on the curve
        return Point(self.curve, public_key_x, public_key_y, SECP256k1.order)

    def bsgs(self, target_point, max_steps, start):
        """Implements the Baby-step Giant-step algorithm to find the private key."""
        baby_steps = {}  # Dictionary to store baby steps
        giant_stride = self.G * max_steps  # Calculates the giant step
        steps_tried = 0  # Counter for tried steps

        current = self.G * start  # Starts with the generator point multiplied by the start
        # Fills the dictionary with baby steps
        for i in range(max_steps):
            baby_steps[(current.x(), current.y())] = i  # Stores the current point
            current = current + self.G  # Moves to the next point
            steps_tried += 1  # Increments the counter

        current = target_point  # Starts searching for the target point
        # Tries to find a match with the baby steps
        for j in range(max_steps):
            current_key = (current.x(), current.y())  # Gets the key of the current point
            if current_key in baby_steps:  # Checks if the point is in the baby steps
                return start + j * max_steps + baby_steps[current_key], steps_tried  # Returns the found private key
            current = current + (self.G * (-max_steps))  # Moves back to the next point
            steps_tried += 1  # Increments the counter

        return None, steps_tried  # Returns None if the key is not found

    def solve_puzzle(self, target_public_key, target_address, start_range_hex, end_range_hex):
        """Main method to solve the puzzle and find the private key."""
        start_range = int(start_range_hex, 16)  # Converts the start range from hexadecimal to decimal
        end_range = int(end_range_hex, 16)  # Converts the end range from hexadecimal to decimal

        interval_size = end_range - start_range + 1  # Calculates the size of the interval
        max_steps = 2 ** int(math.log2(math.sqrt(interval_size)))  # Calculates the maximum number of steps

        target_public_key_point = self.calculate_public_key_point(target_public_key)  # Calculates the public key point

        start_time = time.time()  # Marks the start time
        total_steps_tried = 0  # Total counter for tried steps
        private_key_integer = None  # Initializes the private key variable

        # Iterates over the range of private keys
        for start in range(start_range, end_range, max_steps):
            result, steps = self.bsgs(target_public_key_point, max_steps, start)  # Calls the BSGS algorithm
            total_steps_tried += steps  # Updates the total tried steps
            if result is not None:  # Checks if the key was found
                private_key_integer = result  # Stores the found private key
                break  # Exits the loop if the key was found

            print(f"[+] {start:x} - {min(start + max_steps, end_range):x}")

        # If the private key was found, prints the results
        if private_key_integer is not None:
            private_key_hex = format(private_key_integer, '064x')  # Converts the private key to hexadecimal
            print(f"\nPrivate key found: {private_key_hex}")
            print(f"WIF: {self.generate_wif(private_key_hex)}")
            print(f"Public address: {self.find_public_key(private_key_hex)}")
        else:
            print("\nPrivate key not found.")

        elapsed_time = time.time() - start_time  # Calculates the total execution time
        print(f"Total time: {elapsed_time:.2f} seconds")

        # Calculates and prints attempts per second
        if elapsed_time > 0:
            attempts_per_second = total_steps_tried / elapsed_time  # Calculates attempts per second
            print(f"Attempts per second: {attempts_per_second:.0f}")
        else:
            print("Execution time too short to calculate the rate.")
