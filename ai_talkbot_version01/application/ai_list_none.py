import os
import pprint
import collections
from ai_list_common import (
    ListInterface,
    ListBase,
    ListTypeNgram,
    TestRunnerNoCheckNgram,
)


class NoneList(ListTypeNgram, ListBase, ListInterface):
    def check_text_target(self, text_target):
        pass

    def make_starting_token_list(self):
        pass

    def make_token_list(self):
        self.token_list = self.config.MSGS_BOT_NONE

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
        msg = 'start chrs: {}'.format(tokens_start)
        self.logger.i(msg)

    def _test_token_list(self):
        tokens = self.get_token_list()

        msg = 'tokens: {}'.format(tokens)
        self.logger.i(msg)

    def _test_token_counts(self):
        tokens = self.get_token_list()
        path_name = '_none_counts.txt'
        path = os.path.join(self.config.PATH_TMP, path_name)

        counts = collections.Counter(tokens)
        with open(path, mode='w', encoding='utf-8') as file:
            pprint.pprint(counts, stream=file)

        msg = 'Making counts file is Done!'
        self.logger.i(msg)


if __name__ == '__main__':
    TestRunnerNoCheckNgram(NoneList)
