from __future__ import absolute_import
import unittest

from ptbtest import BadChatException
from ptbtest import BadUserException
from ptbtest import ChatGenerator
from ptbtest import MessageGenerator
from ptbtest import UserGenerator
from ptbtest import BadMessageException
from ptbtest import BadBotException
from ptbtest import BadMarkupError
from telegram import User, Update
from ptbtest import Mockbot


class TestMessageGeneratorCore(unittest.TestCase):
    def setUp(self):
        self.mg = MessageGenerator()

    def test_is_update(self):
        u = self.mg.get_message()
        self.assertIsInstance(u, Update)

    def test_bot(self):
        u = self.mg.get_message()
        self.assertIsInstance(u.message.bot, Mockbot)
        self.assertEqual(u.message.bot.username, "MockBot")

        b = Mockbot(username="AnotherBot")
        mg2 = MessageGenerator(bot=b)
        u = mg2.get_message()
        self.assertEqual(u.message.bot.username, "AnotherBot")

        with self.assertRaises(BadBotException):
            mg3 = MessageGenerator(bot="Yeah!")

    def test_private_message(self):
        u = self.mg.get_message(private=True)
        self.assertEqual(u.message.from_user.id, u.message.chat.id)

    def test_not_private(self):
        u = self.mg.get_message(private=False)
        self.assertEqual(u.message.chat.type, "group")
        self.assertNotEqual(u.message.from_user.id, u.message.chat.id)

    def test_with_user(self):
        ug = UserGenerator()
        us = ug.get_user()
        u = self.mg.get_message(user=us, private=False)
        self.assertEqual(u.message.from_user.id, us.id)
        self.assertNotEqual(u.message.from_user.id, u.message.chat.id)

        u = self.mg.get_message(user=us)
        self.assertEqual(u.message.from_user, us)
        self.assertEqual(u.message.from_user.id, u.message.chat.id)

        us = "not a telegram.User"
        with self.assertRaises(BadUserException):
            u = self.mg.get_message(user=us)

    def test_with_chat(self):
        cg = ChatGenerator()
        c = cg.get_chat()
        u = self.mg.get_message(chat=c)
        self.assertEqual(u.message.chat.id, u.message.from_user.id)
        self.assertEqual(u.message.chat.id, c.id)

        c = cg.get_chat(type="group")
        u = self.mg.get_message(chat=c)
        self.assertNotEqual(u.message.from_user.id, u.message.chat.id)
        self.assertEqual(u.message.chat.id, c.id)

        c = "Not a telegram.Chat"
        with self.assertRaises(BadChatException):
            self.mg.get_message(chat=c)

    def test_with_chat_and_user(self):
        cg = ChatGenerator()
        ug = UserGenerator()
        us = ug.get_user()
        c = cg.get_chat()
        u = self.mg.get_message(user=us, chat=c)
        self.assertNotEqual(u.message.from_user.id, u.message.chat.id)
        self.assertEqual(u.message.from_user.id, us.id)
        self.assertEqual(u.message.chat.id, c.id)

        us = "not a telegram.User"
        with self.assertRaises(BadUserException):
            u = self.mg.get_message(user=us)

        c = "Not a telegram.Chat"
        with self.assertRaises(BadChatException):
            u = self.mg.get_message(chat=c)


class TestMessageGeneratorText(unittest.TestCase):
    def setUp(self):
        self.mg = MessageGenerator()

    def test_simple_text(self):
        u = self.mg.get_message(text="This is a test")
        self.assertEqual(u.message.text, "This is a test")

    def test_text_with_markdown(self):
        teststr = "we have *bold* `code` [google](www.google.com) @username #hashtag _italics_ ```pre block``` " \
                  "ftp://snt.utwente.nl "
        u = self.mg.get_message(text=teststr)
        self.assertEqual(u.message.text, teststr)

        u = self.mg.get_message(text=teststr, parse_mode="Markdown")
        self.assertEqual(len(u.message.entities), 8)
        for ent in u.message.entities:
            if ent.type == "bold":
                self.assertEqual(ent.offset, 8)
                self.assertEqual(ent.length, 4)
            elif ent.type == "code":
                self.assertEqual(ent.offset, 13)
                self.assertEqual(ent.length, 4)
            elif ent.type == "italic":
                self.assertEqual(ent.offset, 43)
                self.assertEqual(ent.length, 7)
            elif ent.type == "pre":
                self.assertEqual(ent.offset, 51)
                self.assertEqual(ent.length, 9)
            elif ent.type == "text_link":
                self.assertEqual(ent.offset, 18)
                self.assertEqual(ent.length, 6)
                self.assertEqual(ent.url, "www.google.com")
            elif ent.type == "mention":
                self.assertEqual(ent.offset, 25)
                self.assertEqual(ent.length, 9)
            elif ent.type == "hashtag":
                self.assertEqual(ent.offset, 35)
                self.assertEqual(ent.length, 8)
            elif ent.type == "url":
                self.assertEqual(ent.offset, 62)
                self.assertEqual(ent.length, 20)

        with self.assertRaises(BadMarkupError):
            self.mg.get_message(
                text="bad *_double_* markdown", parse_mode="Markdown")

    def test_with_html(self):
        teststr = "we have <b>bold</b> <code>code</code> <a href='www.google.com'>google</a> @username #hashtag " \
                  "<i>italics</i> <pre>pre block</pre> ftp://snt.utwente.nl "
        u = self.mg.get_message(text=teststr)
        self.assertEqual(u.message.text, teststr)

        u = self.mg.get_message(text=teststr, parse_mode="HTML")
        self.assertEqual(len(u.message.entities), 8)
        for ent in u.message.entities:
            if ent.type == "bold":
                self.assertEqual(ent.offset, 8)
                self.assertEqual(ent.length, 4)
            elif ent.type == "code":
                self.assertEqual(ent.offset, 13)
                self.assertEqual(ent.length, 4)
            elif ent.type == "italic":
                self.assertEqual(ent.offset, 43)
                self.assertEqual(ent.length, 7)
            elif ent.type == "pre":
                self.assertEqual(ent.offset, 51)
                self.assertEqual(ent.length, 9)
            elif ent.type == "text_link":
                self.assertEqual(ent.offset, 18)
                self.assertEqual(ent.length, 6)
                self.assertEqual(ent.url, "www.google.com")
            elif ent.type == "mention":
                self.assertEqual(ent.offset, 25)
                self.assertEqual(ent.length, 9)
            elif ent.type == "hashtag":
                self.assertEqual(ent.offset, 35)
                self.assertEqual(ent.length, 8)
            elif ent.type == "url":
                self.assertEqual(ent.offset, 62)
                self.assertEqual(ent.length, 20)

        with self.assertRaises(BadMarkupError):
            self.mg.get_message(
                text="bad <b><i>double</i></b> markup", parse_mode="HTML")


class TestMessageGeneratorReplies(unittest.TestCase):
    def setUp(self):
        self.mg = MessageGenerator()

    def test_reply(self):
        u1 = self.mg.get_message(text="this is the first")
        u2 = self.mg.get_message(
            text="This is the second", reply_to_message=u1.message)
        self.assertEqual(u1.message.text, u2.message.reply_to_message.text)

        with self.assertRaises(BadMessageException):
            u = "This is not a Messages"
            self.mg.get_message(reply_to_message=u)


class TestMessageGeneratorForwards(unittest.TestCase):
    def setUp(self):
        self.mg = MessageGenerator()
        self.ug = UserGenerator()
        self.cg = ChatGenerator()

    def test_forwarded_message(self):
        u1 = self.ug.get_user()
        u2 = self.ug.get_user()
        c = self.cg.get_chat(type="group")
        u = self.mg.get_message(
            user=u1, chat=c, forward_from=u2, text="This is a test")
        self.assertEqual(u.message.from_user.id, u1.id)
        self.assertEqual(u.message.forward_from.id, u2.id)
        self.assertNotEqual(u.message.from_user.id, u.message.forward_from.id)
        self.assertEqual(u.message.text, "This is a test")
        self.assertIsInstance(u.message.forward_date, int)

        with self.assertRaises(BadUserException):
            u3 = "This is not a User"
            u = self.mg.get_message(
                user=u1, chat=c, forward_from=u3, text="This is a test")

    def test_forwarded_channel_message(self):
        c = self.cg.get_chat(type="channel")
        us = self.ug.get_user()
        u = self.mg.get_message(
            text="This is a test", forward_from=us, forward_from_chat=c)
        self.assertNotEqual(u.message.chat.id, c.id)
        self.assertNotEqual(u.message.from_user.id, us.id)
        self.assertEqual(u.message.forward_from.id, us.id)
        self.assertEqual(u.message.text, "This is a test")
        self.assertIsInstance(u.message.forward_from_message_id, int)
        self.assertIsInstance(u.message.forward_date, int)

        u = self.mg.get_message(text="This is a test", forward_from_chat=c)
        self.assertNotEqual(u.message.from_user.id, u.message.forward_from.id)
        self.assertIsInstance(u.message.forward_from, User)
        self.assertIsInstance(u.message.forward_from_message_id, int)
        self.assertIsInstance(u.message.forward_date, int)

        with self.assertRaises(BadChatException):
            c = "Not a Chat"
            u = self.mg.get_message(text="This is a test", forward_from_chat=c)

        with self.assertRaises(BadChatException):
            c = self.cg.get_chat("group")
            u = self.mg.get_message(text="This is a test", forward_from_chat=c)


if __name__ == '__main__':
    unittest.main()
