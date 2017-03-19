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
from ptbtest.errors import BadUserException
from ptbtest.errors import BadChatException


class MessageGenerator(PtbGenerator):
    """
        Message generator class. placeholder for random names and mainly used
        via it's get_XXX_message() methods.
    """

    def __init__(self):
        PtbGenerator.__init__(self)
        self.idgen = self._gen_id()
        self.ug = UserGenerator()
        self.cg = ChatGenerator()

    def _gen_id(self):
        x = 1
        while True:
            yield x
            x += 1

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

    def get_message(self,
                    user=None,
                    chat=None,
                    private=True,
                    forward_from=None,
                    forward_from_chat=None,
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
                    forward_from_message_id=None):
        """
        Returns a telegram.Message object

        When called without arguments will return a telegram.Message object for a private chat with a random user.
        for modifiers see args.

        Args:
            forward_from_message_id (Optional[int]):
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
            entities (Optional[lst(telegram.MessageEntity)]):
            reply_to_message (Optional[telegram.Message):
            forward_from_chat (Optional[telegram.Chat]):
            forward_from (Optional[telegram.User):
            text (str): The text for the message
            private (Optional[bool]): If the message is private (optionally with the supplied user) default=True
            chat (Optional[telegram.Chat]): Chat the message is from (m.chat).
            user (Optional[telegram.User]): User the message is from (m.from_user)

        Returns:
            telegram.Message: A telegram Message object.
        """
        user, chat = self._get_user_and_chat(user, chat, private)
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
            forward_from_message_id=forward_from_message_id)
