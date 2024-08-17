# Baby-step Giant-step for private key search (Python Demo)

The `KeyFinder` class is a Python implementation designed to find the private key corresponding to a Bitcoin public address using the Baby-step Giant-step algorithm. **This tool is primarily for educational purposes and should be used responsibly**.

## Features

- **Generate Public Address**: Create a Bitcoin public address from a private key.
- **Wallet Import Format (WIF)**: Convert a private key to its WIF representation.
- **Private Key Search**: Efficiently search for a private key within a specified range that corresponds to a given Bitcoin public address.
- **Public Key Calculation**: Calculate the public key from a private key.
- **Elliptic Curve Operations**: Perform calculations on the elliptic curve used in Bitcoin (SECP256k1).

## Installation

To use the code in this repository, ensure you have the required libraries installed. You can install them using pip:

```bash
pip install -r requirements.txt
```

## Usage

Here’s an example of how to use the code within the `KeyFinder` class:

```python
from src import KeyFinder

# Define the target public key, target address, and the search range
target_public_key = "033c4a45cbd643ff97d77f41ea37e843648d50fd894b864b0d52febc62f6454f7c"
target_address = "1HsMJxNiV7TLxmoF6uJNkydxPFDog4NQum"
start_range_hex = "80000"
end_range_hex = "fffff"

# Solve the puzzle to find the private key
KeyFinder().solve_puzzle(
    target_public_key, target_address, start_range_hex, end_range_hex
)
```

## Methods

### `generate_public(private_key)`
Generates a public address from a private key.

### `generate_wif(private_key)`
Converts a private key to Wallet Import Format (WIF).

### `find_private_key(min_range, max_range, target_address)`
Searches for the private key that corresponds to the target address.

### `find_public_key(private_key)`
Finds the public key corresponding to a given private key.

### `calculate_public_key_point(target_public_key)`
Calculates the (x, y) point of the public key on the elliptic curve.

### `bsgs(target_point, max_steps, start)`
Implements the Baby-step Giant-step algorithm to find the private key.

### `solve_puzzle(target_public_key, target_address, start_range_hex, end_range_hex)`
Main method to solve the puzzle and find the private key.

## Important Notes

- **Ethical Use**: This tool is intended for educational purposes only. Do not use it to attempt to access wallets or private keys that do not belong to you.
- **Performance**: The search for private keys can be computationally intensive and may take a significant amount of time depending on the specified range.
- **Dependencies**: Ensure that the required libraries are installed and compatible with your Python version.

## Acknowledgments

- Bitcoin and its underlying technology.