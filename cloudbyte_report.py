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
        print(f"{ts}  {user} {action}")


if __name__ == "__main__":
    main()