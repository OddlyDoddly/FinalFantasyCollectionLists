import json


def main():
    with open("in/gamelist.json", "rb") as f:
        game_list = json.load(f)
        systems_list = []
        for game in game_list:
            if game['system'] not in systems_list:
                systems_list.append(game['system'])
        with open("in/systems.json", "w") as of:
            of.write(json.dumps(systems_list, indent=4))
        print("System List written to a file.")

    print("File saved to ./gamelist.json")


if __name__ == '__main__':
    main()

