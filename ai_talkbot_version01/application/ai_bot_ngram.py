import random
from ai_bot_common import (
    BotInterface,
    BotBase,
    BotTypeNgram,
    TestRunner,
)


class NgramBot(BotTypeNgram, BotBase, BotInterface):
    def make_sentence(self, starting_token_list, token_list):
        keywords = self.config.KEYWORDS_NGRAM[:]
        random.shuffle(keywords)
        try:
            self.sentences_new
        except AttributeError:
            for keywords in self.config.KEYWORDS_NGRAM:
                keyword = keywords[0][0]
                sentences = self.make_sentence_core(keyword)
                if len(sentences) != 0:
                    break
                msg = f'Could not find a keyword: {keyword}'
                self.logger.w(msg)
            else:
                msg = 'Failed to find keywords. Switch to the none type!'
                self.logger.w(msg)
                sentences = self.config.MSGS_BOT_NONE[:]
            self.sentences_new = sentences
        finally:
            self.sentence_new = random.choice(self.sentences_new)
        return self.get_new_sentence()

    def make_sentence_core(self, keyword):
        chr_start = self.starting_token_list[0]
        token_list = self.token_list
        keyword_num = len(keyword)

        subject_words = []
        for word in token_list:
            if word[0:keyword_num] == keyword:
                subject_words.append(word)
        subject_words_sorted = list(dict.fromkeys(subject_words))

        sentence_new = ''
        sentences_new = []
        for subject in subject_words_sorted:
            sentence_new = subject
            for word in token_list:
                idx = len(sentence_new) - 1
                if sentence_new[idx] == word[0]:
                    word_end = len(word)
                    if '。' in word[0:word_end]:
                        period_index = word.index('。') + 1
                        sentence_new += word[1:period_index]
                        break
                    else:
                        sentence_new += word[1:word_end]
            sentence_new = '{}{}'.format(chr_start, sentence_new[2:])
            sentences_new.append(sentence_new)
        return sentences_new


if __name__ == '__main__':
    from ai_list_ngram import NgramList
    TestClassList = NgramList
    TestClassBot = NgramBot
    TestRunner(TestClassList, TestClassBot, num_of_gram=3)
