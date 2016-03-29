#!/usr/bin/env python

"""
    cobbler.py - Dedicated IPS patching worker
"""

import csv
import argparse
from rom import Rom, RomLayout, TileLayout
from ips import Ips, Hunk
from openpyxl import load_workbook
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

PARSER = argparse.ArgumentParser(description='IPS patch creator')
PARSER.add_argument('--serial', dest='serial', default='DMG-NDJ',
                    help='ROM serial')
PARSER.add_argument('--download', action='store_true', help='Download XLSX')
PARSER.add_argument('--csv', dest='csv', nargs='+', help='CSV input list')
PARSER.add_argument('--xlsx', dest='xlsx', help='XLSX input list')
PARSER.add_argument('--patch', dest='patch', default='test.ips',
                    help='Patch file name')

ARGS = PARSER.parse_args()
GAUTH_CREDS_FILE = 'creds.txt'


class Cobbler:
    """
        Someone to put it all together
    """
    def __init__(self, file_input, serial):
        self.input = file_input
        self.serial = serial
        self.ips = Ips()
        self.rom = Rom()

    def parse_csv(self):
        """
            Given a csv create Updates and fetch tiles
        """
        with open(self.input, 'rb') as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                if row['Start']:
                    update = Update(int(row['Start'], 16),
                                    int(row['End'], 16),
                                    row['Edited'])
                    update.byte_data = update.convert_to_tile(self.serial)
                    hunk = Hunk(update.start, update.length, update.byte_data)
                    self.ips.add_hunk(hunk)

    def parse_xlsx(self):
        """
            Given a xlsx create Updates and fetch tiles
        """
        wb_ = load_workbook(self.input)
        progress_sheet = wb_.get_sheet_by_name('Project Progress')
        cells = progress_sheet['A2:E9']
        sheet_titles = []

        for cell in cells:
            if cell[4].value == 'Y':
                sheet_titles.append(cell[0].value)

        for sheet_name in sheet_titles:
            sheet = wb_.get_sheet_by_name(sheet_name)
            cells = sheet['A2:I20']

            for cel in cells:
                if cel[8].value == 'Y':
                    update = Update(int(cel[0].value, 16),
                                    int(cel[1].value, 16),
                                    cel[4].value)
                    update.byte_data = update.convert_to_tile(self.serial)
                    hunk = Hunk(update.start, update.length, update.byte_data)
                    self.ips.add_hunk(hunk)

    def write_patch(self):
        """
            Write out the IPS patch file
        """
        self.ips.create_patch(ARGS.patch)

    def download_xlsx(self, file_name):
        """
            Pull the latest Drive copy of spreadsheet
        """
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile(GAUTH_CREDS_FILE)

        if gauth.credentials is None:
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()

        gauth.SaveCredentialsFile(GAUTH_CREDS_FILE)

        drive = GoogleDrive(gauth)

        query_string = "fullText contains '{}'".format(self.serial)
        document = drive.ListFile({'q': query_string}).GetList()
        xlsx = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        document[0].GetContentFile(file_name, mimetype=xlsx)


class Update:
    """
        Internal object to track patch attributes and tile table translations
    """
    def __init__(self, start, end, data):
        self.start = start
        self.end = end
        self.data = data
        self.byte_data = bytearray()
        self.length = len(data)

    def __str__(self):
        return '{}-{} {}'.format(self.start, self.end, self.data)

    def convert_to_tile(self, serial):
        """
            Given an Update object translate char to tile values
        """
        tile_layout = TileLayout()
        rom_layout = RomLayout()

        tile_set = rom_layout.get_tile_set(serial, self.start)
        res = bytearray()

        for char in self.data:
            res.append(tile_layout.get_hex(serial, char, tile_set))

        return res


def main():
    """
        Main driver
    """
    if ARGS.download:
        cobbler = Cobbler('', ARGS.serial)
        cobbler.download_xlsx(cobbler.serial + '.xlsx')
    elif ARGS.xlsx:
        cobbler = Cobbler(ARGS.xlsx, ARGS.serial)
        cobbler.parse_xlsx()
        cobbler.write_patch()
    elif ARGS.csv:
        for csv_file in ARGS.csv:
            cobbler = Cobbler(csv_file, ARGS.serial)
            cobbler.parse_csv()
        cobbler.write_patch()

if __name__ == "__main__":
    main()
