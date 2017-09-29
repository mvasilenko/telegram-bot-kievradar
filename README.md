# Very basic Telegram chatbot example 


[![Build Status](https://travis-ci.org/mvasilenko/telegram-bot-kievradar.svg?branch=master)](https://travis-ci.org/mvasilenko/telegram-bot-kievradar)

[![CircleCI](https://circleci.com/gh/mvasilenko/telegram-bot-kievradar.svg?style=svg&circle-token=35dfc63b2632ad540bb1b7d565e942ba68e61e76)](https://circleci.com/gh/mvasilenko/telegram-bot-kievradar)

Currently this telegram bot requires environment variable TOKEN_BOT, which can be obtained during bot setup via telegram BotFather.
It echoes back input and supports two commands - radar map, and news from yandex.

Also features automatic build and deploy to AWS cloud ECR service as a container. Please see [.circleci/config.yml](https://github.com/mvasilenko/telegram-bot-kievradar/blob/master/.circleci/config.yml)

TBD: stateful, store mysql data in attached volume, tests.
