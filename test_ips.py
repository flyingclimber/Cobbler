#!/usr/bin/env python

"""
    test_ips.py - Test Class
"""

import unittest
from ips import Ips, Hunk


class IpsTestCase(unittest.TestCase):
    """
        Tests for ips.py
    """
    def test_is_correct_header(self):
        """
            Tests patch string header
        """
        patch = Ips()

        self.assertEqual(patch.header, 'PATCH')

    def test_is_correct_footer(self):
        """
            Tests patch string footer
        """
        patch = Ips()

        self.assertEqual(patch.footer, 'EOF')

    def test_can_create_hunk(self):
        """
            Tests creating a patch with preset values and reading them back
        """
        offset = bytearray([10])
        size = bytearray([2])
        data = bytearray([50, 50, 100, 104])
        h1_ = Hunk(offset, size, data)

        self.assertEqual(h1_.offset, offset)
        self.assertEqual(h1_.size, size)
        self.assertEqual(h1_.data, data)

    def test_can_add_hunk(self):
        """
            Add a hunk to the ips file and read it back
        """
        patch = Ips()
        offset = bytearray([10])
        size = bytearray([2])
        data = bytearray([50, 50, 100, 104])
        h1_ = Hunk(offset, size, data)
        patch.add_hunk(h1_)

        self.assertEqual(patch.hunks[0], h1_)

if __name__ == "__main__":
    unittest.main()
