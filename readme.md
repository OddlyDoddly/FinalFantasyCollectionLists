# Final Fantasy Collection Lists

This repository is a list of final fantasy games, regions, consoles, and release dates.

The data was originally scraped from [https://thefinalfantasy.net/games/complete-list.html](https://thefinalfantasy.net/games/complete-list.html)
But from here on, the lists should be manually updated by updating the data in the `./in` folder with new records, and regenerating the lists using the python scripts.

As of right now, I'm too lazy to write instructions on generating the list. The code is pretty procedural... I'm writing this readme to document the output data...

## Output Data
Inside the `./out` folder you will find a series of txt and json files.

### The Collections:
- **COMPLETE** is the complete list of final fantasy games
- **PHYSICAL** is the complete list of final fantasy games without any digital download listings
- **DIGITAL** is the complete list of final fantasy games without any physical copy listings

### The Files
Each collection has 4 different major lists:
- **game_by_region_(COLLECTION)** - List of Final Fantasy Titles Organized by Region.
- **game_by_system_(COLLECTION)** - List of Final Fantasy Titles Organized by the Console they were released on.
- **game_by_title_(COLLECTION)** - List of Final Fantasy Titles Organized by Game Title
- **game_by_index_(COLLECTION)** - List of MAIN STORY Final Fantasy Games in Chronological Order
