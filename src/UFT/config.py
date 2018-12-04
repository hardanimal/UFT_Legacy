#!/usr/bin/env python
# encoding: utf-8
"""Description: Configuration for UFT program.
"""

__version__ = "0.1"
__author__ = "@fanmuzhi, @boqiling"

import sys
# Projects PartNumber List
DIAMOND4_LIST = ["AGIGA9811-001BCA",
                 "AGIGA9811-001DCA",
                 "AGIGA9811-001BCB",

                 "AGIGA9811-001JCA",
                 "AGIGA9811-001JCB",
                 "AGIGA9811-001JCC",
                 "AGIGA9811-001JCD",
                 "AGIGA9811-001JCE",
                 "AGIGA9811-001JCF",

                 "AGIGA9801-005JCA",
                 "AGIGA9801-105JCA",
                 "AGIGA9801-205JCA",

                 "AGIGA9801-004BCA",
                 "AGIGA9801-004JCA"]

# total slot number for one channel,
# should be 4, 1 for debug
TOTAL_SLOTNUM = 1

# seconds to delay in charging and discharging,
# increase value to reduce the data in database.
# more data, more accurate test result.
INTERVAL = 2

# DUT will discharge to start voltage before testing
START_VOLT = 1.0

# power supply settings
# node address and channel
PS_ADDR = 5
PS_CHAN = 1
# output
PS_VOLT = 12.0
PS_OVP = 13.0
PS_CURR = 5.0
PS_OCP = 10.0

# aardvark settings
# port number
ADK_PORT = 0

# load Settings
# load RS232 port
# LD_PORT = "COM5"
LD_PORT = "COM5"
LD_DELAY = 3

# self discharge counter
SD_COUNTER = 10

# Result Database
RESULT_DB = "./db/pgem.db"

# Configuration database
CONFIG_DB = "./db/pgem_config.db"

# Location to save xml log
RESULT_LOG = "./logs/"

# Configuration files to synchronize
CONFIG_FILE = "./xml/"

# Resource Folder, include images, icons
RESOURCE = "./res/"
