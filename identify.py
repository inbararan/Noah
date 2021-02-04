import csv
import paths

with open(paths.MASTER, "r") as file:
    records = list(csv.DictReader(file, fieldnames=["uuid", "team", "inner_id", "full_name"]))

# Global sets collecting uuid errors while the functions are called and reported at the end of the run (in main)
missing = set()
collisions = set()


def get_uuid(team, name):
    options = []
    for record in records:
        if team == record["team"] and name == record["full_name"].split()[0]:
            options.append(record["uuid"])
    if len(options) == 0:
        missing.add((team, name))
        return None
    elif len(options) > 1:
        collisions.add((team, name, options))
        return None
    return options[0]


def report_uuid_errors():
    def sort_key(tup):
        # Sort by team (tup[0]) and then by name (tup[1])
        # Not using unpacking because there may be 2 or three values in tup (2 in missing, 3 in collisions)
        return f"{tup[0]}{tup[1]}"
    for team, name in sorted(missing, key=sort_key):
        print(f"ERROR: Candidate not found: team {team} and name {name}")
    for team, name, options in sorted(collisions, key=sort_key):
        print(f"ERROR: UUID collision: team {team} and name {name}"
              f"\tUUIDs are: {options}")


def get_team(uuid: str) -> str:
    for record in records:
        if uuid == record["uuid"]:
            return record["team"]
    print(f"ERROR: No UUID {uuid}")
    return ""


def _get_full_name(uuid: str) -> str:
    for record in records:
        if uuid == record["uuid"]:
            return record["full_name"]
    print(f"ERROR: No UUID {uuid}")
    return ""


def get_private_name(uuid: str) -> str:
    return _get_full_name(uuid).split()[0] if uuid else uuid
