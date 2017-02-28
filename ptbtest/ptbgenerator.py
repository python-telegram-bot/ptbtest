#!/usr/bin/env python
# pylint: disable=E0611,E0213,E1102,C0103,E1101,W0613,R0913,R0904
#
# A library that provides a testing suite fot python-telegram-bot
# wich can be found on https://github.com/python-telegram-bot/python-telegram-bot
# Copyright (C) 2017
# Pieter Schutz - https://github.com/eldinnie
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
"""This module contains a base class for class generators."""
import random


class PtbGenerator:
    """Base class for all generators."""

    def __init__(self):
        pass

    @staticmethod
    def gen_id(group=False):
        """
        Returns an id in the range telegram id's are valid. defaults to a positive int for a private chat.

        Args:
            group (optional[bool]): If True will return a negative id for a group chat.

        Returns:
            int: positive or negitve depending on group argument,

        """
        if group:
            return random.randint(-99999999, -222222)
        else:
            return random.randint(10000, 99999999)
