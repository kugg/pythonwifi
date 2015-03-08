"""
# -*- coding: utf-8 -*-
# Python WiFi -- a library to access wireless card properties via Python
# Copyright (C) 2004 - 2008 Roman Joost
# Copyright (C) 2008 - 2013 Sean Robinson
# Copyright (C) 2015 Christoffer Jerkeby
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public License
#    as published by the Free Software Foundation; either version 2.1 of
#    the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
#    USA

Helper-functions in this file MAY NOT depend on WEXT or nl80211.
"""
import math
import os
import re


def get_nic_names():
    """
    Return list of Network Interface Cards currently available.
    Extract network device names from /proc/net/dev or /sys/class/net

        Returns list of device names.  Returns empty list if no network
        devices are present.

        >>> get_nic_names()
        ['lo', 'eth0']

    """
    try:
        return get_nic_names_sysfs()
    except IOError:
        try:
            return get_nic_names_proc()
        except IOError:
            return []


def get_nic_names_sysfs():
    """
    Return a list containing the interfaces in /sys/class/net
    Raise IOError if /sys/class/net is not found
    """
    return os.listdir("/sys/class/net")


def get_nic_names_proc():
    """
    Return a list containing the interfaces in /proc/net/dev
    Raise IOError if /proc/net/dev is not found.
    """
    device = re.compile('[a-z]{2,}[0-9]*:')
    ifnames = []

    devfile = open('/proc/net/dev', 'r')
    for line in devfile:
        try:
            # append matching pattern, without the trailing colon
            ifnames.append(device.search(line).group()[:-1])
        except AttributeError:
            pass

    devfile.close()
    return ifnames


def get_wnic_names():
    """
    Return list of Wireless Network Interface Cards currently available
    from /proc/net/wireless or /sys/class/net/*.

    Return empty list if no devices are present.

    >>> get_wnic_names()
    ['eth1', 'wifi0']
    """
    try:
        return get_wnic_names_sysfs()
    except IOError:
        return get_wnic_names_proc()


def get_wnic_names_sysfs():
    """
    Return a list containing the interfaces with wifi capability
    listed in /sys/class/net/*/phy80211
    """
    ifnames = get_nic_names_sysfs()
    wifnames = []
    for ifname in ifnames:
        phypath = "/sys/class/net/%s/phy80211/" % (ifname)
        if os.path.exists(phypath):
            wifnames.append(ifname)
    return wifnames


def get_wnic_names_proc():
    """
    Return a list containing the interfaces in /proc/net/wireless
    Raise IOError if /proc/net/wireless is not found.
    """

    ifnames = []

    devfile = open('/proc/net/wireless', 'r')
    device = re.compile('[a-z]{2,}[0-9]*:')
    for line in devfile:
        try:
            # append matching pattern, without the trailing colon
            ifnames.append(device.search(line).group()[:-1])
        except AttributeError:
            pass

    devfile.close()
    return ifnames


def get_phy_name_sysfs(ifname):
    """
    Return the phy name of a network interface name.
    Raise IOError on insufficient permissions /sys/class/net/*/phy80211/name
    """
    phynamepath = "/sys/class/net/%s/phy80211/name" % (ifname)

    try:
        phyfile = open(phynamepath)
        phyname = phyfile.read().strip()
        phyfile.close()
    except IOError as error:
        if error.errno == 13:
            raise

    try:
        return phyname
    except UnboundLocalError:
        # raise ValueError ("This is not a phy80211 devoce")
        pass


def get_phy_names():
    """
    Return a list of phy interface names.
    For more information about PHY see the Documentation/networking/phy.txt
    in the Linux kernel source.
    """
    ifnames = get_nic_names()
    phynames = []

    for ifname in ifnames:
        phynames.append(get_phy_name_sysfs(ifname))

    return phynames


def get_wiphy_names():
    """
    Return a list of all wireless enabled PHY interface names.
    For more information about PHY see the Documentation/networking/phy.txt
    in the Linux kernel source.
    """
    wifnames = get_wnic_names()
    phynames = []

    for wifname in wifnames:
        phynames.append(get_phy_name_sysfs(wifname))

    return phynames


def ifname_to_index(ifname):
    """
    Return interface index of interface name.
    Similar to if_nametoindex() in net/if.h from POSIX.
    Raise ValueError if the interface is not found.
    Raise ValueError if the index information is not integer.
    """
    return ifname_to_index_sysfs(ifname)


def ifname_to_index_proc(ifname):
    """
    Return interface index of interface name.
    Similar to if_nametoindex() in net/if.h from POSIX.
    Raise ValueError if the interface is not found.
    Raise ValueError if the index information is not integer.
    This function depends on the availability of /proc filesystem.
    """
    raise NotImplementedError
    # TODO: Make the least ugly /proc/ned/dev parser to collect if index.
    ifname = ""
    return ifname


def ifname_to_index_sysfs(ifname):
    """
    Return interface index of interface name.
    Similar to if_nametoindex() in net/if.h from POSIX.
    Raise ValueError if the interface is not found.
    Raise ValueError if the index information is not integer.
    This function depends on the availability of /sys filesystem.
    """

    phynamepath = "/sys/class/net/%s/ifindex" % (ifname)

    try:
        phyfile = open(phynamepath)
        index = int(phyfile.read())
        phyfile.close()

    except IOError as error:
        if error.errno == 13:
            raise
    except ValueError:
        raise ValueError("Index is not an integer.")
    try:
        return index
    except UnboundLocalError:
        raise ValueError("Interface not found.")


def index_to_ifname(index):
    """
    Return string of interface name from a given index.
    Simialar to if_indextoname() in net/if.h from POSIX.
    Raise ValueError if the index is not corresponding to an interface.
    """
    return index_to_ifname_sysfs(index)


def index_to_ifname_proc(index):
    """
    Return string of interface name from a given index.
    Simialar to if_indextoname() in net/if.h from POSIX.
    Raise ValueError if the index is not corresponding to an interface.
    This function depends on the availability of the /proc filesystem.
    """
    raise NotImplementedError
    # TODO: Make the least ugly /proc/ned/dev parser to collect if index.
    ifname = ""
    return ifname


def index_to_ifname_sysfs(index):
    """
    Return string of interface name from a given index.
    Simialar to if_indextoname() in net/if.h from POSIX.
    Raise ValueError if the index is not corresponding to an interface.
    This function depends on the availability of the /sys filesystem.
    """
    ifnames = get_nic_names()
    for ifname in ifnames:
        ifindexpath = "/sys/class/net/%s/ifindex" % (ifname)
        try:
            ifindexfile = open(ifindexpath)
            ifindex = int(ifindexfile.read())
            ifindexfile.close()

        except IOError as error:
            if error.errno == 13:
                raise
        except ValueError:
            # raise ValueError("Index in sysfs is not an integer.")
            pass
        if ifindex == index:
            return ifname
    raise ValueError("Index is not corresponding to an interface.")


def mw_to_dbm(mwatt):
    """Convert mW to log dBm (float)."""
    return math.log10(mwatt) * 10.0


def dbm_to_mw(dbm):
    """Convert log dBm values to linear mW"""
    return pow(10.0, (dbm / 10.0))


def abs_to_dbm(power):
    """
    Absolute power measurement in dBm (IW_QUAL_DBM):
    map into -192 .. 63 range
    """

    if power > 63:
        return power - 0x100
    else:
        return power


def dbm_to_power(dbm):
    """Convert dbm to power unit return string value in pW nW uW or mW"""
    with_units = ""
    val = dbm_to_mw(dbm)

    if val < 0.00000001:
        with_units = "%.2f pW" % (val * 1e9)
    elif val < 0.00001:
        with_units = "%.2f nW" % (val * 1e6)
    elif val < 0.01:
        with_units = "%.2f uW" % (val * 1e3)
    else:
        with_units = "%.2f mW" % (val)
    return with_units


def makedict(**kwargs):
    """Return dict from arguments"""
    return kwargs


def hex_to_int(hexstring):
    """ Convert hex string to integer. """
    return int(hexstring, 16)
