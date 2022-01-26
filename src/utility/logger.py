#!/usr/bin/env python
# -- coding: utf-8 --
###########################################################################
#
# Copyright (c) 2020 Copyright (c) 2020, Dingshi Inc.  All rights reserved.
#
###########################################################################
import logging


"""use the simplest way of logging"""

LOG_LEVEL = logging.INFO

datetime_format = '%Y-%m-%d %H:%M:%S'
format_string = '[%(levelname)s] %(asctime)s %(filename)s[%(lineno)d] %(message)s'


def init_logging(level=LOG_LEVEL, format=format_string, datefmt=datetime_format):
    logging.basicConfig(level=level, format=format, datefmt=datefmt)


# vim: set expandtab ts=4 sw=4 sts=4 tw=100:
