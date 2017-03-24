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

from .mockbot import Mockbot
from .usergenerator import UserGenerator
from .chatgenerator import ChatGenerator
from .messagegenerator import MessageGenerator
from .callbackquerygenerator import CallbackQueryGenerator
from .inlinequerygenerator import InlineQueryGenerator
from .errors import BadUserException
from .errors import BadChatException
from .errors import BadMessageException
from .errors import BadBotException
from .errors import BadMarkupException
from .errors import BadCallbackQueryException

__all__ = [
    "BadUserException", "BadChatException", "BadMessageException",
    "BadBotException", "Mockbot", "UserGenerator", "ChatGenerator",
    "MessageGenerator", "BadMarkupException", "CallbackQueryGenerator",
    "BadCallbackQueryException", "InlineQueryGenerator"
]
