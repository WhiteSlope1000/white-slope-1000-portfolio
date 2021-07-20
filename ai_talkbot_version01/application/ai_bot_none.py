from itertools import cycle
from ai_bot_common import (
    BotInterface,
    BotBase,
    BotTypeNgram,
    TestRunner,
)


class NoneBot(BotTypeNgram, BotBase, BotInterface):
    def make_sentence(self, starting_token_list, token_list):
        try:
            self.sentences_new
        except AttributeError:
            self.sentences_new = self.token_list[:]
            self.sentences_new = cycle(self.sentences_new)
        finally:
            self.sentence_new = next(self.sentences_new)
        return self.get_new_sentence()


if __name__ == '__main__':
    from ai_list_none import NoneList
    TestClassList = NoneList
    TestClassBot = NoneBot
    TestRunner(TestClassList, TestClassBot, num_of_gram=TestClassBot.config.DISABLE_NGRAM)
