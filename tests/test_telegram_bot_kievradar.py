import unittest

import telegram_bot_kievradar

class TestTelegramBotKievRadar(unittest.TestCase):

    def test_kiev_news_text(self):
        self.assertTrue(len(telegram_bot_kievradar.kiev_news_text()) > 0)

if __name__ == '__main__':
    unittest.main()
