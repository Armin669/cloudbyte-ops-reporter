#!/usr/bin/env python3
"""CloudByte Ops Reporter: summarise CloudByte's activity from the command line."""


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

    # Count events per user
    user_counts = {}
    for line in records:
        timestamp, user, action = line.split()
        user_counts[user] = user_counts.get(user, 0) + 1


        # Rank users by event count (highest first)
    user_pairs = []
    for name, count in user_counts.items():
        user_pairs.append((count, name))
    user_pairs.sort(reverse=True)

    print("Most active users")
    for rank, (count, name) in enumerate(user_pairs, start=1):
        print(f"  {rank}. {name}: {count} events")

if __name__ == "__main__":
    main()