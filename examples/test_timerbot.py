from __future__ import absolute_import
import unittest

import time

from telegram.ext import CommandHandler
from telegram.ext import Job
from telegram.ext import Updater

from ptbtest import ChatGenerator
from ptbtest import MessageGenerator
from ptbtest import Mockbot

"""
This is an example to show how the ptbtest suite can be used.
This example follows the timerbot example at:
https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/timerbot.py
We will skip the start and help handlers and focus on the timer.

"""
class Testtimerbot(unittest.TestCase):
    def setUp(self):
        # For use within the tests we nee some stuff. Starting with a Mockbot
        self.bot = Mockbot()
        # Some generators for users and chats
        self.cg = ChatGenerator()
        # And a Messagegenerator and updater (for use with the bot.)
        self.mg = MessageGenerator(self.bot)
        self.updater = Updater(bot=self.bot)

    def test_timer(self):
        # first declare the callback methods
        def alarm(bot, job):
            """Function to send the alarm message"""
            bot.sendMessage(job.context, text='Beep!')

        def set(bot, update, args, job_queue, chat_data):
            """Adds a job to the queue"""
            chat_id = update.message.chat_id
            try:
                # args[0] should contain the time for the timer in seconds
                due = int(args[0])
                if due < 0:
                    update.message.reply_text('Sorry we can not go back to future!')
                    return

                # Add job to queue
                job = Job(alarm, due, repeat=False, context=chat_id)
                chat_data['job'] = job
                job_queue.put(job)

                update.message.reply_text('Timer successfully set!')

            except (IndexError, ValueError):
                update.message.reply_text('Usage: /set <seconds>')

        def unset(bot, update, chat_data):
            """Removes the job if the user changed their mind"""

            if 'job' not in chat_data:
                update.message.reply_text('You have no active timer')
                return

            job = chat_data['job']
            job.schedule_removal()
            del chat_data['job']

            update.message.reply_text('Timer successfully unset!')
        # Now add those handlers to the updater and start polling
        dp = self.updater.dispatcher
        dp.add_handler(CommandHandler("set", set,
                                      pass_args=True,
                                      pass_job_queue=True,
                                      pass_chat_data=True))
        dp.add_handler(CommandHandler("unset", unset, pass_chat_data=True))
        self.updater.start_polling()

        #  we want to check if the bot returns a message to the same chat after a period of time
        # so let's create a chat to use
        chat = self.cg.get_chat()

        # let's generate some updates we can use
        u1 = self.mg.get_message(chat=chat, text="/set")
        u2 = self.mg.get_message(chat=chat, text="/set -20")
        u3 = self.mg.get_message(chat=chat, text="/set 6")
        u4 = self.mg.get_message(chat=chat, text="/unset")

        # first check some errors
        self.bot.insertUpdate(u1)
        self.bot.insertUpdate(u2)
        self.bot.insertUpdate(u4)
        data = self.bot.sent_messages
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]['text'], "Usage: /set <seconds>")
        self.assertEqual(data[1]['text'], 'Sorry we can not go back to future!')
        self.assertEqual(data[2]['text'], 'You have no active timer')

        # now check if setting and unsetting works (within timer limit)
        self.bot.insertUpdate(u3)
        data = self.bot.sent_messages[-1]
        self.assertEqual(data['text'], 'Timer successfully set!')
        time.sleep(2)
        self.bot.insertUpdate(u4)
        data = self.bot.sent_messages[-1]
        self.assertEqual(data['text'], 'Timer successfully unset!')
        # and to be certain we have to wait some more to see if it stops sending the message
        # we reset the bot so we can be sure nothing more has been sent
        self.bot.reset()
        time.sleep(5)
        data = self.bot.sent_messages
        self.assertEqual(len(data), 0)

        # lastly we will make sure an alarm message is sent after the timelimit has passed
        self.bot.insertUpdate(u3)
        time.sleep(6)
        data = self.bot.sent_messages[-1]
        self.assertEqual(data['text'], 'Beep!')
        self.assertEqual(data['chat_id'], chat.id)

        # and stop the updater.
        self.updater.stop()


if __name__ == '__main__':
    unittest.main()