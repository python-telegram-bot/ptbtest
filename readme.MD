# Maintainer Wanted

Hi.

Occasionally the developer team of [PTB](https://python-telegram-bot.org) is being asked about the status of this library, [ptbtest](https://pypi.org/project/ptbtest/), which is intended to help write unit tests for bots built with `python-telegram-bot`.

`ptbtest` is currently not maintained and not compatible with recent PTB versions. The former maintainer has transferred the ownership of the [repository](https://github.com/python-telegram-bot/ptbtest) to PTBs dev team. However, we have no resources to maintain `ptbtest` in addition to PTB.

Since we have seen some interest from the community in the continuation of `ptbtest`, we would like to start a search for a new maintainer/developer team. A new maintainer/dev team would be responsible for adapting `ptbtest` to new PTB releases, fixing bugs in `ptbtest` and releasing new versions to PyPi when appropriate. Of course a new maintainer/dev team would be given the appropriate access rights and ownerships. Please note that we are looking for people, who are willing to be committed to the project in the mid to long term, i.e. rather a few years than a few month. Moreover, `ptbtest` is currently a pure spare-time project, so a maintainer/dev team would not get paid for their work (as is the case for `python-telegram-bot`).

As our goal is for the library to maintained by members of the PTB community, we would prefer to intervene as little as possible in the search for a new maintainer/dev team. We therefore created a group chat where you can get in contact with other interested people and exchange about your different insights on `ptbtest`, Python packaging and open source development. To join the chat, please contact [@BiboJoshi](https://t.me/BiboJoshi), [@Poolitzer](https://t.me/Poolitzer) or [@Hoppingturtles](https://t.me/Hoppingturtles) on Telegram.

Of course, we'd like to make sure for `ptbtest` to be in good hands. On the other hand, deciding who the right maintainer/dev team might be, is not easy. E.g. we are aware that there are some forks of `ptbtest`, but we are not familiar with the exact status of each fork. We therefore decided on the following procedure:

This search for a maintainer/dev team will stay open until the end of April. Until then, we ask the members of the group chat (see above) to elect one maintainer and optionally additional members of the development team. We expect the maintainer to be able to demonstrate experience with Python packaging, open source development and familiarity with `ptbtest`. If for example the elected person has published a non-trivial package on PyPi or is already a maintainer of another library (Python or other language) and uses `ptbtest` elaborately in as existing project or even has worked with the `ptbtest` source before, we can safely assume that these requirements are fulfilled. The cherry on the cake would be if the elected maintainer/dev team already submit some initial work on `ptbtest` until end of April.

We emphasize that we ask for *one* maintainer to be elected who we can grant the access rights and ownerships.

We are very looking forward to your involvement and hope that `ptbtest` will be continued.

Your PTB Developer Team

---

Original readme below

---

[![Build Status](https://travis-ci.org/Eldinnie/ptbtest.svg?branch=master)](https://travis-ci.org/Eldinnie/ptbtest) [![Documentation Status](https://readthedocs.org/projects/ptbtestsuite/badge/?version=master)](http://ptbtestsuite.readthedocs.io/en/master/?badge=master) [![Coverage Status](https://coveralls.io/repos/github/Eldinnie/ptbtest/badge.svg?branch=master)](https://coveralls.io/github/Eldinnie/ptbtest?branch=master)
[![PyPI](https://img.shields.io/pypi/v/ptbtest.svg)](https://pypi.python.org/pypi/ptbtest) [![PyPI](https://img.shields.io/pypi/pyversions/ptbtest.svg)](https://pypi.python.org/pypi/ptbtest) [![PyPI](https://img.shields.io/pypi/l/ptbtest.svg)](https://pypi.python.org/pypi/ptbtest)

# (In) compatibility
Unfortunately lately this testsuite has not been updated to any versions of python-telegram-bot higher than 6.0. Hopefully some time can be spent to update it soon.

# ptbtest
## a testsuite for [Python telegram bot](https://github.com/python-telegram-bot/python-telegram-bot/)

This library is meant for people wanting to write unittests for their python-telegram-bot driven bots.
The following things make this library attractive to create unittests
* Mockbot - A fake bot that does not contact telegram servers
* Works with the updater from telegram.ext
* Generatorclasses to easily create Users, Chats and Updates.

Read the [documentation](http://ptbtestsuite.readthedocs.io/en/master/?badge=master) for further reading and check out the examples.
