import time
from PyQt5.QtCore import (
    QThread,
)
from common import attach_common
from database_downloader import DatabaseDownload
from ai_list_memorize import MemorizeList
from ai_list_morpheme import MorphemeList
from ai_list_ngram import NgramList
from ai_list_none import NoneList
from ai_bot_memorize import MemorizeBot
from ai_bot_morpheme import MorphemeBot
from ai_bot_ngram import NgramBot
from ai_bot_none import NoneBot


@attach_common
class TalkBotThread(QThread):
    parent = None
    bot = None
    lister = None

    text_target = ''
    tokens_start_of_text = []
    tokens_of_text = []

    def run(self):
        self.start_database()
        self.update_bot_type()
        self.start_main_loop()

    def start_database(self):
        if self.config.ENABLED_DOWNLOAD:
            DatabaseDownload.remove_tempfiles()
            DatabaseDownload.set_url('')
            DatabaseDownload.do_download_html()
        else:
            DatabaseDownload.do_not_download_html()
        self.text_target = DatabaseDownload().get_outcome()

    def update_bot_type(self):
        parent = self.parent
        parent.is_bot_ready = False
        parent.show_bot_not_ready_msg()

        self.type_bot = parent.type_bot
        self.select_token_list()
        self.select_bot()

        parent.bot = self.bot
        parent.lister = self.lister
        parent.is_bot_ready = True
        parent.show_bot_ready_msg()
        self.output_bot_type()

    def output_bot_type(self):
        parent = self.parent
        msgs = (
            'TalkBot:',
            '        id: {}'.format(parent.type_bot),
            '       bot: {}'.format(parent.bot.__class__.__name__),
            '    lister: {}'.format(parent.lister.__class__.__name__),
            '    tokens: {}'.format(str(parent.lister.get_token_list())[:60]),
        )
        for msg in msgs:
            self.logger.w(msg)

    def select_token_list(self):
        if self.type_bot == 0:
            self.lister = NoneList(
                num_of_gram=self.config.DISABLE_NGRAM,
                text_target=self.text_target,
            )
            self.tokens_start_of_text = self.lister.get_starting_token_list()
            self.tokens_of_text = self.lister.get_token_list()
            return

        if self.type_bot == 1:
            self.lister = NgramList(
                num_of_gram=3,
                text_target=self.text_target,
            )
            self.tokens_start_of_text = self.lister.get_starting_token_list()
            self.tokens_of_text = self.lister.get_token_list()
            return

        if self.type_bot == 2:
            self.lister = MorphemeList(
                num_of_gram=self.config.DISABLE_NGRAM,
                text_target=self.text_target,
            )
            self.tokens_start_of_text = self.lister.get_starting_token_list()
            self.tokens_of_text = self.lister.get_token_list()
            return

        if self.type_bot == 3:
            self.lister = MemorizeList(
                num_of_gram=self.config.DISABLE_NGRAM,
                text_target=self.text_target,
            )
            self.tokens_start_of_text = self.lister.get_starting_token_list()
            self.tokens_of_text = self.lister.get_token_list()
            return

        err = self.type_bot
        raise Exception(err)

    def select_bot(self):
        if self.type_bot == 0:
            self.bot = NoneBot(
                starting_token_list=self.tokens_start_of_text,
                token_list=self.tokens_of_text,
            )
            return

        if self.type_bot == 1:
            self.bot = NgramBot(
                starting_token_list=self.tokens_start_of_text,
                token_list=self.tokens_of_text,
            )
            return

        if self.type_bot == 2:
            self.bot = MorphemeBot(
                starting_token_list=self.tokens_start_of_text,
                token_list=self.tokens_of_text,
            )
            return

        if self.type_bot == 3:
            self.bot = MemorizeBot(
                starting_token_list=self.tokens_start_of_text,
                token_list=self.tokens_of_text,
            )
            return

        err = self.type_bot
        raise Exception(err)

    def start_main_loop(self):
        parent = self.parent
        while True:
            time.sleep(0.2)

            if parent.is_app_close:
                break

            if parent.type_bot != self.type_bot:
                self.update_bot_type()
                continue

            parent.update_bot_msg_to_proper_latest_status()

        msg = 'Stopped the database thread!'
        self.logger.w(msg)


if __name__ == "__main__":
    from gui_talkbot import MainWindow
    TestClass = MainWindow

    import sys
    from PyQt5.QtWidgets import QApplication
    qapp = QApplication(sys.argv)
    window = TestClass()
    window.show()
    code = qapp.exec()
    sys.exit(code)
