#!/usr/bin/env python

"""
    cobbler.py - Dedicated IPS patching worker
"""

import ips
import csv
import argparse
from rom import Rom, RomLayout, TileLayout

PARSER = argparse.ArgumentParser(description='IPS patch creator')
PARSER.add_argument('--serial', dest='serial', default='DMG-NDJ',
                    help='ROM serial')
PARSER.add_argument('--csv', dest='csv', nargs='+', default=['Nekketsu.csv'],
                    help='CSV input list')

ARGS = PARSER.parse_args()


class Cobbler:
    """
        Someone to put it all together
    """
    def __init__(self, csv_input, serial):
        self.input = csv_input
        self.serial = serial
        self.ips = ips.Ips()

    def parse_csv(self):
        """
            Given a csv create Updates and fetch tiles
        """
        with open(self.input, 'rb') as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                if row['Start']:
                    update = Update(row['Start'], row['End'], row['Edited'])
                    update.byte_data = update.convert_to_tile(self.serial)
                    hunk = ips.Hunk(update.start, update.end, update.byte_data)
                    self.ips.add_hunk(hunk)

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
        self.byte_data = bytearray()
        self.length = len(end) - len(start)

    def __str__(self):
        return '{}-{} {}'.format(self.start, self.end, self.data)

    def convert_to_tile(self, serial):
        """
            Given an Update object translate char to tile values
        """
        tile_layout = TileLayout(serial)
        rom_layout = RomLayout(serial)
        tile_set = rom_layout.get_tile_set(serial, self.start)
        res = bytearray()

        for char in self.data:
            res.append(tile_layout.get_hex(char, tile_set))

        return res


def main():
    """
        Main driver
    """
    for csv_file in ARGS.csv:
        cobbler = Cobbler(csv_file, ARGS.serial)
        cobbler.parse_csv()
        cobbler.write_patch()

if __name__ == "__main__":
    main()
