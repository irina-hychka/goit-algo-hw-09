import timeit

def find_coins_greedy(amount, coins):
    """
    Implements a greedy algorithm to make change using the largest possible coins first.

    Args:
        amount (int): The total amount of change to be given.
        coins (List[int]): List of available coin denominations.

    Returns:
        dict: A dictionary where keys are coin denominations and values are their counts.
    """
    result = {}

    for coin in coins:
        if amount <= 0:
            break  # Exit early if change is fully given

        count = amount // coin  # Max number of this coin that fits in remaining amount
        if count > 0:
            result[coin] = count
            amount -= coin * count  # Reduce remaining amount accordingly

    return result


def find_min_coins(amount, coins):
    """
    Uses dynamic programming to find the optimal (minimum number of coins) way to make change.

    Args:
        amount (int): The total amount of change to be given.
        coins (List[int]): List of available coin denominations.

    Returns:
        dict: A dictionary with coin denominations as keys and the count of each used coin as values.
              Returns an empty dictionary if change cannot be made.
    """

    # Initialize table to track the minimum number of coins needed for each amount
    min_coins = [float('inf')] * (amount + 1)
    coin_used = [0] * (amount + 1)  # Tracks which coin was last used for each amount

    min_coins[0] = 0  # Base case: 0 coins needed to make amount 0

    # Build up the solution for all values from 1 to amount
    for s in range(1, amount + 1):
        for coin in coins:
            if s >= coin and min_coins[s - coin] + 1 < min_coins[s]:
                min_coins[s] = min_coins[s - coin] + 1
                coin_used[s] = coin  # Record the coin used to build this amount

    if min_coins[amount] == float('inf'):
        return {}  # No solution found

    # Reconstruct the coin set used to make the amount
    result = {}
    current_amount = amount
    while current_amount > 0:
        coin = coin_used[current_amount]
        result[coin] = result.get(coin, 0) + 1
        current_amount -= coin

    return result

def compare_algorithms(amount, coins_desc, coins_asc):
    # Run greedy algorithm and measure time
    greedy_time = timeit.timeit(
        lambda: find_coins_greedy(amount, coins_desc),
        number=1000
    )
    greedy_result = find_coins_greedy(amount, coins_desc)

    # Run dynamic programming algorithm and measure time
    dp_time = timeit.timeit(
        lambda: find_min_coins(amount, coins_asc),
        number=1000
    )
    dp_result = find_min_coins(amount, coins_asc)

    # Convert seconds to microseconds
    greedy_time_us = greedy_time / 1000 * 1_000_000
    dp_time_us = dp_time / 1000 * 1_000_000

    # Print results in nice format
    print(f"Amount: {amount}")
    print(f"Greedy algorithm result: {greedy_result}")
    print(f"Dynamic programming result: {dp_result}")
    print(f"Greedy time: {greedy_time_us:.3f} µs")
    print(f"DP time:     {dp_time_us:.3f} µs\n")

# Usage
if __name__ == "__main__":
    # For the Dynamic Programming algorithm
    coins_asc = [1, 2, 5, 10, 25, 50]
    # For the Greedy algorithm
    coins_desc = coins_asc[::-1]

    compare_algorithms(113, coins_desc, coins_asc)
    compare_algorithms(1234, coins_desc, coins_asc)
    compare_algorithms(10565, coins_desc, coins_asc)
    compare_algorithms(100000, coins_desc, coins_asc)
