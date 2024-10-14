import random
import time
from itertools import combinations
import pandas as pd
import matplotlib.pyplot as plt

def knapsack_combinations(items, capacity):
    max_value = 0
    best_combination = []
    for i in range(1, len(items) + 1):
        for combination in combinations(items, i):
            total_weight = sum(x[0] for x in combination)
            total_value = sum(x[1] for x in combination)
            if total_weight <= capacity and total_value > max_value:
                max_value = total_value
                best_combination = combination
    return max_value, best_combination

def knapsack_heuristic(items, capacity, heuristic=0):
    if heuristic == 0:
        # Value per weight ratio
        items = sorted(items, key=lambda x: x[1] / x[0], reverse=True)  
    elif heuristic == 1:
        # Lesser weight
        items = sorted(items, key=lambda x: x[0])  
    else:
        # Higher value
        items = sorted(items, key=lambda x: x[1], reverse=True)  
    
    total_value = 0
    total_weight = 0
    best_combination = []
    for weight, value in items:
        if total_weight + weight <= capacity:
            best_combination.append((weight, value))
            total_value += value
            total_weight += weight

    return total_value, best_combination

def generate_knapsack_example(num_items, max_weight, max_value):
    """Generate a random knapsack problem instance."""
    items = [(random.randint(1, max_weight), random.randint(1, max_value)) for _ in range(num_items)]
    capacity = random.randint(max_weight // 2, max_weight)
    return items, capacity

def main():
    results = []
    max_weight = 20
    max_value = 100
    for n in range(5, 50, 5):
        items, capacity = generate_knapsack_example(n, max_weight, max_value)

        row = {"n": n, "capacity": capacity}

        # Combinatory Approach
        if n <= 25:  # Limit due to combinatorial explosion
            time_start = time.perf_counter_ns()
            max_value_c, best_combination_c = knapsack_combinations(items, capacity)
            time_end = time.perf_counter_ns()
            row["comb_value"] = max_value_c
            row["comb_items"] = len(best_combination_c)
            row["comb_time"] = time_end - time_start
        else:
            row["comb_value"] = None
            row["comb_items"] = None
            row["comb_time"] = None

        # Heuristic Approaches
        heuristics = ["value_per_weight", "lesser_weight", "higher_value"]
        for i, heuristic_name in enumerate(heuristics):
            time_start = time.perf_counter_ns()
            max_value_h, best_combination_h = knapsack_heuristic(items, capacity, i)
            time_end = time.perf_counter_ns()
            row[f"{heuristic_name}_value"] = max_value_h
            row[f"{heuristic_name}_items"] = len(best_combination_h)
            row[f"{heuristic_name}_time"] = time_end - time_start

        results.append(row)

    df = pd.DataFrame(results)
    print(df)

    plt.figure(figsize=(10, 6))
    plt.plot(df['n'], df['comb_time'], label='Combinatory', marker='o', linestyle='--', color='r')
    plt.plot(df['n'], df['value_per_weight_time'], label='Heuristic: Value/Weight', marker='o', linestyle='-', color='g')
    plt.plot(df['n'], df['lesser_weight_time'], label='Heuristic: Lesser Weight', marker='o', linestyle='-', color='b')
    plt.plot(df['n'], df['higher_value_time'], label='Heuristic: Higher Value', marker='o', linestyle='-', color='m')

    plt.title('Execution Time vs Number of Items')
    plt.xlabel('Number of Items (n)')
    plt.ylabel('Execution Time (nanoseconds)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    df = df.to_csv("results.csv", encoding='utf-8')
    

if __name__ == "__main__":
    main()
