import argparse

from mtgdb import card 
from mtgdb import database
from mtgdb import lookup

def parse_args():
    parser = argparse.ArgumentParser(prog="mtgdb")
    parser.add_argument("-f", "--foil", action="store_true")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--add", "-a", nargs=3, metavar=("SET", "NUM", "COUNT"))
    group.add_argument("--remove", "-r", nargs=3, metavar=("SET", "NUM", "COUNT"))
    group.add_argument("--update", "-u", nargs=2, metavar=("SET", "NUM"))
    group.add_argument("--search", "-s", nargs=2, metavar=("SET", "NUM"))
    args = parser.parse_args()
    assert 1 == sum(arg != None for arg in (args.add, args.remove, args.update, args.search))
    return args

def add(db, set_code, collector_number, foil, count):
    card = lookup.lookup(set_code, collector_number, foil)
    result = db.add(card, count)
    print(f"Added {count} {card}")
    print(result)

def remove(db, set_code, collector_number, foil, count):
    card = lookup.lookup(set_code, collector_number, foil)
    result = db.remove(card, count)
    print(f"Removed {count} {card}")
    print(result)

def update(db, set_code, collector_number, foil):
    card = lookup.lookup(set_code, collector_number, foil)
    result = db.add(card)
    print(result)

def search(db, set_code, collector_number, foil):
    card = lookup.lookup(set_code, collector_number, foil)
    result = db.search(card)
    print(result)

def main():
    args = parse_args()

    db = database.Database("mtgdb.db")

    if args.add != None:
        add(db, args.add[0], args.add[1], args.foil, args.add[2])
    elif args.remove != None:
        remove(db, args.remove[0], args.remove[1], args.foil, args.remove[2])
    elif args.update != None:
        update(db, args.update[0], args.update[1], args.foil)
    elif args.search != None:
        search(db, args.update[0], args.update[1], args.foil)
    else:
        # Should never happen. parse_args should require at least one
        print("No operation selected")
        assert any(arg != None for arg in (args.add, args.remove, args.update, args.search))
