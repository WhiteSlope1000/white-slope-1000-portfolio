from ai_bot_common import (
    BotInterface,
    BotBase,
    BotTypeMorpheme,
    TestRunner,
)


class MemorizeBot(BotTypeMorpheme, BotBase, BotInterface):
    pass


if __name__ == '__main__':
    from ai_list_memorize import MemorizeList
    TestClassList = MemorizeList
    TestClassBot = MemorizeBot
    TestRunner(TestClassList, TestClassBot, num_of_gram=TestClassBot.config.DISABLE_NGRAM)
