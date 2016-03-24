#!/usr/bin/env python

"""
    rom.py - Rom related functionality
"""

import json

DATA_DIR = 'data'
TILE_LAYOUT_JSON = 'tile_layout.json'
ROM_LAYOUT_JSON = 'rom_layout.json'


class Rom:
    """
        Game we are patching
    """
    def __init__(self, serial):
        self.serial = serial
        self.rom_layout = RomLayout(serial)
        self.tile_layout = TileLayout(serial)

    def __str__(self):
        return self.serial


class RomLayout:
    """
        Layout table that maps rom address to a tile set
    """
    def __init__(self, serial):
        self.serial = serial

        with open(DATA_DIR + "/" + ROM_LAYOUT_JSON, 'r') as layout_file:
            self.mapping = json.load(layout_file)

    def get_tile_set(self, serial, address):
        """
            Return the tile set that maps to the given address
        """
        for rom_range in self.mapping[serial]:
            start = int(self.mapping[serial][rom_range]['start'], 16)
            end = int(self.mapping[serial][rom_range]['end'], 16)
            address_ = int(address, 16)

            if start <= address_ <= end:
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
