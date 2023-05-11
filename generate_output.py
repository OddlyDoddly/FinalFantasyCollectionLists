import math
import json
from typing import List


def load_games():
    with open("in/gamelist.json", "rb") as f:
        return json.load(f)


def load_regions():
    with open("in/regions_alias.json", "rb") as f:
        return json.load(f)


def load_systems():
    with open("in/systems_alias.json", "rb") as f:
        return json.load(f)


def get_regions(alias, regions):
    game_regions = []
    for region, aliases in regions.items():
        if alias in aliases:
            game_regions.append(region)
    return game_regions


def get_systems(alias, systems):
    game_systems = []
    for system, aliases in systems.items():
        if alias in aliases:
            game_systems.append(system)
    return game_systems


def get_regions_by_system(game, game_regions, game_systems):
    regions_by_system = {}
    release_dates_by_system = {}
    for system in game_systems:
        regions_by_system[system] = []
        release_dates_by_system[system] = {}
        for region in game_regions:
            if region not in release_dates_by_system[system].keys():
                release_dates_by_system[system][region] = []
            regions_by_system[system].append(region)
            release_dates_by_system[system][region].append(game['release'])
    return regions_by_system, release_dates_by_system


def get_systems_by_region(game, game_systems, game_regions):
    systems_by_region = {}
    release_dates_by_region = {}

    for region in game_regions:
        systems_by_region[region] = []
        release_dates_by_region[region] = {}
        for system in game_systems:
            if system not in release_dates_by_region[region].keys():
                release_dates_by_region[region][system] = []
            systems_by_region[region].append(system)
            release_dates_by_region[region][system].append(game['release'])
    return systems_by_region, release_dates_by_region


def main(tag="", exculuded_systems=[]):
    games = load_games()
    regions = load_regions()
    systems = load_systems()

    list_by_region = {}
    list_by_system = {}
    list_by_title = {}
    list_by_system_region = {}

    for system in systems.keys():
        list_by_system[system] = []
        for region in regions.keys():
            list_by_region[region] = []
            list_by_system_region[system + "_" + region] = []

    for game in games:
        game_regions = get_regions(game['region'], regions)
        game_systems = get_systems(game['system'], systems)
        game['regions'] = game_regions
        game['systems'] = game_systems

        regions_by_system, releases_by_system = get_regions_by_system(game, game_regions, game_systems)
        systems_by_region, releases_by_region = get_systems_by_region(game, game_systems, game_regions)
        game['systems_by_region'] = systems_by_region
        game['releases_by_region'] = releases_by_region
        game['regions_by_system'] = regions_by_system
        game['releases_by_system'] = releases_by_system

        for system in game_systems:
            list_by_system[system].append(game)
            for region in game_regions:
                list_by_region[region].append(game)
                list_by_system_region[system + "_" + region].append(game)

        if game['name'] in list_by_title.keys():
            for system in regions_by_system.keys():
                if system in list_by_title[game['name']]['regions_by_system'].keys():
                    list_by_title[game['name']]['regions_by_system'][system] = list(set(
                        list_by_title[game['name']]['regions_by_system'][system] + regions_by_system[system]))
                else:
                    list_by_title[game['name']]['regions_by_system'][system] = regions_by_system[system]

            for region in systems_by_region.keys():
                if region in list_by_title[game['name']]['systems_by_region'].keys():
                    list_by_title[game['name']]['systems_by_region'][region] = list(set(
                        list_by_title[game['name']]['systems_by_region'][region] + systems_by_region[region]))
                else:
                    list_by_title[game['name']]['systems_by_region'][region] = systems_by_region[region]

            for region in releases_by_region.keys():
                if region in list_by_title[game['name']]['releases_by_region'].keys():
                    for system in releases_by_region[region]:
                        if system in list_by_title[game['name']]['releases_by_region'][region].keys():
                            list_by_title[game['name']]['releases_by_region'][region][system] = \
                                list(set(list_by_title[game['name']]['releases_by_region'][region][system] + releases_by_region[region][system]))
                        else:
                            list_by_title[game['name']]['releases_by_region'][region][system] = releases_by_region[region][system]
                else:
                    list_by_title[game['name']]['releases_by_region'][region] = releases_by_region[region]

            for system in releases_by_system.keys():
                if system in list_by_title[game['name']]['releases_by_system'].keys():
                    for region in releases_by_system[system].keys():
                        if region in list_by_title[game['name']]['releases_by_system'][system].keys():
                            list_by_title[game['name']]['releases_by_system'][system][region] = list(set(
                                list_by_title[game['name']]['releases_by_system'][system][region] + releases_by_system[system][region]
                            ))
                        else:
                            list_by_title[game['name']]['releases_by_system'][system][region] = releases_by_system[system][region]
                else:
                    list_by_title[game['name']]['releases_by_system'][system] = releases_by_system[system]

            list_by_title[game['name']]['name'] = game['name']
            list_by_title[game['name']]['systems'] = list(set(list_by_title[game['name']]['systems'] + game_systems))
            list_by_title[game['name']]['regions'] = list(set(list_by_title[game['name']]['regions'] + game_regions))
            list_by_title[game['name']]['earliest_release'] = list(set(list_by_title[game['name']]['regions'] + game_regions))

        else:
            list_by_title[game['name']] = {
                'name': game['name'],
                'systems': game_systems,
                'regions': game_regions,
                'regions_by_system': regions_by_system,
                'systems_by_region': systems_by_region,
                'releases_by_region': releases_by_region,
                'releases_by_system': releases_by_system
            }
    with open(f"./out/json/games_by_system_{tag}.json", "w") as f:
        f.write(json.dumps(list_by_system, indent=4))
        print("File saved to ./out/json/games_by_system_{tag}.json")
    with open(f"./out/json/games_by_region_{tag}.json", "w") as f:
        f.write(json.dumps(list_by_region, indent=4))
        print("File saved to ./out/json/games_by_region_{tag}.json")
    with open(f"./out/json/games_by_system_and_region_{tag}.json", "w") as f:
        f.write(json.dumps(list_by_system_region, indent=4))
        print("File saved to ./out/json/games_by_system_and_region_{tag}.json")
    with open(f"./out/json/games_by_title_{tag}.json", "w") as f:
        f.write(json.dumps(list_by_title, indent=4))
        print("File saved to ./out/json/games_by_title_{tag}.json")

    text = ""
    for system in systems:
        if system in exculuded_systems:
            continue
        text += "===== " + system + " =====\n"
        for title, game in list_by_title.items():
            if system in game['systems']:
                system_regions = ''
                for region in game['regions_by_system'][system]:
                    release = game['releases_by_region'][region][system]
                    system_regions += f"\t\t{region} - {release}\n"
                text += f"\t- {game['name']}\n{system_regions}\n"
        text += "\n"
    with open(f"./out/txt/games_by_system_{tag}.txt", encoding='utf-16', mode="w") as f:
        f.write(text)
        print(f"File saved to ./out/txt/games_by_system_{tag}.txt")

    text = ""
    for region in regions:
        text += "===== " + region + " =====\n"
        for title, game in list_by_title.items():
            if region in game['regions']:
                region_systems = ''
                for system in game['systems_by_region'][region]:
                    if system in exculuded_systems:
                        continue
                    release = game['releases_by_system'][system][region]
                    region_systems += f"\t\t{system} - {release}\n"
                text += f"\t-{game['name']}\n{region_systems}\n"
        text += "\n"
    with open(f"./out/txt/games_by_region_{tag}.txt", encoding='utf-16', mode="w") as f:
        f.write(text)
        print(f"File saved to ./out/txt/games_by_region_{tag}.txt")

    text = ""
    for title, game in list_by_title.items():
        text += f"===== {title} =====\n"
        for system, regions in game['releases_by_system'].items():
            if system in exculuded_systems:
                continue
            text += f"\t{system}\n"
            for region, releases in regions.items():
                text += f"\t\t{region} - {releases}\n"
        text += "\n"
    with open(f"./out/txt/games_by_title_{tag}.txt", encoding='utf-16', mode="w") as f:
        f.write(text)
        print(f"File saved to ./out/txt/games_by_title_{tag}.txt")

    titles = {
        "Final Fantasy I": [],
        "Final Fantasy II": [],
        "Final Fantasy III": [],
        "Final Fantasy IV": [],
        "Final Fantasy V": [],
        "Final Fantasy VI": [],
        "Final Fantasy VII": [],
        "Final Fantasy VIII": [],
        "Final Fantasy IX": [],
        "Final Fantasy X": [],
        "Final Fantasy XI": [],
        "Final Fantasy XII": [],
        "Final Fantasy XIII": [],
        "Final Fantasy XIV": [],
        "Final Fantasy XV": [],
        "Final Fantasy XVI": [],
        "Final Fantasy XIII-2": [],
        "Final Fantasy X-2": [],
    }

    for title, game in list_by_title.items():
        if '[' in title:
            game_index_str = title[title.find('[')+1:title.find(']')]

            if not game_index_str.isdigit():
                indexes = []
                by_commas = game_index_str.split(', ')
                for s in by_commas:
                    if '&' in s:
                        indexes = indexes + s.split(' & ')
                    elif s is not None:
                        indexes.append(s)
                for index in indexes:
                    if index == '10-2':
                        new_title = "Final Fantasy X-2"
                    elif index == '13-2':
                        new_title = "Final Fantasy XIII-2"
                    else:
                        new_title = list(titles.keys())[int(index) - 1]
                    titles[new_title].append(game)
            else:
                game_index = int(game_index_str)
                new_title = list(titles.keys())[game_index-1]
                titles[new_title].append(game)

    text = ""
    for title, game_list in titles.items():
        text += f"===== {title} =====\n"
        for game in game_list:
            text += f"\t{game['name']}\n"
            for system, regions in game['releases_by_system'].items():
                if system in exculuded_systems:
                    continue
                text += f"\t\t{system}\n"
                for region, releases in regions.items():
                    text += f"\t\t\t{region} - {releases}\n"
        text += "\n"

    with open(f"./out/txt/games_by_index_{tag}.txt", encoding='utf-16', mode="w") as f:
        f.write(text)
        print(f"File saved to ./out/txt/games_by_index_{tag}.txt")

    with open(f"./out/json/games_by_index_{tag}.json", encoding='utf-16', mode="w") as f:
        f.write(json.dumps(titles, indent=4))
        print(f"File saved to ./out/json/games_by_index_{tag}.json")


if __name__ == '__main__':
    digital_platforms = [
        "ARCADE",
        "OTHER",
        "VIDEO",
        "WINDOWS-PHONE",
        "ANDROID",
        "IOS",
        "MOBILE-OTHER",
        "XBONE-DIGITAL",
        "XB360-ARCADE",
        "PS5-PSN",
        "PS4-PSN",
        "PS3-PSN",
        "PSN",
        "PSP-PSN",
        "N3DS-ESHOP",
        "SWITCH-ESHOP",
        "WIIU-ESHOP",
        "WII-ESHOP",
        "NINTENDO-ESHOP",
        "NES-CLASSIC"
    ]

    non_digital_platforms = [
        "NES",
        "NES-CLASSIC",
        "SNES",
        "GC",
        "WII",
        "WIIU",
        "SWITCH",
        "GB",
        "GBC",
        "GBA",
        "NDS",
        "N3DS",
        "PSP",
        "PSVITA",
        "PS1",
        "PS2",
        "PS3",
        "PS4",
        "PS5",
        "XBOX",
        "XB360",
        "XBONE",
        "XBSX",
        "WS",
        "MOBILE-OTHER",
        "VIDEO",
        "OTHER",
        "ARCADE"
    ]

    main("COMPLETE", [])