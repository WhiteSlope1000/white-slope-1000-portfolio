import MeCab
from core_logger import Logging
logger = Logging(__name__, __file__).get_logger()


class Analyzer(object):
    options = (
        'mecabrc',   # デフォルト
        '-Ochasen',  # ChaSen 互換形式
        '-Owakati',  # 分かち書きのみを出力
        '-Oyomi',    # 読みのみを出力
        '-u C:/Python38/Lib/site-packages/MeCab/NEologd_20200910-u.dic',
    )
    logger = logger
    surfaces = []
    posids = []

    def __init__(self):
        self.tagger = MeCab.Tagger(self.options[-1])
        self.tagger.parse('')

    def show_data(self, msg):
        msg = self.tagger.parse(msg)
        self.logger.i(msg)

    def get_surfaces(self):
        return self.surfaces

    def get_posids(self):
        return self.posids

    def get_surfaces_and_posids(self, msg):
        surfaces = self.surfaces
        posids = self.posids
        surfaces_append = surfaces.append
        posids_append = posids.append

        def core(msg):
            node = self.tagger.parseToNode(msg)
            surfaces.clear()
            posids.clear()
            self._test_show_node_members(node)
            while node:
                self._test_show_node_info(node)
                surface = node.surface
                if surface == '':
                    node = node.next
                    continue

                posid = node.posid
                surfaces_append(surface)
                posids_append(posid)
                node = node.next
            return surfaces, posids

        self.get_surfaces_and_posids = core
        return core(msg)

    def _test_show_node_members(self, node):
        for member in dir(node):
            if member.startswith('_'):
                continue
            self.logger.i(member)

    def _test_show_node_info(self, node):
        self.logger.i('')
        self.logger.i(f'CSVで表記された素性情報: {node.feature}')
        self.logger.i(f'     形態素の文字列情報: {node.surface}')
        self.logger.i(f'           形態素の長さ: {node.length}')
        self.logger.i(f'   形態素に付与されたID: {node.id}')
        self.logger.i(f'           形態素の種類: {node.stat}')
        self.logger.i(f'         形態素の品詞ID: {node.posid}')
        self.logger.i(f'   文字フォーマット情報: {node.char_type}')
        self.logger.i(f'               周辺確率: {node.prob}')
        self.logger.i(f'         単語生起コスト: {node.wcost}')
        self.logger.i(f'             累計コスト: {node.cost}')


if __name__ == '__main__':
    msg = 'ｶﾞﾝは早期発見が出来ますか？'
    analyzer = Analyzer()
    surfaces, posids = analyzer.get_surfaces_and_posids(msg)
    logger.i('')
    logger.i(surfaces)
    logger.i(posids)
