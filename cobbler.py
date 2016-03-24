#!/usr/bin/env python

"""
    cobbler.py - Dedicated IPS patching worker
"""

import ips
import csv
import json

CSV_LIST = ['Nekketsu.csv']
DATA_DIR = 'data'
TILE_LAYOUT_JSON = 'tile_layout.json'
ROM_LAYOUT_JSON = 'rom_layout.json'


class Cobbler:
    """
        Someone to put it all together
    """
    def __init__(self, csv):
        self.csv = csv
        self.ips = ips.Ips()

    def parse_csv(self):
        """
            Given a csv create Updates and fetch tiles
        """
        with open(self.csv, 'rb') as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                if row['Start']:
                    update = Update(row['Start'], row['End'], row['Edited'])
                    print update
                    print update.convert_to_tile()

    def write_patch(self):
        """
            Write out the IPS patch file
        """
        self.ips.create_patch()


class Update:
    """
        Internal object to track patch attributes and tile table translations
    """
    def __init__(self, start, end, data):
        self.start = start
        self.end = end
        self.data = data

    def __str__(self):
        return '{}-{} {}'.format(self.start, self.end, self.data)

    def convert_to_tile(self):
        """
            Given an Update object translate char to tile values
        """
        tile_layout = TileLayout('DMG-NDJ')
        rom_layout = RomLayout('DMG-NDJ')
        tile_set = rom_layout.get_tile_set('DMG-NDJ', self.start)
        res = bytearray()

        for char in self.data:
            res.append(tile_layout.get_hex(char, tile_set))

        return res


class Rom:
    """
        Game we are patching
    """
    def __init__(self, serial):
        self.serial = serial
        self.rom_layout = RomLayout(serial)
        self.tile_layout = TileLayout(serial)


class RomLayout:
    """
        Layout table that maps rom address to a tile set
    """
    def __init__(self, serial):
        with open(DATA_DIR + "/" + ROM_LAYOUT_JSON, 'r') as layout_file:
            self.mapping = json.load(layout_file)

    def get_tile_set(self, serial, address):
        """
            Return the tile set that maps to the given address
        """
        for rom_range in self.mapping[serial]:
            if int(self.mapping[serial][rom_range]['start'], 16) <= \
                    int(address, 16) <= \
                    int(self.mapping[serial][rom_range]['end'], 16):
                return self.mapping[serial][rom_range]['tile_set']


class TileLayout:
    """
        Layout table that maps tiles to decimal values
    """
    def __init__(self, serial):
        self.serial = serial

        with open(DATA_DIR + "/" + TILE_LAYOUT_JSON, 'r') as layout_file:
            self.mapping = json.load(layout_file)

    def get_hex(self, char, tile_set):
        """
            Return the decimal tile mapping for a character using a tile
        """
        return self.mapping[self.serial][tile_set][char.upper()]


def main():
    """
        Main driver
    """
    for csv_file in CSV_LIST:
        cobbler = Cobbler(csv_file)
        cobbler.parse_csv()
        cobbler.write_patch()

if __name__ == "__main__":
    main()
