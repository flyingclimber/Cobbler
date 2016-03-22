#!/usr/bin/env python

"""
    cobbler.py - IPS patch creator
"""

PATCH = 'test.ips'


class Patch:
    """
        High level view of a patch
    """
    def __init__(self):
        pass

    def create_patch(self):
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

    def create_patch(self):
        """
            Output a final patch to disk
        """
        with open(PATCH, 'wb') as f:
            f.write(self.header)

            for hunk in self.hunks:
                f.write(hunk.offset)
                f.write(hunk.size)
                f.write(hunk.data)

            f.write(self.footer)


class Hunk:
    """
        Individual IPS record
    """
    def __init__(self, offset, size, data):
        self.offset = offset
        self.size = size
        self.data = data


class Cobbler:
    """
        Someone to put it all together
    """
    def __init__(self):
        pass


def main():
    """
        Main runner
    """
    patch = Ips()
    h1_ = Hunk(bytearray([10]), bytearray([2]), bytearray([50, 100, 104]))
    h2_ = Hunk(bytearray([20]), bytearray([50]),
              bytearray([10, 20, 30, 40, 50, 255]))
    patch.add_hunk(h1_)
    patch.add_hunk(h2_)
    patch.create_patch()


if __name__ == "__main__":
    main()
