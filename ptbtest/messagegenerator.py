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
"""This module provides a class to generate telegram mesages"""

from .ptbgenerator import PtbGenerator
from telegram import Message, Chat, User
from ptbtest import UserGenerator, ChatGenerator
from ptbtest.errors import BadUserException, BadMessageException
from ptbtest.errors import BadChatException, BadBotException
from ptbtest.errors import BadMarkupError
from ptbtest.updategenerator import update
import datetime
import time
from ptbtest import Mockbot
from .entityparser import EntityParser


class MessageGenerator(PtbGenerator):
    """
        Message generator class.

        Attributes:
            bot (ptbtest.Mockbot): Bot to encode with the messages

        Args:
            bot (Optional[ptbtest.Mockbot])
    """

    def __init__(self, bot=None):
        PtbGenerator.__init__(self)
        self.idgen = self._gen_id()
        self.ug = UserGenerator()
        self.cg = ChatGenerator()
        if not bot:
            self.bot = Mockbot()
        elif isinstance(bot, Mockbot):
            self.bot = bot
        else:
            raise BadBotException

    def _gen_id(self):
        x = 1
        while True:
            yield x
            x += 1

    @update
    def get_message(self,
                    user=None,
                    chat=None,
                    private=True,
                    forward_from=None,
                    forward_from_chat=None,
                    forward_date=None,
                    reply_to_message=None,
                    text=None,
                    entities=None,
                    audio=None,
                    document=None,
                    photo=None,
                    sticker=None,
                    video=None,
                    voice=None,
                    caption=None,
                    contact=None,
                    location=None,
                    venue=None,
                    new_chat_member=None,
                    left_chat_member=None,
                    new_chat_title=None,
                    new_chat_photo=None,
                    delete_chat_photo=False,
                    group_chat_created=False,
                    supergroup_chat_created=False,
                    migrate_to_chat_id=None,
                    migrate_from_chat_id=None,
                    channel_chat_created=False,
                    pinned_message=None,
                    forward_from_message_id=None,
                    parse_mode=None):
        """
        When called without arguments will return an update object for a message from a private chat with a
        random user. for modifiers see args.

        Args/Attributes:
            user (Optional[telegram.User]): User the message is from (m.from_user)
            chat (Optional[telegram.Chat]): Chat the message is from (m.chat).
            private (Optional[bool]): If the message is private (optionally with the supplied user) default=True
            text (str): The text for the message, can make use of markdown or html, make sure to specify with parse_mode
            parse_mode (Optional[str]): "HTML" or "Markdown" parses the text and fills entities
            entities (Optional[lst(telegram.MessageEntity)]): when text and parsemode are set this will be filled with
            the entities in the text.
            reply_to_message (Optional[telegram.Message): Messages this one is a reply to
            forward_from (Optional[telegram.User): User this message is forwarded from
            forward_from_chat (Optional[telegram.Chat]): channel this message is forwarded from
            forward_date (Optional[int]): Original sent date
            forward_from_message_id (Optional[int]): message id from forwarded channel post.
            pinned_message (Optional[telegram.Message]):
            channel_chat_created (Optional[True]):
            migrate_from_chat_id (Optional[int]):
            migrate_to_chat_id (Optional[int]):
            supergroup_chat_created (Optional[True]):
            group_chat_created (Optional[True]):
            delete_chat_photo (Optional[True]):
            new_chat_photo (Optional[lst(telegram.Photosize)]):
            new_chat_title (Optional[str]):
            left_chat_member (Optional[telegram.User]):
            new_chat_member (Optional[telegram.User]):
            venue (Optional[telegram.Venue]):
            location (optional[telegram.Location]):
            contact (optional[telegram.Contact]):
            caption (Optional[str]):
            voice (Optional[telegram.Voice]):
            video (Optional[telegram.Video]):
            sticker (Optional[telegram.Sticker]):
            photo (Optional[lst(telegram.PhotoSize)]):
            document (Optional[telegram.Document]):
            audio (Optional[telegram.Audio]):



        Returns:
            telegram.Update: A telegram update object containing a message.
        """
        user, chat = self._get_user_and_chat(user, chat, private)

        if reply_to_message and not isinstance(reply_to_message, Message):
            raise BadMessageException

        forward_date, forward_from, forward_from_message_id = self._handle_forward(
            forward_date, forward_from, forward_from_chat,
            forward_from_message_id)

        text, entities = self._handle_text(text, entities, parse_mode)

        return Message(
            next(self.idgen),
            user,
            None,
            chat,
            text=text,
            forward_from=forward_from,
            forward_from_chat=forward_from_chat,
            reply_to_message=reply_to_message,
            entities=entities,
            audio=audio,
            document=document,
            photo=photo,
            sticker=sticker,
            video=video,
            voice=voice,
            caption=caption,
            contact=contact,
            location=location,
            venue=venue,
            new_chat_member=new_chat_member,
            left_chat_member=left_chat_member,
            new_chat_title=new_chat_title,
            new_chat_photo=new_chat_photo,
            delete_chat_photo=delete_chat_photo,
            group_chat_created=group_chat_created,
            supergroup_chat_created=supergroup_chat_created,
            migrate_to_chat_id=migrate_to_chat_id,
            migrate_from_chat_id=migrate_from_chat_id,
            channel_chat_created=channel_chat_created,
            pinned_message=pinned_message,
            forward_from_message_id=forward_from_message_id,
            forward_date=forward_date,
            bot=self.bot)

    def _get_user_and_chat(self, user, chat, private):
        if chat and user:
            if not isinstance(chat, Chat):
                raise BadChatException
            if not isinstance(user, User):
                raise BadUserException
        elif chat:
            if not isinstance(chat, Chat):
                raise BadChatException
            if chat.type == "private":
                user = self.ug.get_user(
                    first_name=chat.first_name,
                    last_name=chat.last_name,
                    username=chat.username,
                    id=chat.id)
            else:
                user = self.ug.get_user()
        elif user and private:
            if not isinstance(user, User):
                raise BadUserException
            chat = self.cg.get_chat(user=user)
        elif user:
            if not isinstance(user, User):
                raise BadUserException
            chat = self.cg.get_chat(type="group")
        elif private:
            user = self.ug.get_user()
            chat = self.cg.get_chat(user=user)
        else:
            user = self.ug.get_user()
            chat = self.cg.get_chat(type="group")
        return user, chat

    def _handle_forward(self, forward_date, forward_from, forward_from_chat,
                        forward_from_message_id):
        if forward_from and not isinstance(forward_from, User):
            raise BadUserException
        if forward_from_chat:
            if not isinstance(forward_from_chat, Chat):
                raise BadChatException
            if forward_from_chat.type != "channel":
                raise BadChatException(
                    'forward_from_chat must be of type "channel"')
            if not forward_from:
                forward_from = UserGenerator().get_user()
        if forward_from and not isinstance(forward_date, int):
            if not isinstance(forward_date, datetime.datetime):
                now = datetime.datetime.now()
            else:
                now = forward_date
            try:
                # Python 3.3+
                forward_date = int(now.timestamp())
            except AttributeError:
                # Python 3 (< 3.3) and Python 2
                forward_date = int(time.mktime(now.timetuple()))
        if (forward_from_message_id and
                not isinstance(forward_from_message_id, int)) or (
                    forward_from_chat and not forward_from_message_id):
            forward_from_message_id = next(self.idgen)
        return forward_date, forward_from, forward_from_message_id

    def _handle_text(self, text, entities, parse_mode):
        if text and entities:
            pass
        elif text and parse_mode:
            if parse_mode not in ["HTML", "Markdown"]:
                raise BadMarkupError('Mardown mode must be HTML or Markdown')
            elif parse_mode == "HTML":
                text, entities = EntityParser.parse_html(text)
            else:
                text, entities = EntityParser.parse_markdown(text)

        return text, entities
