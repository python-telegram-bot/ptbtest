from __future__ import absolute_import
import unittest

from ptbtest import BadChatException
from ptbtest import BadUserException
from ptbtest import ChatGenerator
from ptbtest import MessageGenerator
from ptbtest import UserGenerator
from ptbtest import BadMessageException


class TestMessageGeneratorText(unittest.TestCase):
    def setUp(self):
        self.mg = MessageGenerator()

    def test_simple_text(self):
        m = self.mg.get_message(text="This is a test")
        self.assertEqual(m.text, "This is a test")

        m = self.mg.get_message(text="This is a test", private=False)
        self.assertNotEqual(m.from_user.id, m.chat.id)

    def test_private_message(self):
        m = self.mg.get_message(text="This is a test", private=True)
        self.assertEqual(m.text, "This is a test")
        self.assertEqual(m.from_user.id, m.chat.id)

    def test_with_user(self):
        ug = UserGenerator()
        u = ug.get_user()
        m = self.mg.get_message(text="This is a test", user=u, private=False)
        self.assertEqual(m.text, "This is a test")
        self.assertEqual(m.from_user.id, u.id)
        self.assertNotEqual(m.from_user.id, m.chat.id)

        m = self.mg.get_message(text="This is a test", user=u)
        self.assertEqual(m.text, "This is a test")
        self.assertEqual(m.from_user, u)
        self.assertEqual(m.from_user.id, m.chat.id)

        u = "not a telegram.User"
        with self.assertRaises(BadUserException):
            m = self.mg.get_message(text="This is a test", user=u)

    def test_with_chat(self):
        cg = ChatGenerator()
        c = cg.get_chat()
        m = self.mg.get_message(text="This is a test", chat=c)
        self.assertEqual(m.chat.id, m.from_user.id)
        self.assertEqual(m.chat.id, c.id)
        self.assertEqual(m.text, "This is a test")

        c = cg.get_chat(type="group")
        m = self.mg.get_message(text="This is a test", chat=c)
        self.assertNotEqual(m.from_user.id, m.chat.id)
        self.assertEqual(m.chat.id, c.id)

        c = "Not a telegram.Chat"
        with self.assertRaises(BadChatException):
            self.mg.get_message(text="This is a test", chat=c)

    def test_with_chat_and_user(self):
        cg = ChatGenerator()
        ug = UserGenerator()
        u = ug.get_user()
        c = cg.get_chat()
        m = self.mg.get_message(text="This is a test", user=u, chat=c)
        self.assertNotEqual(m.from_user.id, m.chat.id)
        self.assertEqual(m.from_user.id, u.id)
        self.assertEqual(m.chat.id, c.id)
        self.assertEqual(m.text, "This is a test")

        u = "not a telegram.User"
        with self.assertRaises(BadUserException):
            m = self.mg.get_message(text="This is a test", user=u)

        c = "Not a telegram.Chat"
        with self.assertRaises(BadChatException):
            m = self.mg.get_message(text="This is a test", chat=c)


class TestMessageGeneratorReplies(unittest.TestCase):
    def setUp(self):
        self.mg = MessageGenerator()

    def test_reply(self):
        m1 = self.mg.get_message(text="this is the first")
        m2 = self.mg.get_message(
            text="This is the second", reply_to_message=m1)
        self.assertEqual(m1.text, m2.reply_to_message.text)

        with self.assertRaises(BadMessageException):
            m = "This is not a Messages"
            self.mg.get_message(reply_to_message=m)


class TestMessageGeneratorForwards(unittest.TestCase):
    def setUp(self):
        self.mg = MessageGenerator()

    def test_forwarded_message(self):
        ug = UserGenerator()
        u1 = ug.get_user()
        u2 = ug.get_user()
        cg = ChatGenerator()
        c = cg.get_chat(type="group")
        m = self.mg.get_message(
            user=u1, chat=c, forward_from=u2, text="This is a test")
        self.assertEqual(m.from_user.id, u1.id)
        self.assertEqual(m.forward_from.id, u2.id)
        self.assertNotEqual(m.from_user.id, m.forward_from.id)
        self.assertEqual(m.text, "This is a test")

        with self.assertRaises(BadUserException):
            u3 = "This is not a User"
            m = self.mg.get_message(
                user=u1, chat=c, forward_from=u3, text="This is a test")


if __name__ == '__main__':
    unittest.main()
