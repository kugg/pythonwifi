#!/usr/bin/python
"""
Unittests for pythonwifi
"""

import unittest
from __init__ import *


class TestSequenceFunctions(unittest.TestCase):
    """Test suite for basic helper funcitons of pythonwifi."""
    def setUp(self):
        """Basic test setup."""
        self.nics = []
        self.wnics = []
        self.phynames = []

    def test_get_nic_names(self):
        """List available interfaces."""
        self.nics = get_nic_names()

    def test_get_nic_names_sysfs(self):
        """List available interfaces using sysfs."""
        get_nic_names_sysfs()

    def test_get_nic_names_proc(self):
        """List available interfaces using procfs."""
        get_nic_names_proc()

    def test_get_wnic_names(self):
        """List available Wireless Network Interface Cards."""
        self.wnics = get_wnic_names()

    def test_get_wnic_names_sysfs(self):
        """List available Wireless Network Interface Cards using sysfs."""
        get_wnic_names_sysfs()

    def test_get_wnic_names_proc(self):
        """List available Wireless Network Interface Cards using procfs."""
        get_wnic_names_proc()

    def test_get_phy_name_sysfs(self):
        """
        Test lookup of physical interface from interface name
        using sysfs.
        """
        for nic in self.wnics:
            get_phy_name_sysfs(nic)

    def test_get_phy_names(self):
        """
        Test generic fetching of phy names.
        get_phy_names()
        """
        self.phynames = get_phy_names()

    def test_get_wiphy_names(self):
        """
        Test Wireless PHY interface listing.
        """
        get_wiphy_names()

    def test_ifname_to_index(self):
        """
        Test to verify lookup from interface to index.
        """
        for nic in self.nics:
            ifname_to_index(nic)

    def test_ifname_to_index_sysfs(self):
        """
        Test sysfs lookup of interface to index.
        """
        for nic in self.nics:
            ifname_to_index_sysfs(nic)

    def test_ifname_to_index_proc(self):
        """
        Test proc lookup of interface to index.
        """
        # ifname_to_index_proc(get_nic_names()[1])
        pass

    def test_index_to_ifname(self):
        """
        Test generic lookup of index to interface.
        """
        index_to_ifname(ifname_to_index(get_nic_names()[1]))

    def test_index_to_ifname_sysfs(self):
        """
        Test sysfs lookup of index to interface.
        """
        index_to_ifname_sysfs(ifname_to_index_sysfs(get_nic_names()[1]))

    def test_mw_to_dbm(self):
        """
        Verify mW linear to logarithmic dbm conversion.
        """
        self.assertEqual(mw_to_dbm(16), 12.041199826559248)
        self.assertEqual(mw_to_dbm(9999), 39.999565683801926)

    def test_dbm_to_mw(self):
        """
        Verify log dbm to linear mW conversion.
        """
        self.assertEqual(dbm_to_mw(-192), 6.309573444801943e-20)
        self.assertEqual(15, int(dbm_to_mw(mw_to_dbm(15))))

    def test_abs_to_dbm(self):
        """
        Test abs to dbm conversion.
        """
        abs_to_dbm(63)
        abs_to_dbm(-192)

    def test_dbm_to_power(self):
        """
        Test dbm to power unit conversion.
        """
        self.assertEqual(dbm_to_power(105), '31622776601.68 mW')
        self.assertEqual(dbm_to_power(-105), '0.03 pW')

    def test_makedict(self):
        """
        Test filling of a dict.
        """
        makedict()

    def test_hex_to_int(self):
        """
        Test hex conversion.
        """
        hex_to_int("00AA")


if __name__ == '__main__':
    unittest.main()
