import os.path
import pprint
import collections
from common import attach_common
from database_downloader import DatabaseDownload


@attach_common
class ListInterface(object):
    text_target = ''
    msg_by_user = ''
    starting_token_list = []
    token_list = []

    def set_user_msg(self, msg_by_user):
        if len(msg_by_user) < 1:
            self.msg_by_user = msg_by_user
            return

        characters = self.get_trailing_characters()
        if not msg_by_user.endswith(characters):
            msg_by_user += '。'
            msg = f'added a trailing character: {msg_by_user}'
            self.logger.w(msg)
        self.msg_by_user = msg_by_user

    def get_user_msg(self):
        return self.msg_by_user

    def get_starting_token_list(self):
        return self.starting_token_list

    def get_token_list(self):
        return self.token_list

    def __init__(self, num_of_gram, text_target):
        self.check_num_of_gram(num_of_gram)
        self.check_text_target(text_target)
        self.make_starting_token_list()
        self.make_token_list()

    def check_num_of_gram(self, num_of_gram):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)

    def check_text_target(self, text_target):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)

    def make_start_token_list(self):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)

    def make_token_list(self):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)

    def make_type_name_list(self, txt):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)

    def make_morph_list(self, txt):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)

    def __call__(self, msg_by_user):
        self.set_user_msg(msg_by_user)
        self.update_starting_token_list()
        self.update_token_list()

    def update_starting_token_list(self):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)

    def update_token_list(self):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)

    def _test_generator(self):
        self._test_starting_token_list()
        self._test_token_list()
        self._test_token_counts()

    def _test_starting_token_list(self):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)

    def _test_token_list(self):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)

    def _test_token_counts(self):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)


class ListBase(object):
    def check_num_of_gram(self, num_of_gram):
        if num_of_gram == self.config.DISABLE_NGRAM:
            msg = '"num_of_gram" will not be used.'
            self.logger.w(msg)
            return False

        msg = f'num_of_gram: {num_of_gram}'
        self.logger.w(msg)
        self.num_of_gram = num_of_gram
        return True

    def check_text_target(self, text_target):
        if len(text_target) == 0:
            err = 'Target text is empty.'
            raise Exception(err)

        self.text_target = text_target


class ListTypeNgram(object):
    def make_starting_token_list(self):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)

    def make_token_list(self):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)

    def make_type_name_list(self, txt):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)

    def make_morph_list(self, txt):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)

    def update_starting_token_list(self):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)

    def update_token_list(self):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)


class ListTypeMorpheme(object):
    def make_starting_token_list(self):
        txt = self.text_target
        self.starting_token_list = self.make_type_name_list(txt)
        msg = len(self.starting_token_list)
        msg = 'starting token size: {}'.format(msg)
        self.logger.i(msg)

    def make_token_list(self):
        txt = self.text_target
        self.token_list = self.make_morph_list(txt)
        msg = len(self.token_list)
        msg = 'token size: {}'.format(msg)
        self.logger.i(msg)

    def make_type_name_list(self, txt):
        if 1:
            type_name = ''
            starting_token_list = []
            kana_list = ['い', 'う', 'だ']
            for i in range(len(txt) - 1):
                if self.sort_chr_type(txt[i]) == 2:
                    type_name += txt[i]
                    if self.sort_chr_type(txt[i]) != self.sort_chr_type(txt[i + 1]):
                        ii = 0
                        for kana in kana_list:
                            if kana != txt[i + 1]:
                                ii += 1
                                if ii == len(kana_list):
                                    starting_token_list.append(type_name)
                        type_name = ''
            return starting_token_list
        else:
            return self.make_pos_list(txt)

#    def make_pos_list(self, txt):
#        # pos --> PoS --> Part of Speech
#        # ToDo: Not based on PoS but Kanji, hirakana, katakana
#        data_noun = self.make_noun_list(txt)  # Pick up only nouns.
#        data_verb = self.make_verb_list(txt)  # Pick up only verbs.
#        data_adje = self.make_adje_list(txt)  # Pick up only adjectives.
#        results = data_noun + data_verb + data_adje
#        return results
#
#    def make_noun_list(self, txt):
#        matched = ''
#        starting_token_list = []
#        kana_list = ('を', 'は', 'が', 'に', 'へ', 'で', 'の')
#        for idx_a in range(len(txt) - 2):
#            idx_b = idx_a + 1
#            txt_a = txt[idx_a]
#            txt_b = txt[idx_b]
#            chr_type_a = self.sort_chr_type(txt_a)
#            chr_type_b = self.sort_chr_type(txt_b)
#            if chr_type_a != 2:
#                continue
#
#            matched += txt_a
#            if chr_type_a == chr_type_b:
#                continue
#
#            if txt_b.endswith(kana_list):
#                starting_token_list.append(matched)
#            matched = ''
#        return starting_token_list
#
#    def make_verb_list(self, txt):
#        starting_token_list = []
#        return starting_token_list
#
#    def make_adje_list(self, txt):
#        starting_token_list = []
#        return starting_token_list

    def make_morph_list(self, txt):
        morph = ''
        morph_list = []
        num_max = len(txt) - 1
        for i in range(num_max):
            morph += txt[i]
            if self.sort_chr_type(txt[i]) != self.sort_chr_type(txt[i + 1]):
                morph_list.append(morph)
                morph = ''
            if (i + 1) == num_max:
                morph += txt[i + 1]
                morph_list.append(morph)
        return morph_list

    def update_starting_token_list(self):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)

    def update_token_list(self):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)

    def _test_starting_token_list(self):
        tokens_start = self.get_starting_token_list()

        content = str(tokens_start)
        max = len(content)
        msg_fmt = 'starting tokens: {}'.format
        if max > 60:
            msg = msg_fmt(content[:60])
        else:
            msg = msg_fmt(content)
        self.logger.i(msg)

    def _test_token_list(self):
        tokens = self.get_token_list()

        content = str(tokens)
        max = len(content)
        msg_fmt = 'tokens: {}'.format
        if max > 60:
            msg = msg_fmt(content[:60])
        else:
            msg = msg_fmt(content)
        self.logger.i(msg)

    def _test_token_counts(self):
        tokens = self.get_token_list()
        path_name = '_morph_counts.txt'
        path = os.path.join(self.config.PATH_TMP, path_name)

        counts = collections.Counter(tokens)
        with open(path, mode='w', encoding='utf-8') as file:
            pprint.pprint(counts, stream=file)

        msg = 'Making counts file is Done!'
        self.logger.i(msg)


@attach_common
class TestRunnerCheckNgram(object):
    def __init__(self, TestClass):
        for num_of_gram in range(0, 6):
            self.logger.i('\n')
            try:
                if num_of_gram == 0:
                    DatabaseDownload.remove_tempfiles()
                    DatabaseDownload.set_url('')
                    DatabaseDownload.do_download_html()
                    text = DatabaseDownload().get_outcome()
                elif num_of_gram == 1:
                    DatabaseDownload.remove_tempfiles()
                    DatabaseDownload.set_url('')
                    DatabaseDownload.do_download_html()
                    text = DatabaseDownload().get_outcome()
                else:
                    DatabaseDownload.set_url('')
                    DatabaseDownload.do_not_download_html()
                    text = DatabaseDownload().get_outcome()

                inst = TestClass(
                    num_of_gram=num_of_gram,
                    text_target=text,
                )
                inst(msg_by_user='白い服を着ている私はおそらく元気だなぁ')
                inst._test_generator()
            except self.InvalidNumOfNgramError:
                msg = 'OK with Exceptions in NgramList Test Mode!'
                msg = 'num_of_gram: {}, {}'.format(num_of_gram, msg)
                self.logger.e(msg)
            except self.NoOverwrittenError:
                msg = 'Check if correct overriding is done!'
                msg = 'num_of_gram: {}, {}'.format(num_of_gram, msg)
                self.logger.e(msg)


@attach_common
class TestRunnerNoCheckNgram(object):
    def __init__(self, TestClass):
        self.logger.i('\n')
        DatabaseDownload.set_url('')
        DatabaseDownload.do_not_download_html()
        text = DatabaseDownload().get_outcome()

        inst = TestClass(
            num_of_gram=self.config.DISABLE_NGRAM,
            text_target=text,
        )
        inst(msg_by_user='白い服を着ている私はおそらく元気だなぁ')
        inst._test_generator()


if __name__ == '__main__':
    class TestA(ListTypeNgram, ListBase, ListInterface):
        pass

    class TestB(ListTypeMorpheme, ListBase, ListInterface):
        pass

    TestRunnerCheckNgram(TestA)
    TestRunnerNoCheckNgram(TestB)
