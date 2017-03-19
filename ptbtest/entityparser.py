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
"""This module provides a helperclass to transform marked_up messages to plaintext with entities"""
import re
from ptbtest.errors import BadMarkupError
from telegram import MessageEntity


class EntityParser():
    # MENTION = 'mention'
    # HASHTAG = 'hashtag'
    # BOT_COMMAND = 'bot_command'
    # URL = 'url'
    # EMAIL = 'email'
    # BOLD = 'bold'
    # ITALIC = 'italic'
    # CODE = 'code'
    # PRE = 'pre'
    # TEXT_LINK = 'text_link'
    # TEXT_MENTION = 'text_mention'
    # ALL_TYPES = [
    #     MENTION, HASHTAG, BOT_COMMAND, URL, EMAIL, BOLD, ITALIC, CODE, PRE, TEXT_LINK, TEXT_MENTION
    # ]
    def __init__(self):
        pass

    @staticmethod
    def parse_markdown(message):
        entities = []
        invalids = re.compile(
            r'''(\*_|\*```|\*`|\*\[.*?\]\(.*?\)|_\*|_```|_`|_\[.*?\]\(.*?\)|```\*|```_|
                                  ```\[.*?\]\(.*?\)|`\*|`_|`\[.*?\]\(.*?\)|\[.*?\]\(.*?\)\*|
                                  \[.*?\]\(.*?\)_|\[.*?\]\(.*?\)```|\[.*?\]\(.*?\)`)'''
        )
        markdowns = re.compile(r'(([`]{3}|\*|_|`)(.*?)(\2))')
        text_links = re.compile(r'(\[(.*?)\]\((.*?)\))')
        mentions = re.compile(r'@[a-zA-Z0-9]{1,}\b')
        hashtags = re.compile(r'#[a-zA-Z0-9]{1,}\b')
        botcommands = re.compile(r'(?<!\/|\w)\/[a-zA-Z0-0_\-]{1,}\b')
        urls = re.compile(
            r'(([hHtTpP]{4}[sS]?|[fFtTpP]{3})://)?([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?'
        )

        inv = invalids.search(message)
        if inv:
            raise BadMarkupError(
                "nested markdown is not supported. your text: {}".format(
                    inv.groups()[0]))

        while markdowns.search(message):
            markdown = markdowns.search(message)
            text = markdown.groups()[2]
            start = markdown.start()
            if markdown.groups()[1] == "*":
                type = "bold"
            elif markdown.groups()[1] == "_":
                type = "italic"
            elif markdown.groups()[1] == "`":
                type = "code"
            elif markdown.groups()[1] == "```":
                type = "pre"
            entities.append(MessageEntity(type, start, len(text)))
            message = markdowns.sub(r'\3', message, count=1)

        while text_links.search(message):
            link = text_links.search(message)
            url = link.groups()[2]
            text = link.groups()[1]
            start = link.start()
            length = len(text)
            for x, ent in enumerate(entities):
                if ent.offset > start:
                    entities[x].offset -= link.end() - start - length + 1
            entities.append(MessageEntity('text_link', start, length, url=url))
            message = text_links.sub(r'\2', message, count=1)

        for mention in mentions.finditer(message):
            entities.append(
                MessageEntity('mention',
                              mention.start(), mention.end() - mention.start(
                              )))
        for hashtag in hashtags.finditer(message):
            entities.append(
                MessageEntity('hashtag',
                              hashtag.start(), hashtag.end() - hashtag.start(
                              )))

        for botcommand in botcommands.finditer(message):
            entities.append(
                MessageEntity('bot_command',
                              botcommand.start(),
                              botcommand.end() - botcommand.start()))
        for url in urls.finditer(message):
            entities.append(
                MessageEntity('url', url.start(), url.end() - url.start()))

        return message, entities

    @staticmethod
    def parse_html(message):
        entities = []
        invalids = re.compile(r'''(<b><i>|<b><pre>|<b><code>|<b>(<a.*?>)|
                                   <i><b>|<i><pre>|<i><code>|<i>(<a.*?>)|
                                   <pre><b>|<pre><i>|<pre><code>|<pre>(<a.*?>)|
                                   <code><b>|<code><i>|<code><pre>|<code>(<a.*?>)|
                                   (<a.*>)?<b>|(<a.*?>)<i>|(<a.*?>)<pre>|(<a.*?>)<code>)'''
                              )
        tags = re.compile(r'(<(b|i|pre|code)>(.*?)<\/\2>)')
        text_links = re.compile(r'<a href=[\'\"](.*?)[\'\"]>(.*?)<\/a>')
        mentions = re.compile(r'@[a-zA-Z0-9]{1,}\b')
        hashtags = re.compile(r'#[a-zA-Z0-9]{1,}\b')
        botcommands = re.compile(r'(?<!\/|\w)\/[a-zA-Z0-0_\-]{1,}\b')
        urls = re.compile(
            r'(([hHtTpP]{4}[sS]?|[fFtTpP]{3})://)?([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?'
        )

        inv = invalids.search(message)
        if inv:
            raise BadMarkupError("nested html is not supported. your text: {}".
                                 format(inv.groups()[0]))

        while tags.search(message):
            tag = tags.search(message)
            text = tag.groups()[2]
            start = tag.start()
            if tag.groups()[1] == "b":
                type = "bold"
            elif tag.groups()[1] == "i":
                type = "italic"
            elif tag.groups()[1] == "code":
                type = "code"
            elif tag.groups()[1] == "pre":
                type = "pre"
            entities.append(MessageEntity(type, start, len(text)))
            message = tags.sub(r'\3', message, count=1)

        while text_links.search(message):
            link = text_links.search(message)
            url = link.groups()[0]
            text = link.groups()[1]
            start = link.start()
            length = len(text)
            for x, ent in enumerate(entities):
                if ent.offset > start:
                    entities[x].offset -= link.end() - start - length + 1
            entities.append(MessageEntity('text_link', start, length, url=url))
            message = text_links.sub(r'\2', message, count=1)

        for mention in mentions.finditer(message):
            entities.append(
                MessageEntity('mention',
                              mention.start(), mention.end() - mention.start(
                              )))
        for hashtag in hashtags.finditer(message):
            entities.append(
                MessageEntity('hashtag',
                              hashtag.start(), hashtag.end() - hashtag.start(
                              )))

        for botcommand in botcommands.finditer(message):
            entities.append(
                MessageEntity('bot_command',
                              botcommand.start(),
                              botcommand.end() - botcommand.start()))
        for url in urls.finditer(message):
            entities.append(
                MessageEntity('url', url.start(), url.end() - url.start()))

        return message, entities
