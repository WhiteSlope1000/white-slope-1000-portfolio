import re
from common import attach_common


@attach_common
class CssForMainWindow(object):
    data_css = {}
    regexp = re.compile(r'^(.*?rgba.)\s*([0-9]+),\s*([0-9]+),\s*([0-9]+),\s*([0-9]+)(.*?)$')

    def get_all_css_data(self):
        data_css = self.data_css
        align_color_desc = self.align_color_desc
        for key, lines in self.data_css.items():
            lines = align_color_desc(lines)
            css = ''.join(lines)
            css = css.replace('    ', ' ')
            css = css.replace('{ ', ' {')
            data_css[key] = css
        return data_css

    def align_color_desc(self, lines):
        search = self.regexp.search

        def core(lines):
            lines_new = []
            append = lines_new.append
            for line in lines:
                match = search(line)
                if not match:
                    append(line)
                    continue
                group = match.group
                line = '{}{}, {}, {}, {}{}'.format(
                    group(1),
                    f'{group(2):>3s}',
                    f'{group(3):>3s}',
                    f'{group(4):>3s}',
                    f'{group(5):>3s}',
                    group(6),
                )
                append(line)
            return lines_new

        self.align_color_desc = core
        return core(lines)

    def _test_all_css_data(self):
        data_css = self.get_all_css_data()
        for key, val in data_css.items():
            msg = f'{key:24}: "{val}"'
            print(msg)

    def __init__(self):
        self.setup_style_sheets_for_bot_and_you_labels()
        self.setup_style_sheets_for_bot_type_buttons()
        self.setup_style_sheets_for_bot_exit_button()
        self.setup_style_sheets_for_user_input()
        self.setup_style_sheets_for_bg_image()

    def setup_style_sheets_for_bot_and_you_labels(self):
        css_bot_ready_ok = [
            'QLabel',
            '{',
            '    font-size: 32px;',
            '    color: rgba(0, 96, 0, 255);',
            '    background-color: rgba(240, 150, 150, 160);',
            '    border-radius: 8px;',
            '}',
        ]
        css_bot_ready_ng = [
            'QLabel',
            '{',
            '    font-size: 32px;',
            '    color: rgba(96, 0, 0, 255);',
            '    background-color: rgba(240, 150, 150,  80);',
            '    border-radius: 8px;',
            '}',
        ]
        css_bot = [
            'QLabel',
            '{',
            '    font-size: 32px;',
            '    color: black;',
            '    background-color: rgba(240, 150, 150, 160);',
            '    border-radius: 8px;',
            '}',
        ]
        css_you = [
            'QLabel',
            '{',
            '    font-size: 32px;',
            '    color: black;',
            '    background-color: rgba(140, 210, 240, 160);',
            '    border-radius: 8px;',
            '}',
        ]
        self.data_css["label_bot_ready_ok"] = css_bot_ready_ok
        self.data_css["label_bot_ready_ng"] = css_bot_ready_ng
        self.data_css["label_bot"] = css_bot
        self.data_css["label_you"] = css_you

        css_help = [
            'QLabel',
            '{',
            '    font-size: 24px;',
            '    color: black;',
            '    background-color: rgba(120, 240, 200, 160);',
            '    border-radius: 8px;',
            '}',
        ]
        self.data_css["label_help"] = css_help

        css_space = [
            'QLabel',
            '{',
            '   width: 96px;'
            '}',
        ]
        self.data_css["label_space"] = css_space

    def setup_style_sheets_for_bot_type_buttons(self):
        css_button_bot = [
            'QPushButton',
            '{',
            '    font-size: 24px;',
            '    font-weight: bold;',
            '    color: rgba(10, 10, 200, 255);',
            '    background-color: rgba(120, 120, 120, 196);',
            '    border: 4px solid rgba( 0, 0, 0, 64);',
            '    border-radius: 6px;',
            '    height: 50px;',
            '    width: 96px;',
            '}',
        ]
        css_button_bot_crr = [
            'QPushButton',
            '{',
            '    font-size: 24px;',
            '    font-weight: bold;',
            '    color: rgba(128, 128, 255, 255);',
            '    background-color: rgba(20, 20, 20, 196);',
            '    border: 4px solid rgba(0, 0, 255, 128);',
            '    border-radius: 6px;',
            '    height: 50px;',
            '    width: 96px;',
            '}',
        ]
        self.data_css["button_bot"] = css_button_bot
        self.data_css["button_bot_crr"] = css_button_bot_crr

    def setup_style_sheets_for_bot_exit_button(self):
        css_button_exit = [
            'QPushButton',
            '{',
            '    font-size: 24px;',
            '    font-weight: bold;',
            '    color: rgba(160, 50, 50, 255);',
            '    background-color: rgba(50, 50, 50, 230);',
            '    border: 4px solid rgba(60, 0, 60, 32);',
            '    border-radius: 6px;',
            '    height: 50px;',
            '    width: 96px;',
            '}',
        ]
        css_button_exit_on = [
            'QPushButton',
            '{',
            '    font-size: 24px;',
            '    font-weight: bold;',
            '    color: rgba(144, 10, 10, 255);',
            '    background-color: rgba(100, 100, 180, 196);',
            '    border: 4px solid rgba(60, 0, 60, 128);',
            '    border-radius: 6px;',
            '    height: 50px;',
            '    width: 96px;',
            '}',
        ]
        css_button_help = [
            'QPushButton',
            '{',
            '    font-size: 24px;',
            '    font-weight: bold;',
            '    color: rgba(250, 250, 250, 255);',
            '    background-color: rgba(50, 180, 50, 200);',
            '    border: 4px solid rgba(60, 0, 60, 32);',
            '    border-radius: 6px;',
            '    height: 50px;',
            '    width: 50px;',
            '}',
        ]
        self.data_css["button_exit"] = css_button_exit
        self.data_css["button_exit_on"] = css_button_exit_on
        self.data_css["button_help"] = css_button_help

    def setup_style_sheets_for_user_input(self):
        css_input_user = [
            'QLineEdit',
            '{',
            '    font-size: 24px;',
            '    font-weight: bold;',
            '    color: rgba(0, 64, 196, 255);',
            '    background-color: rgba(200, 200, 200, 196);',
            '    border: 4px solid rgba(100, 100, 100, 32);',
            '    border-radius: 6px;',
            '    height: 50px;',
            '    width: 96px;',
            '}',
        ]
        self.data_css["input_user"] = css_input_user

    def setup_style_sheets_for_bg_image(self):
        css_page_bg_img_00 = [
            '.QPage00#{}'.format(self.config.WIDGET_NAME_PAGE_00),
            '{',
            '    background-image: url({});'.format(self.config.PATH_IMG_BG_01),
            '    background-color: rgba(  0,   0,   0, 255);',
            '}',
        ]
        css_page_bg_img_01 = [
            '.QPage01#{}'.format(self.config.WIDGET_NAME_PAGE_01),
            '{',
            '    background-image: url({});'.format(self.config.PATH_IMG_BG_02),
            '    background-color: rgba(  0,   0,   0, 255);',
            '}',
        ]
        css_page_bg_filter = [
            'QWidget#{}'.format(self.config.WIDGET_NAME_PAGE_BG_FILTER),
            '{',
            '    background-color: rgba(  0,   0,   0, 128);',
            '}',
        ]
        self.data_css["page_bg_img_00"] = css_page_bg_img_00
        self.data_css["page_bg_img_01"] = css_page_bg_img_01
        self.data_css["page_bg_filter"] = css_page_bg_filter


if __name__ == '__main__':
    TestClass = CssForMainWindow
    inst = TestClass()
    inst._test_all_css_data()
