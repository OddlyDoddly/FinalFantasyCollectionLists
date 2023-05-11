import json


def main():
    with open("in/gamelist.json", "rb") as f:
        game_list = json.load(f)
        region_list = []
        for game in game_list:
            if game['region'] not in region_list:
                region_list.append(game['region'])
        with open("in/regions.json", "w") as of:
            of.write(json.dumps(region_list, indent=4))
        print("Region List written to a file.")

    print("File saved to ./regions.json")


if __name__ == '__main__':
    main()

