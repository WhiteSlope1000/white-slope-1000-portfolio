import matplotlib.pyplot as pyplot
from core_exception import ConstError
from core_const import Const


class Config(Const):
    NAME_FILE_TARGET = 'ai_00_meros.txt'

    TITLE = '共起 ネットワーク アナライザ'
    LABEL_NODE = 'ノート数'
    LABEL_EDGE = 'エッジ数'
    LABEL_IBOX = 'フィルタ (Insertで起動)'
    LABEL_BUTTON = '更新'

    THRESHOLD_NODE = 1
    THRESHOLD_EDGE = 1
    THRESHOLD_WORD = ''
    THRESHOLD_WORD = 'メロス セリヌンティウス 友 私'
    THRESHOLD_WORD = '私'

    FONT = 'MS Gothic'
    PATH_TO_MECAB_USER_DICT = 'C:/Users/chizu/PycharmProjects/pythonProject/venv/GitHub/NEologd/NEologd.20200910-u.dic'

    FIG_SIZE_W = 10
    FIG_SIZE_H = 8
    FIG_SIZE = (
        FIG_SIZE_W,
        FIG_SIZE_H,
    )

    SIZE_MAX_NODE = 3600
    SIZE_MAX_EDGE = 18

    BG_COL_GRAPH = (0.80, 0.80, 0.70)
    BG_COL_FRAME = (0.40, 0.40, 0.35)
    BG_COL_LIGHT = (0.8, 0.8, 0.8)
    BG_COL_DARK = (0.1, 0.1, 0.1)

    FG_COL_NODE_LABEL = (1.0, 1.0, 1.0, 0.9)
    FG_COL_EDGE_LABEL = (1.0, 1.0, 1.0, 0.9)
    FG_COL_IBOX_LABEL = (1.0, 1.0, 1.0, 0.9)

    BG_COL_NODE_LABEL = (0.1, 0.1, 0.1, 0.8)
    BG_COL_EDGE_LABEL = (0.1, 0.1, 0.1, 0.7)
    BG_COL_IBOX_LABEL = (0.1, 0.1, 0.1, 0.6)

    BG_COL_NODE_AX = (0.0, 0.8, 0.8, 0.3)
    BG_COL_EDGE_AX = (0.0, 0.8, 0.8, 0.2)
    BG_COL_IBOX_AX = (0.0, 0.8, 0.8, 0.1)
    BG_COL_CHECKB_AX = (0.4, 0.4, 0.4, 1.0)
    BG_COL_BUTTON_AX = (0.0, 0.0, 0.0, 1.0)
    BG_COL_BUTTON_SPACE = (0.0, 0.8, 0.8, 0.3)

    BG_COL_NODE_VLINE = (0.0, 0.8, 0.8, 0.6)
    BG_COL_EDGE_VLINE = (0.0, 0.8, 0.8, 0.5)

    BG_COL_IBOX_SPACE = (0.0, 1.0, 1.0, 0.2)
    BG_COL_IBOX_HOVER = (1.0, 0.5, 0.2, 0.3)
    BG_COL_BUTTON_HOVER = (1.0, 0.5, 0.2, 0.3)

    BG_COL_NODE_POLY = (0.0, 0.0, 1.0, 0.8)
    BG_COL_EDGE_POLY = (0.0, 0.0, 1.0, 0.7)
    BG_COL_IBOX_POLY = (0.0, 0.8, 0.8, 0.1)

    FG_COL_IBOX_DISP = (0.5, 0.0, 0.0, 1.0)

    # Select a color from examples. --> https://matplotlib.org/examples/color/named_colors.html
    # ToDo: Setting pyplot.cm here does not work for now.
    POSES_PARAM = (
        [0, '全切替', 'black',         pyplot.cm.OrRd],  # NOQA: E241
        [1, '助詞',   'darkgreen',     pyplot.cm.OrRd],  # NOQA: E241
        [1, '助動詞', 'white',         pyplot.cm.OrRd],  # NOQA: E241
        [1, '記号',   'yellow',        pyplot.cm.OrRd],  # NOQA: E241
        [1, '感動詞', 'hotpink',       pyplot.cm.OrRd],  # NOQA: E241
        [1, '接頭詞', 'pink',          pyplot.cm.OrRd],  # NOQA: E241
        [1, '接続詞', 'darkred',       pyplot.cm.OrRd],  # NOQA: E241
        [1, '連体詞', 'indigo',        pyplot.cm.OrRd],  # NOQA: E241
        [1, '副詞',   'navy',          pyplot.cm.OrRd],  # NOQA: E241
        [1, '動詞',   'yellowgreen',   pyplot.cm.OrRd],  # NOQA: E241
        [1, '形容詞', 'tomato',        pyplot.cm.OrRd],  # NOQA: E241
        [1, '名詞',   'orange',        pyplot.cm.OrRd],  # NOQA: E241
    )


if __name__ == '__main__':
    if 0:
        from ai_nx_analyzer import CoOccurrenceNetwork
        network = CoOccurrenceNetwork()
        network()
    else:
        config = Config()
        try:
            config.TITLE = 0
        except ConstError:
            err = 'ConstError: OK because of test mode.'
            print(err)

        try:
            config.FONT = 0
        except ConstError:
            err = 'ConstError: OK because of test mode.'
            print(err)
