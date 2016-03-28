#!/usr/bin/env python

"""
    ips.py - IPS patch creator
"""

import struct


class Patch:
    """
        High level view of a patch
    """
    def __init__(self):
        pass

    def create_patch(self, file_name):
        """
            Write a patch file to disk
        """
        pass


class Ips(Patch):
    """
        Patch conforming to http://zerosoft.zophar.net/ips.php
    """
    def __init__(self):
        self.type = self.__class__
        self.header = 'PATCH'
        self.footer = 'EOF'
        self.hunks = []

    def add_hunk(self, hunk):
        """
            Add a new block to the total patchset
        """
        if hunk.offset:
            self.hunks.append(hunk)
        else:
            print "Skipping: No offset given"

    def create_patch(self, file_name):
        """
            Output a final patch to disk
        """
        with open(file_name, 'wb') as patch_file:
            patch_file.write(self.header)

            for hunk in self.hunks:
                patch_file.write(hunk.offset)
                patch_file.write(hunk.size)
                patch_file.write(hunk.data)

            patch_file.write(self.footer)


class Hunk:
    """
        Individual IPS record
    """
    def __init__(self, offset, size, data):
        self.offset = struct.pack(">BH", *divmod(offset, 1 << 16))
        self.size = struct.pack('>H', size)
        self.data = data
