# Maintainer Wanted

Hi.

Occasionally the developer team of [PTB](https://python-telegram-bot.org) is being asked about the status of this library, [ptbtest](https://pypi.org/project/ptbtest/), which is intended to help write unit tests for bots built with `python-telegram-bot`.

`ptbtest` is currently not maintained and not compatible with recent PTB versions. The former maintainer has transferred the ownership of the [repository](https://github.com/python-telegram-bot/ptbtest) to PTBs dev team. However, we have no resources to maintain `ptbtest` in addition to PTB.

Unfortunately, our first call for maintainers for `ptbtest` was not successful. We therefore decided that the first person who reaches out to us and wants to take over maintenance of `ptbtest` will be granted the corresponding access rights and ownerships. We still expect that person to demonstrate a minimum level of experience with Python packaging, open source development and familiarity with ptbtest.

We are very looking forward to your involvement and hope that `ptbtest` will be continued.

Your PTB Developer Team

---

Original readme below

---

[![Build Status](https://travis-ci.org/Eldinnie/ptbtest.svg?branch=master)](https://travis-ci.org/Eldinnie/ptbtest) [![Documentation Status](https://readthedocs.org/projects/ptbtestsuite/badge/?version=master)](http://ptbtestsuite.readthedocs.io/en/master/?badge=master) [![Coverage Status](https://coveralls.io/repos/github/Eldinnie/ptbtest/badge.svg?branch=master)](https://coveralls.io/github/Eldinnie/ptbtest?branch=master)
[![PyPI](https://img.shields.io/pypi/v/ptbtest.svg)](https://pypi.python.org/pypi/ptbtest) [![PyPI](https://img.shields.io/pypi/pyversions/ptbtest.svg)](https://pypi.python.org/pypi/ptbtest) [![PyPI](https://img.shields.io/pypi/l/ptbtest.svg)](https://pypi.python.org/pypi/ptbtest)

# compatibility
Updated to 11.1.0

# ptbtest
## a testsuite for [Python telegram bot](https://github.com/python-telegram-bot/python-telegram-bot/)

This library is meant for people wanting to write unittests for their python-telegram-bot driven bots.
The following things make this library attractive to create unittests
* Mockbot - A fake bot that does not contact telegram servers
* Works with the updater from telegram.ext
* Generatorclasses to easily create Users, Chats and Updates.

Read the [documentation](http://ptbtestsuite.readthedocs.io/en/master/?badge=master) for further reading and check out the examples.
