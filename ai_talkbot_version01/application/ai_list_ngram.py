import os
import pprint
import random
import collections
from ai_list_common import (
    ListInterface,
    ListBase,
    ListTypeNgram,
    TestRunnerCheckNgram,
)


class NgramList(ListTypeNgram, ListBase, ListInterface):
    def check_num_of_gram(self, num_of_gram):
        if super().check_num_of_gram(num_of_gram):
            return

        if num_of_gram < 1:
            err = f'num_of_gram: {num_of_gram}'
            raise self.InvalidNumOfNgramError(err)

    def make_starting_token_list(self):
        keywords = self.config.KEYWORDS_NGRAM[:]
        random.shuffle(keywords)
        self.starting_token_list = [keywords[0][1]]

    def make_token_list(self):
        txt = self.text_target

        ngram_list = []
        num_max = len(txt) - (self.num_of_gram - 1)
        for i in range(num_max):
            sta = i
            end = i + self.num_of_gram
            ngram_list.append(txt[sta:end])

        self.token_list = ngram_list
        msg = 'list_size: {}'.format(len(ngram_list))
        self.logger.i(msg)

    def make_type_name_list(self, txt):
        pass

    def make_morph_list(self, txt):
        pass

    def update_starting_token_list(self):
        pass

    def update_token_list(self):
        pass

    def _test_starting_token_list(self):
        tokens_start = self.get_starting_token_list()

        max = len(tokens_start) - 1
        msg_fmt = 'start chrs: {}'.format
        if max > 10:
            msg = msg_fmt(tokens_start[0:10])
        else:
            msg = msg_fmt(tokens_start)
        self.logger.i(msg)

    def _test_token_list(self):
        tokens = self.get_token_list()

        max = len(tokens)
        msg_fmt = 'ngram list: {}'.format
        if max > 10:
            msg = msg_fmt(tokens[0:10])
        else:
            msg = msg_fmt(tokens)
        self.logger.i(msg)

    def _test_token_counts(self):
        tokens = self.get_token_list()
        path_name = '_gram_counts.txt'
        path = os.path.join(self.config.PATH_TMP, path_name)

        if self.num_of_gram == 1:
            with open(path, mode='w', encoding='utf-8') as file:
                file

        counts = collections.Counter(tokens)
        with open(path, mode='a', encoding='utf-8') as file:
            pprint.pprint(counts, stream=file)

        msg = 'Making counts file is Done!'
        self.logger.i(msg)


if __name__ == '__main__':
    TestRunnerCheckNgram(NgramList)
