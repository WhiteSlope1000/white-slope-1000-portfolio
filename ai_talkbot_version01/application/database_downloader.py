import os
import re
import urllib.parse
import urllib.request
from common import attach_common


@attach_common
class DatabaseDownloadInterface(object):
    filename_html = '_source.html'
    filename_source = '_source.txt'

    url_target = ''
    txt_outcome = ''

    @classmethod
    def set_url(cls, url=''):
        if url != '':
            cls.url_target = url
            cls.logger.i(cls.url_target)
            return

        # For testing.
        list_for_testing = [
            'https://www.aozora.gr.jp/cards/000148/files/752_14964.html',       # 坊っちゃん    夏目漱石
            'https://www.aozora.gr.jp/cards/000081/files/473_42318.html',       # よだかの星    宮沢賢治
            'https://www.aozora.gr.jp/cards/000009/files/50713_68371.html',     # 踊る人形      アーサー・コナン・ドイル
        ]
        cls.url_target = list_for_testing[0]
        cls.logger.i(cls.url_target)

    @classmethod
    def remove_tempfiles(cls):
        os.makedirs(cls.config.PATH_TMP, exist_ok=True)
        os.makedirs(cls.config.PATH_TXT, exist_ok=True)

        cls.setup_paths()
        if os.path.exists(cls.path_html):
            os.remove(cls.path_html)
        if os.path.exists(cls.path_source):
            os.remove(cls.path_source)

    @classmethod
    def setup_paths(cls):
        try:
            cls.path_html
        except AttributeError:
            cls.path_html = os.path.join(cls.config.PATH_TMP, cls.filename_html)
            cls.path_source = os.path.join(cls.config.PATH_TMP, cls.filename_source)

    @classmethod
    def remove_tempfiles(cls):
        os.makedirs(cls.config.PATH_TMP, exist_ok=True)

        cls.setup_paths()
        if os.path.exists(cls.path_html):
            os.remove(cls.path_html)
        if os.path.exists(cls.path_source):
            os.remove(cls.path_source)

    @classmethod
    def setup_paths(cls):
        try:
            cls.path_html
        except AttributeError:
            cls.path_html = os.path.join(cls.config.PATH_TMP, cls.filename_html)
            cls.path_source = os.path.join(cls.config.PATH_TMP, cls.filename_source)

    @classmethod
    def do_download_html(cls):
        cls.setup_paths()
        cls.is_downloading_html = True
        msg_fmt = 'is_downloading_html: {}'.format
        msg = msg_fmt(cls.is_downloading_html)
        cls.logger.w(msg)

    @classmethod
    def do_not_download_html(cls):
        cls.setup_paths()
        cls.is_downloading_html = False
        msg_fmt = 'is_downloading_html: {}'.format
        msg = msg_fmt(cls.is_downloading_html)
        cls.logger.w(msg)

    def get_outcome(self):
        self.store_outcome()
        return self.txt_outcome

    def store_outcome(self):
        name = self.url_target.split('/')[-1]
        name = name.replace('.html', '.txt')
        path = os.path.join(
            self.config.PATH_TXT,
            name,
        )
        with open(path, mode='w', encoding='utf-8') as file:
            file.write(self.txt_outcome)


class DatabaseDownload(DatabaseDownloadInterface):
    txt_html = ''

    def __init__(self):
        self.check_download_flag()
        self.get_html()
        self.parse_html_to_text()
        self.store_text_to_file()
        self.eliminate_unwanted_text()

    def check_download_flag(self):
        try:
            self.is_downloading_html
        except AttributeError():
            err = 'Need to call do_download_html() or do_not_download_html() once.'
            self.logger.e(err)
            raise self.AbortProgram()

    def get_html(self):
        if not self.is_downloading_html:
            return

        url = self.url_target
        html = urllib.request.urlopen(url)
        html_data = html.read()
        html.close()

        path = self.path_html
        with open(path, mode='wb') as file:
            file.write(html_data)

    def parse_html_to_text(self):
        path = self.path_html
        try:
            txt_html = ''
            with open(path, mode='r', encoding='shift_jis') as file:
                lines_html = file.readlines()
                for line in lines_html:
                    if line.startswith('　　'):
                        continue
                    if line.startswith('「'):
                        txt_html += line
                        continue
                    if line.startswith('　'):
                        txt_html += line
                        continue
                self.txt_html = txt_html
        except FileNotFoundError:
            err = 'Need to download html file.'
            err += 'is_downloading_html: {}'.format(self.is_downloading_html)
            self.logger.e(err)
            raise self.AbortProgram()

    def store_text_to_file(self):
        path = self.path_source
        txt = self.txt_html
        with open(path, mode='w', encoding='utf-8') as file:
            file.write(txt)

    def eliminate_unwanted_text(self):
        txt = self.txt_html
        msg = f'txt_html - old: {len(txt)}'
        self.logger.i(msg)

        txt = re.sub(r'\<[^<^>]+\>', '', txt)
        txt = re.sub(r'[\r\n\t\s]+', '', txt)
        txt = re.sub(r'（[ぁ-んァ-ン]+）', '', txt)
        txt = re.sub(r'底本：[^：]+', '', txt)
        txt = txt.replace('」', '  ')
        txt = txt.replace('「', '  ')

        msg = f'txt_html - new: {len(txt)}'
        self.logger.i(msg)

        msg = f'   num of text: {len(txt)}'
        self.logger.i(msg)
        self.txt_outcome = txt

    def _test_download_result(self):
        test_result = self.get_outcome()
        max = len(test_result)
        if max > 100:
            self.logger.i(test_result[0:100])
        else:
            self.logger.i(test_result)


@attach_common
class TestRunner(object):
    def __init__(self, TestClass):
        self.setup_test_confitions(TestClass)
        self.do_case_download_with_wrong_process(TestClass)
        self.test_case_do_download(TestClass)
        self.test_case_do_not_download(TestClass)

    def setup_test_confitions(self, TestClass):
        TestClass.set_url('')
        TestClass.remove_tempfiles()
        TestClass.do_not_download_html()

    def do_case_download_with_wrong_process(self, TestClass):
        try:
            TestClass()
        except self.AbortProgram:
            msg = 'Test OK: Aborted program.'
            self.logger.w(msg)
            self.logger.i('')

    def test_case_do_download(self, TestClass):
        TestClass.do_download_html()
        inst = TestClass()
        inst._test_download_result()
        msg = 'Test OK: Downloaded data.'
        self.logger.w(msg)
        self.logger.i('')

    def test_case_do_not_download(self, TestClass):
        TestClass.do_not_download_html()
        inst = TestClass()
        inst._test_download_result()
        msg = 'Test OK: Reused tempfiles.'
        self.logger.w(msg)
        self.logger.i('')


if __name__ == '__main__':
    TestClass = DatabaseDownload
    TestRunner(TestClass)
