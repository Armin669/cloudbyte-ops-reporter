#!/usr/bin/env python3
"""CloudByte Ops Reporter: summarise CloudByte's activity from the command line."""
import csv

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

    pairs = [(count, key) for key, count in counts.items()]
    pairs.sort(key=by_count_then_name)
    return pairs

def get_action(record):
    return record.split()[2]

def main():
    with open("cloudbyte_access.log") as f:
        records = [line for line in f]

    first = records[0].split()[0].replace("T", " ")
    last = records[-1].split()[0].replace("T", " ")

    print("CloudByte Access Report")
    print(f"{len(records)} events from {first} to {last}")

    # Read the staff roster into a {username: department} lookup.
    with open("users.csv") as f:
        dept_of = {row["username"]: row["department"] for row in csv.DictReader(f)}

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

    print()
    print("Most active logins")
    login_records = [record for record in records if get_action(record) == "login"]
    for rank, (count, user) in enumerate(count_and_rank(login_records, get_user), 1):
        print(f"  {rank}. {user}: {count} events")

    print()
    person = "alice"
    print(f"Activity for {person}")
    person_records = [record for record in records if get_user(record) == person]
    for rank, (count, action) in enumerate(count_and_rank(person_records, get_action), 1):
        print(f"  {rank}. {action}: {count} events")

    # Activity by department
    print("Activity by department")
    dept_counts = {}
    for record in records:
        user = get_user(record)
        dept = dept_of[user]
        dept_counts[dept] = dept_counts.get(dept, 0) + 1
    for i, (dept, count) in enumerate(sorted(dept_counts.items(), key=lambda x: (-x[1], x[0])), 1):
        print(f"  {i}. {dept}: {count} events")          

    print("Busiest hours")
    hour_pairs = count_and_rank(records, get_hour)
    for count, hour in hour_pairs:
        print(f"  {hour}:00  {count} events")

if __name__ == "__main__":
    main()