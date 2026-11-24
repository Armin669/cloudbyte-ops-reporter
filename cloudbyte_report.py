#!/usr/bin/env python3
"""CloudByte Ops Reporter: summarise CloudByte's activity from the command line."""

def get_user(record):
    return record.split()[1]

def get_hour(record):
    return record.split()[0][11:13]

def by_count_then_name(pair):
    """Sort key: busiest first, ties broken A-to-Z by name."""
    count, name = pair
    return (-count, name)

def count_and_rank(records, get_key):
    counts = {}
    for record in records:
        key = get_key(record)
        counts[key] = counts.get(key, 0) + 1

    pairs = []
    for key, count in counts.items():
        pairs.append((count, key))
    pairs.sort(key=by_count_then_name)
    return pairs

def get_action(record):
    return record.split()[2]

def main():
    with open("cloudbyte_access.log") as f:
        records = f.readlines()

    first = records[0].split()[0].replace("T", " ")
    last = records[-1].split()[0].replace("T", " ")

    print("CloudByte Access Report")
    print(f"{len(records)} events from {first} to {last}")

    print()   # blank line

    for line in records:
        parts = line.split()
        ts = parts[0].replace("T", " ")
        user = parts[1]
        action = parts[2]
        print(f"{ts}  {user}  {action}")

    print()  # blank line

    user_pairs = count_and_rank(records, get_user)

    print("Most active users")
    for rank, (count, name) in enumerate(user_pairs, start=1):
        print(f"  {rank}. {name}: {count} events")

    print()
    print()
    print("Activity by type")
    action_pairs = count_and_rank(records, get_action)
    for rank, (count, action) in enumerate(action_pairs, start=1):
        print(f"  {rank}. {action}: {count} events")

    print("Busiest hours")
    hour_pairs = count_and_rank(records, get_hour)
    for count, hour in hour_pairs:
        print(f"  {hour}:00  {count} events")

if __name__ == "__main__":
    main()