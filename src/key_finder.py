import bitcoin  # For conversions between private and public keys
import bitcoinlib  # For Bitcoin operations
from ecdsa import SECP256k1, numbertheory  # For elliptic curve operations
from ecdsa.ellipticcurve import Point  # To represent points on the curve
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
    def calculate_iterations_and_time(start_range_hex, end_range_hex, operations_per_second=1000000):
        """
        Calculates the total number of iterations required and estimates the time needed.

        Args:
        start_range_hex (str): The start of the range in hexadecimal.
        end_range_hex (str): The end of the range in hexadecimal.
        iterations_per_second (int): The number of iterations that can be processed per second.

        Returns:
        tuple: (total_iterations, estimated_time_seconds, estimated_time_formatted)
        """
        start_range = int(start_range_hex, 16)
        end_range = int(end_range_hex, 16)

        total_iterations = end_range - start_range + 1
        estimated_time_seconds = total_iterations / operations_per_second

        years, remainder = divmod(estimated_time_seconds, 31536000)
        days, remainder = divmod(remainder, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        time_parts = []
        if years > 0:
            time_parts.append(f"{years:,.0f} years")
        if days > 0:
            time_parts.append(f"{days:.0f} days")
        if hours > 0:
            time_parts.append(f"{hours:.0f} hours")
        if minutes > 0:
            time_parts.append(f"{minutes:.0f} minutes")
        if seconds > 0 or not time_parts:
            time_parts.append(f"{seconds:.2f} seconds")

        estimated_time_formatted = ", ".join(time_parts)

        return total_iterations, estimated_time_seconds, estimated_time_formatted

    @staticmethod
    def calculate_iterations_and_time_with_bsgs(start_range_hex, end_range_hex, operations_per_second):
        """
            Calculates the total number of operations required for the Baby-step Giant-step (BSGS) algorithm
            and estimates the time needed to complete the search.

            This method uses the BSGS algorithm to estimate the computational effort required to search
            through a given range of private keys. It calculates the number of operations based on the
            square root of the interval size, which is characteristic of the BSGS algorithm's efficiency.

            Args:
            start_range_hex (str): The start of the private key range in hexadecimal.
            end_range_hex (str): The end of the private key range in hexadecimal.
            operations_per_second (int): The estimated number of operations that can be processed per second.
                                         Defaults to 1,000,000 operations per second.

            Returns:
            tuple: A tuple containing three elements:
                   - interval_size (int): The total number of possible keys in the given range.
                   - estimated_time_seconds (float): The estimated time in seconds to complete the search.
                   - estimated_time_formatted (str): A human-readable string representing the estimated time,
                                                     formatted with appropriate units (years, days, hours, minutes, seconds).

            Note:
            - The actual time may vary depending on hardware capabilities and implementation efficiency.
            - The BSGS algorithm provides a significant speedup compared to brute force methods,
              with a time complexity of O(sqrt(n)) instead of O(n).
            """
        start_range = int(start_range_hex, 16)
        end_range = int(end_range_hex, 16)

        interval_size = end_range - start_range + 1

        max_steps = 2 ** int(math.log2(math.sqrt(interval_size)))

        total_operations = 2 * max_steps

        estimated_time_seconds = total_operations / operations_per_second

        years, remainder = divmod(estimated_time_seconds, 31536000)
        days, remainder = divmod(remainder, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        time_parts = []
        if years > 0:
            time_parts.append(f"{years:,.0f} years")
        if days > 0:
            time_parts.append(f"{days:.0f} days")
        if hours > 0:
            time_parts.append(f"{hours:.0f} hours")
        if minutes > 0:
            time_parts.append(f"{minutes:.0f} minutes")
        if seconds > 0 or not time_parts:
            time_parts.append(f"{seconds:.2f} seconds")

        estimated_time_formatted = ", ".join(time_parts)

        return interval_size, estimated_time_seconds, estimated_time_formatted

    @staticmethod
    def find_private_key(min_range_hex, max_range_hex, target_address):
        """Searches for the private key that corresponds to the target address."""
        start_time = time.time()
        keys_checked = 0

        min_range = int(min_range_hex, 16)
        max_range = int(max_range_hex, 16)

        for private_key in range(min_range, max_range):
            private_key_hex = format(private_key, '064x')  # Converte a chave privada para hexadecimal
            public_address = KeyFinder.find_public_key(private_key_hex)

            keys_checked += 1

            if keys_checked % 1000 == 0:
                elapsed_time = time.time() - start_time
                print(f"Keys checked: {keys_checked}, Elapsed time: {elapsed_time:.2f} seconds")

            # Verifica se o endereço público gerado corresponde ao endereço alvo
            if public_address == target_address:
                return private_key_hex  # Retorna a chave privada encontrada

        return None

    @staticmethod
    def find_public_key(private_key):
        """Finds the public key corresponding to a given private key."""
        private_key_decimal = int(private_key, 16)  # Converts the private key from hexadecimal to decimal
        public_key = bitcoin.privkey_to_pubkey(private_key_decimal)  # Generates the public key
        return public_key

    @staticmethod
    def generate_wif(private_key):
        """Converts a private key to Wallet Import Format (WIF)."""
        key = bitcoinlib.keys.Key(private_key)
        return key.wif()

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
        giant_step = self.G * max_steps  # Calculates the giant step
        steps_tried = 0  # Counter for tried steps

        # Baby-step
        current = self.G * start
        for i in range(max_steps):
            baby_steps[(current.x(), current.y())] = i
            current = current + self.G  # Baby step
            steps_tried += 1

        # Giant-step
        current = target_point
        for j in range(max_steps):
            current_key = (current.x(), current.y())
            if current_key in baby_steps:
                return start + j * max_steps + baby_steps[current_key], steps_tried
            current = current + (-giant_step)  # Giant step (moving backwards)
            steps_tried += 1

        return None, steps_tried

    def solve_puzzle(self, target_public_key, target_address, start_range_hex, end_range_hex):
        """Main method to solve the puzzle and find the private key."""
        start_range = int(start_range_hex, 16)  # Converts the start range from hexadecimal to decimal
        end_range = int(end_range_hex, 16)  # Converts the end range from hexadecimal to decimal

        interval_size = end_range - start_range + 1
        max_steps = 2 ** int(math.log2(math.sqrt(interval_size)))

        target_public_key_point = self.calculate_public_key_point(target_public_key)

        print("target_public_key_point", target_public_key_point)

        start_time = time.time()
        total_steps_tried = 0
        private_key_integer = None

        # Iterates over the range of private keys
        for start in range(start_range, end_range, max_steps):
            key, steps = self.bsgs(target_public_key_point, max_steps, start)
            total_steps_tried += steps
            if key is not None:
                private_key_integer = key
                break

            print(f"[+] {start:x} - {min(start + max_steps, end_range):x}")

        if private_key_integer is not None:
            private_key_hex = format(private_key_integer, '064x')  # Converts the private key to hexadecimal
            print(f"\nPrivate key found: {private_key_hex}")
            print(f"WIF: {self.generate_wif(private_key_hex)}")
            print(f"Public address: {self.find_public_key(private_key_hex)}")
        else:
            print("\nPrivate key not found.")

        elapsed_time = time.time() - start_time
        print(f"Total time: {elapsed_time:.2f} seconds")

        if elapsed_time > 0:
            attempts_per_second = total_steps_tried / elapsed_time
            print(f"Attempts per second: {attempts_per_second:.0f}")
        else:
            print("Execution time too short to calculate the rate.")
