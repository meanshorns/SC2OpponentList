#!/usr/bin/env python3
"A searchable database of Starcraft players"
import json, os

# Globals
DBFILE = os.path.join(os.environ['APPDATA'], "starcraftplayers.json")


def printHelp():
    "print a help message"
    print(
"""To add a player, type \"add playername\" and you will be prompted for a description.
To delete player, type \"del playername\"
To search for a player, type their name and hit enter.
To quit, type \"quit\", \"exit\", \"bye\", or send EOF.""")

class JsonDB():
    "The database that reads and writes out the json file."
    def __init__(self):
        "self._db is a dict of playername: description. playernames are all stripped and lowered"
        try:
            self._db = json.loads(open(DBFILE).read())
        except FileNotFoundError:
            print("No existing database found, starting fresh.")
            self._db = {}
    def add(self, playername, description):
        "add a new entry"
        self._db[playername.strip().lower()] = description.strip()
    def delete(self, playername):
        "delete an entry. raise KeyError if not found."
        del self._db[playername.strip().lower()]
    def search(self, playername):
        "search the database for playername and return a list of tuples: [(playername, description), ...]. an empty list is returned if there are no matches, a KeyError will not be raised."
        playername = playername.strip().lower()
        results = []
        for key in self._db:
            if playername in key:
                results.append((key, self._db[key]))
        return results
    def save(self):
        "Save the database"
        open(DBFILE, 'w').write(json.dumps(self._db))

if __name__ == "__main__":
    database = JsonDB()
    try:
        while True:
            try: # unset arg so it can be detected
                del arg
            except NameError:
                pass
            try:
                userinput = input("> ")
            except EOFError: # quit
                break
            try: # make sure line isn't blank
                cmd = userinput.split()[0].lower()
            except IndexError:
                printHelp()
                continue
            try: # try to get an arg for commands that require it
                arg = userinput.split()[1]
            except IndexError:
                pass
            if cmd == 'add': # parse args
                try:
                    description = input("Enter description for {}: ".format(arg))
                except NameError: # arg wasn't set because it is not present, this add command was invalid
                    printHelp()
                    continue
                if not description:
                    print("No description entered, not adding {}.".format(arg))
                else:
                    database.add(arg, description)
                    print("Added {}!".format(arg))
            elif cmd in ('del', 'delete'):
                try:
                    database.delete(arg)
                except NameError: # arg wasn't set
                    printHelp()
                    continue
                except KeyError:
                    print("Player not found in database:", arg)
                else:
                    print("Deleted", arg)
            elif cmd in ('help', '?'):
                printHelp()
            elif cmd in ('exit', 'quit', 'bye'):
                break
            else: # do a db search
                results = database.search(cmd)
                if not results:
                    print("0 results found.")
                    continue
                for r in results:
                    print("{}: {}".format(r[0], r[1]))
    finally:
        database.save()
