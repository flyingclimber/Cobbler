#!/usr/bin/env python

import ips
import csv
import json

CSV = 'Nekketsu.csv'
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
        with open(self.csv, 'rb') as g:
            reader = csv.DictReader(g)

            for row in reader:
                if row['Start']:
                    update = Update(row['Start'], row['End'], row['Edited'])
                    print update
                    print update.convert_to_tile()


class Update:
    def __init__(self, start, end, data):
        self.start = start
        self.end = end
        self.data = data

    def __str__(self):
        return '{}-{} {}'.format(self.start, self.end, self.data)

    def convert_to_tile(self):
        tile_layout = TileLayout('DMG-NDJ')
        rom_layout = RomLayout('DMG-NDJ')
        tile_set = rom_layout.get_tile_set('DMG-NDJ', self.start)
        res = bytearray()

        for char in self.data:
            res.append(tile_layout.get_hex(char, tile_set))

        return res


class Rom:
    def __init__(self, serial):
        self.serial = serial
        self.rom_layout = RomLayout(serial)
        self.tile_layout = TileLayout(serial)


class RomLayout:
    def __init__(self, serial):
        with open(DATA_DIR + "/" + ROM_LAYOUT_JSON, 'r') as g:
            self.mapping = json.load(g)

    def get_tile_set(self, serial, address):
        for rom_range in self.mapping[serial]:
            if int(self.mapping[serial][rom_range]['start'], 16) <= int(address, 16) <= int(self.mapping[serial][rom_range]['end'], 16):
                return self.mapping[serial][rom_range]['tile_set']


class TileLayout:
    def __init__(self, serial):
        self.serial = serial

        with open(DATA_DIR + "/" + TILE_LAYOUT_JSON, 'r') as g:
            self.mapping = json.load(g)

    def get_hex(self, char, tile_set):
        return self.mapping[self.serial][tile_set][char.upper()]


def main():
    cobbler = Cobbler(CSV)
    cobbler.parse_csv()

if __name__ == "__main__":
    main()
