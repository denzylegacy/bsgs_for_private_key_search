from src import KeyFinder


if __name__ == "__main__":
    target_public_key = "02f6a8148a62320e149cb15c544fe8a25ab483a0095d2280d03b8a00a7feada13d"
    target_address = "1PWCx5fovoEaoBowAvF5k91m2Xat9bMgwb"
    start_range_hex = "400000000"
    end_range_hex = "7ffffffff"

    key_finder = KeyFinder()

    total = 100_000_000

    # Calculate iterations and estimated time - #130
    total_iterations, estimated_time_seconds, estimated_time_formatted = (
        key_finder.calculate_iterations_and_time_with_bsgs(
            start_range_hex, end_range_hex, operations_per_second=total
        )
    )

    print(f"Total iterations to be mapped: {total_iterations:,}")
    print(f"Estimated time: {estimated_time_formatted}")

    # # Proceed with solving the puzzle
    # key_finder.find_private_key(
    #     start_range_hex, end_range_hex, target_address
    # )

    # Proceed with solving the puzzle
    # key_finder.solve_puzzle(
    #     target_public_key, target_address, start_range_hex, end_range_hex
    # )
