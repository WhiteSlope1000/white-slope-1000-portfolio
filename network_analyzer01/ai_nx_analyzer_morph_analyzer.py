import os.path
import MeCab
import re
from threading import Thread
from operator import itemgetter
from collections import defaultdict as DefaultDict
from collections import Counter
from core_full_half import ZenHan
from common import attach_common


class CoOccurrenceNetworkMorphAnalyzer(object):
    # Patterns for decide a line.
    words_delimiter = re.compile(r'[。「」！？　、]')
    words_delimiter = re.compile(r'[。「」！？　]')

    # Patterns for mecab output format.
    regexp_pos_1st = re.compile(r'^([^*^,]+)')
    regexp_pos_all = re.compile(r'^(.*?)[,*]{2,}[^*]+')

    mecab = None
    zenhan = None

    def setup_mecab(self):
        option = f'-u {self.config.PATH_TO_MECAB_USER_DICT}'
        self.mecab = MeCab.Tagger(option)

    def setup_part_of_speech_data(self):
        self.poses_white = tuple(data[1] for data in self.config.POSES_PARAM[1:])
        self.poses_black = (
            'BOS/EOS',
        )

        msg = 'valid part of speeches (POS):'
        self.logger.i(msg)
        for pos in self.poses_white:
            msg = f'  "{pos}"'
            self.logger.i(msg)

    def setup_full_half_length_counter(self):
        self.zenhan = ZenHan()

    def load_line_data(self):
        path = self.path_file_target
        lines = []
        lines_add = lines.extend
        split = self.words_delimiter.split
        with open(path, mode='r', encoding='utf-8') as file:
            for line in file.readlines():
                # line = line.replace('、', '')
                lines_add(split(line))
        self.lines = lines

    def start_morph_analysis(self):
        lines = self.lines

        poses_white = self.poses_white
        poses_black = self.poses_black
        regexp_pos_1st_match = self.regexp_pos_1st.match
        regexp_pos_all_match = self.regexp_pos_all.match
        parseToNode = self.mecab.parseToNode

        self.setup_vars_for_morph_analysis()
        edges = self.edges
        edges_count = self.edges_count
        nodeids_token = self.nodeids_token
        nodeids_count = self.nodeids_count
        nodeids_posid = self.nodeids_posid
        tokens_node = self.tokens_node
        poses_node = self.poses_node
        posids_mecab = self.posids_mecab

        token_id_new = 0
        token_id_old = -1
        token_id_crr = -1

        path = self.path_morph_file_black
        with open(path, mode='w', encoding='utf-8') as file:
            write = file.write
            for line in lines:
                node = parseToNode(line)
                token_id_old = -1
                while node:
                    feature = node.feature
                    match = regexp_pos_1st_match(feature)
                    if not match:
                        continue

                    surface = node.surface
                    surface_pos = match.group(1)
                    if surface_pos in poses_black or \
                       surface_pos not in poses_white:
                        write(feature + '\n')
                        node = node.next
                        continue

                    if surface not in nodeids_token.values():
                        posid = node.posid
                        tokens_node[surface] = token_id_new
                        nodeids_token[token_id_new] = surface
                        nodeids_count[token_id_new] = 1
                        nodeids_posid[token_id_new] = posid
                        poses_node[surface_pos].append(token_id_new)
                        token_id_crr = token_id_new
                        token_id_new += 1
                        if posid not in posids_mecab:
                            if match := regexp_pos_all_match(feature):
                                posids_mecab[posid] = match.group(1)
                    else:
                        token_id_crr = tokens_node[surface]
                        nodeids_count[token_id_crr] += 1

                    if token_id_old != -1 and \
                       token_id_crr != token_id_old:
                        edges.append((
                            min(token_id_old, token_id_crr),
                            max(token_id_old, token_id_crr),
                            # token_id_old,
                            # token_id_crr,
                        ))

                    token_id_old = token_id_crr
                    node = node.next

        self.edges = edges
        self.edges_count = edges_count(edges)
        self.nodeids_token = nodeids_token
        self.nodeids_count = nodeids_count
        self.nodeids_posid = nodeids_posid
        self.tokens_node = tokens_node
        self.poses_node = poses_node
        self.posids_mecab = posids_mecab

        self.edges_set_sorted = sorted(set(self.edges))

        self.threads.append(Thread(target=self.output_morph_info))
        self.threads.append(Thread(target=self.store_edges_to_file))
        self.threads.append(Thread(target=self.store_tokens_to_file))

    def setup_vars_for_morph_analysis(self):
        self.edges = []
        self.edges_count = Counter
        self.nodeids_token = DefaultDict(str)
        self.nodeids_count = DefaultDict(int)
        self.nodeids_posid = DefaultDict(int)
        self.tokens_node = DefaultDict(int)
        self.poses_node = DefaultDict(list)
        self.posids_mecab = DefaultDict(str)

        log = self.logger.i
        log('')
        log('        edges: Normal      list of [(nodeid_a, nodeid_b), ...]')
        log('  edges_count: Counter     dict of {(nodeid_a, nodeid_b): count, ...}')
        log('nodeids_token: DefaultDict dict of {nodeid: token, ...}')
        log('nodeids_count: DefaultDict dict of {nodeid: count, ...}')
        log('nodeids_posid: DefaultDict dict of {nodeid: posid, ...}')
        log('  tokens_node: DefaultDict dict of {token: nodeid, ...}')
        log('   poses_node: DefaultDict dict of {pos: [nodeid_a, nodeid_c, ...]}')
        log(' posids_mecab: Normal      dict of {posid_mecab: description_mecab, ...}')
        log('')
        log('        edges: [(2, 3), (3, 4), (4, 5), ...]')
        log('  edges_count: {(3, 8): 129, (2, 3): 49, ...}')
        log('nodeids_token: {0: "走れメロス", 1: "太宰治", 2: "メロス", ...}')
        log('nodeids_count: {0: 1, 1: 1, 2: 76, 3: 267, 4: 2, 5: 59, 6: 214, ...}')
        log('nodeids_posid: {0: 41, 1: 42, 2: 41, 3: 16, ...}')
        log('  tokens_node: {"走れメロス": 0, "太宰治": 1, "メロス": 2, ...}')
        log('   poses_node: {"名詞": [0, ...], "助詞": [450, ...], ...}')
        log(' posids_mecab: {41: "名詞,固有名詞,一般", ...}')
        log('')

    def output_morph_info(self):
        nodeids_token = self.nodeids_token
        nodeids_count = self.nodeids_count
        nodeids_posid = self.nodeids_posid
        posids_mecab = self.posids_mecab

        data = []
        for token_id, token in nodeids_token.items():
            data.append((
                nodeids_count[token_id],
                nodeids_posid[token_id],
                token,
            ))
        sorted_data = sorted(
            data,
            key=itemgetter(0, 1, 2),
            reverse=True,
        )

        num_max = 50
        len_max = 30
        get_real_hankaku_length = self.zenhan.get_real_hankaku_length

        path = self.path_morph_file_white
        with open(path, mode='w', encoding='utf-8') as file:
            msg_a = f'検出された有効なトークン: {" "}'
            msg_b = f'出現回数{" "*2}品詞ID{" "*2}品詞内訳{" "*24}文字列'
            file.write(msg_a + '\n')
            file.write(msg_b + '\n')
            self.logger.i(msg_a)
            self.logger.i(msg_b)

            for idx, data in enumerate(sorted_data):
                count = data[0]
                pos_id = data[1]
                pos = posids_mecab[pos_id].replace(',', ', ')
                token = data[2]
                len_dif = len_max - get_real_hankaku_length(pos)
                pos_dif = ' ' * len_dif
                pos = pos + pos_dif
                msg = f'{" "*4}{count:4d}{" "*6}{pos_id:2d}{" "*2}{pos}{" "*2}{token}'
                file.write(msg + '\n')
                if idx < num_max:
                    self.logger.i(msg)

    def store_edges_to_file(self):
        edges = self.edges_set_sorted
        path = self.path_morph_file_edges
        with open(path, mode='w', encoding='utf-8') as file:
            file.write('edges = [\n')
            for _e in edges:
                file.write(f'    {_e},\n')
            file.write(']\n')

    def store_tokens_to_file(self):
        nodeids_token = self.nodeids_token
        edges = self.edges_set_sorted
        path = self.path_morph_file_tokens
        with open(path, mode='w', encoding='utf-8') as file:
            file.write('tokens = [\n')
            for _e in edges:
                _t = (
                    nodeids_token[_e[0]],
                    nodeids_token[_e[1]],
                )
                file.write(f'    {_t},\n')
            file.write(']\n')


@attach_common
class TestClass(CoOccurrenceNetworkMorphAnalyzer):
    path_crr = os.path.dirname(__file__)
    threads = []

    def __init__(self):
        self.setup_path()
        self.setup_mecab()
        self.setup_part_of_speech_data()
        self.setup_full_half_length_counter()

        self.test_poses()

        self.load_line_data()
        self.start_morph_analysis()
        self.start_threads()

    def setup_path(self):
        if not self.config.NAME_FILE_TARGET.endswith('.txt'):
            err = 'Target filename shall be end with ".txt"'
            raise Exception(err)

        name_file = self.config.NAME_FILE_TARGET
        self.path_file_target = os.path.join(
            self.path_crr,
            name_file,
        )

        path = self.path_file_target
        self.path_morph_file_black = path.replace(
            name_file,
            name_file.replace('.txt', '_black.log'),
        )
        self.path_morph_file_white = path.replace(
            name_file,
            name_file.replace('.txt', '_white.log'),
        )
        self.path_morph_file_edges = path.replace(
            name_file,
            name_file.replace('.txt', '_edges.py'),
        )
        self.path_morph_file_tokens = path.replace(
            name_file,
            name_file.replace('.txt', '_tokens.py'),
        )

    def test_poses(self):
        msg = 'self.poses_white:'
        self.logger.i(msg)
        for _s in self.poses_white:
            self.logger.i(f'  "{_s}"')

        msg = 'self.poses_black:'
        self.logger.i(msg)
        for _s in self.poses_black:
            self.logger.i(f'  "{_s}"')

    def start_threads(self):
        if len(self.threads) == 0:
            return

        for thread in self.threads:
            thread.daemon = True
            thread.start()


if __name__ == '__main__':
    if 0:
        from ai_nx_analyzer import CoOccurrenceNetwork
        network = CoOccurrenceNetwork()
        network()
    else:
        instance = TestClass()
        instance.threads[0].join()
        instance.threads[1].join()
        instance.threads[2].join()
