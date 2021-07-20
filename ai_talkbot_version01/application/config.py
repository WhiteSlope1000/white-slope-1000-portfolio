import os.path
from core_const import Const


class AiConfig(Const):
    DIRNAME_SE = 'sounds'
    DIRNAME_TMP = 'temp'
    DIRNAME_TXT = 'texts'
    DIRNAME_URL = 'urls'
    DIRNAME_IMAGE = 'images'

    FILENAME_JSON = 'config.json'
    FILENAME_IMAGE_BG_00 = 'tsuyu.png'
    FILENAME_IMAGE_BG_01 = 'spring01.png'
    FILENAME_IMAGE_BG_02 = 'spring02.png'

    FILENAME_SE_BUTTON = 'se_button_clicked.wav'
    FILENAME_SE_START = 'se_start_app.wav'
    FILENAME_SE_KEY = 'se_pressed_key.wav'

    PATH_CRR = os.path.dirname(__file__)
    PATH_SE = os.path.join(PATH_CRR, DIRNAME_SE)
    PATH_TMP = os.path.join(PATH_CRR, DIRNAME_TMP)
    PATH_TXT = os.path.join(PATH_CRR, DIRNAME_TXT)
    PATH_URL = os.path.join(PATH_CRR, DIRNAME_URL)
    PATH_JSON = os.path.join(PATH_CRR, FILENAME_JSON)
    PATH_SE_BUTTON = os.path.join(PATH_SE, FILENAME_SE_BUTTON).replace('\\', '/')
    PATH_SE_START = os.path.join(PATH_SE, FILENAME_SE_START).replace('\\', '/')
    PATH_SE_KEY = os.path.join(PATH_SE, FILENAME_SE_KEY).replace('\\', '/')
    PATH_IMG_BG_00 = os.path.join(PATH_CRR, DIRNAME_IMAGE, FILENAME_IMAGE_BG_00).replace('\\', '/')
    PATH_IMG_BG_01 = os.path.join(PATH_CRR, DIRNAME_IMAGE, FILENAME_IMAGE_BG_01).replace('\\', '/')
    PATH_IMG_BG_02 = os.path.join(PATH_CRR, DIRNAME_IMAGE, FILENAME_IMAGE_BG_02).replace('\\', '/')

    TYPES_BOT = {
        0: "No Bot",
        1: "3-Gram",
        2: "Morpheme",
        3: "Memorize",
    }
    TYPE_BOT = 3

    MSGS_BOT_NONE = [
        'え？',
        '私 ...',
        '日本語でお願いします。',
        '本日はいいお天気ですね。',
        'すみません、よくわかりません。',
        '白い服を着ている私はおそらく元気だなぁ。',
    ]
    KEYWORDS_NGRAM = [
        ('おれ', '俺'),
        ('わたし', '私'),
        ('きみ', '君'),
        ('オレ', '俺'),
        ('ワタシ', '私'),
        ('キミ', '君'),
        ('あなた', '貴方'),
        ('おまえ', 'お前'),
        ('きさま', '貴様'),
        ('アナタ', '貴方'),
        ('オマエ', 'お前'),
        ('キサマ', '貴様'),
    ]

    ENABLED_SE = True
    ENABLED_DOWNLOAD = True
    DISABLE_NGRAM = -1  # a number of N-gram. "-1" means "disable".

    WINDOW_TITLE = 'AI Bot Ver.1'
    WINDOW_W_MIN = 640
    WINDOW_H_MIN = 480

    INTERVAL_MSG_SPEED = 16  # [msec]
    INTERVAL_APP_CLOSE = 50  # [msec]
    TIMEOUT_APP_CLOSE = 30  # [times] --> INTERVAL_APP_CLOSE * TIMEOUT_APP_CLOSE [msec]

    WIDGET_NAME_PAGE_00 = 'Page00'
    WIDGET_NAME_PAGE_01 = 'Page01'
    WIDGET_NAME_PAGE_BG_FILTER = 'PageBgFilter'


if __name__ == '__main__':
    config = AiConfig()
    try:
        config.WINDOW_H_MIN = 0
    except config.ConstError:
        err = 'ConstError: OK because of test mode.'
        print(err)

    try:
        config.WINDOW_HOGE = 0
    except config.ConstError:
        err = 'ConstError: OK because of test mode.'
        print(err)
