from src import KeyFinder


if __name__ == "__main__":
    target_public_key = "033c4a45cbd643ff97d77f41ea37e843648d50fd894b864b0d52febc62f6454f7c"
    target_address = "1HsMJxNiV7TLxmoF6uJNkydxPFDog4NQum"
    start_range_hex = "80000"
    end_range_hex = "fffff"

    KeyFinder().solve_puzzle(
        target_public_key, target_address, start_range_hex, end_range_hex
    )
