from ai_bot_common import (
    BotInterface,
    BotBase,
    BotTypeMorpheme,
    TestRunner,
)


class MorphemeBot(BotTypeMorpheme, BotBase, BotInterface):
    pass


if __name__ == '__main__':
    from ai_list_morpheme import MorphemeList
    TestClassList = MorphemeList
    TestClassBot = MorphemeBot
    TestRunner(TestClassList, TestClassBot, num_of_gram=TestClassBot.config.DISABLE_NGRAM)
