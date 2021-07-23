import random
from common import attach_common


@attach_common
class BotInterface(object):
    starting_token_list = []
    token_list = []
    chr_start = ''
    sentence_new = ''

    def get_new_sentence(self):
        return self.sentence_new

    def __init__(self, starting_token_list, token_list):
        self.starting_token_list = starting_token_list
        self.token_list = token_list


class BotBase(object):
    def make_sentence(self, starting_token_list, token_list):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)


class BotTypeNgram(object):
    def make_sentence(self, starting_token_list, token_list):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)


class BotTypeMorpheme(object):
    def make_sentence(self, starting_token_list, token_list):
        self.starting_token_list = starting_token_list
        self.token_list = token_list
        self.setup_chr_start()
        self.make_sentence_core()
        return self.get_new_sentence()

    def setup_chr_start(self):
        tokens_start = self.starting_token_list
        num = len(tokens_start) - 1
        num = random.randint(0, num)
        self.chr_start = tokens_start[num]

    def make_sentence_core(self):
        token_list = self.token_list
        chr_start = self.chr_start
        sentence_new = ''
        sentence_new += chr_start

        characters = self.get_trailing_characters()
        chr_next = chr_start
        num_max = token_list.count(chr_next)
        for i in range(50):
            if chr_next.endswith(characters):
                break
            num_r = random.randint(0, num_max)
            for index, chr in enumerate(token_list):
                if chr == chr_next:
                    if index >= num_r:
                        break
            if index == len(token_list) - 1:
                chr_next = '。'
            else:
                chr_next = token_list[index + 1]
            sentence_new += chr_next

        self.sentence_new = sentence_new


class TalkBotTypeNgram(object):
    def make_sentence(self):
        pass


class TalkBotTypeMorpheme(object):
    def make_sentence(self):
        self.setup_chr_start()
        self.make_sentence_core()

    def setup_chr_start(self):
        tokens_start = self.starting_token_list
        num = len(tokens_start) - 1
        num = random.randint(0, num)
        self.chr_start = tokens_start[num]

    def make_sentence_core(self):
        token_list = self.token_list
        chr_start = self.chr_start
        sentence_new = ''
        sentence_new += chr_start

        chr_next = chr_start
        num_max = token_list.count(chr_next)
        for i in range(50):
            if chr_next == '。':
                break
            num_r = random.randint(0, num_max)
            for index, chr in enumerate(token_list):
                if chr == chr_next:
                    if index >= num_r:
                        break
            if index == len(token_list) - 1:
                chr_next = '。'
            else:
                chr_next = token_list[index + 1]
            sentence_new += chr_next

        self.sentence_new = sentence_new


@attach_common
class TestRunner(object):
    def __init__(self, TestClassList, TestClassBot, num_of_gram):
        self.logger.i('\n\n')
        msg = f'Start of testing: TargetTestClass: {TestClassList.__name__} {TestClassBot.__name__}'
        self.logger.i(msg)

        try:
            self.download_source_texts()
            self.test_starting_token_of_word_list(TestClassList, num_of_gram)
            self.test_token_list_of_word_list(TestClassList, num_of_gram)
            self.test_msg_by_user_of_word_list(TestClassList, num_of_gram)
            self.test_bot_with_word_list(TestClassBot, TestClassList, num_of_gram)
        except self.NoOverwrittenError:
            msg = 'check if correct overriding is done!'
            msg = 'num_of_gram: {} --> {}'.format(num_of_gram, msg)
            self.logger.e(msg)

        msg = 'End of testing:'
        self.logger.i(msg)

    def download_source_texts(self):
        from database_downloader import DatabaseDownload

        try:
            DatabaseDownload.set_url('')
            DatabaseDownload.do_not_download_html()
            text = DatabaseDownload().get_outcome()
        except (FileNotFoundError, self.AbortProgram):
            DatabaseDownload.remove_tempfiles()
            DatabaseDownload.set_url('')
            DatabaseDownload.do_download_html()
            text = DatabaseDownload().get_outcome()
        self.text_target = text

    def test_starting_token_of_word_list(self, TestClassList, num_of_gram):
        text_target = self.text_target
        lister = TestClassList(
            num_of_gram=num_of_gram,
            text_target=text_target,
        )
        lister.get_starting_token_list()

    def test_token_list_of_word_list(self, TestClassList, num_of_gram):
        text_target = self.text_target
        lister = TestClassList(
            num_of_gram=num_of_gram,
            text_target=text_target,
        )
        lister.get_token_list()

    def test_msg_by_user_of_word_list(self, TestClassList, num_of_gram):
        text_target = self.text_target
        lister = TestClassList(
            num_of_gram=num_of_gram,
            text_target=text_target,
        )
        lister(msg_by_user='白い服を着ている私はおそらく元気だなぁ')
        lister.get_user_msg()

    def test_bot_with_word_list(self, TestClassBot, TestClassList, num_of_gram):
        text_target = self.text_target
        lister = TestClassList(
            num_of_gram=num_of_gram,
            text_target=text_target,
        )

        bot = TestClassBot(
            starting_token_list=lister.get_starting_token_list(),
            token_list=lister.get_token_list(),
        )

        for i in range(10):
            msg_by_user = random.choice(self.config.MSGS_BOT_NONE)
            msg = f' msg_by_user: {msg_by_user}'
            self.logger.i(msg)

            lister(msg_by_user=msg_by_user)
            sentence_new = bot.make_sentence(
                starting_token_list=lister.get_starting_token_list(),
                token_list=lister.get_token_list(),
            )

            msg = f'sentence_new: {sentence_new}'
            self.logger.i(msg)
            self.logger.i('')


if __name__ == '__main__':
    from ai_list_common import (
        ListTypeNgram,
        ListTypeMorpheme,
        ListBase,
        ListInterface,
    )

    class ListClassA(ListTypeNgram, ListBase, ListInterface):
        pass

    class ListClassB(ListTypeMorpheme, ListBase, ListInterface):
        pass

    class BotClassA(BotTypeNgram, BotBase, BotInterface):
        pass

    class BotClassB(BotTypeMorpheme, BotBase, BotInterface):
        pass

    TestClassList = ListClassA
    TestClassBot = BotClassA
    TestRunner(TestClassList, TestClassBot, num_of_gram=TestClassBot.config.DISABLE_NGRAM)

    TestClassList = ListClassB
    TestClassBot = BotClassB
    TestRunner(TestClassList, TestClassBot, num_of_gram=TestClassBot.config.DISABLE_NGRAM)
