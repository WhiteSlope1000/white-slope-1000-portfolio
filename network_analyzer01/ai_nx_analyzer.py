import os.path
import matplotlib.pyplot as pyplot
import matplotlib
import networkx as nx
import copy
from ai_nx_analyzer_morph_analyzer import CoOccurrenceNetworkMorphAnalyzer
from ai_nx_analyzer_widget import CoOccurrenceNetworkWidget
from common import attach_common


class CoOccurrenceNetworkBase(object):
    path_crr = os.path.dirname(__file__)

    threads = []
    graphs = []
    fig = None
    ax = None

    is_1st_time = True
    is_1st_time_kivy = True
    status_onoff_all = False

    def __init__(self):
        self.setup_path()
        self.setup_matplotlib()
        self.setup_mecab()
        self.setup_part_of_speech_data()
        self.setup_full_half_length_counter()

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

    def setup_matplotlib(self):
        matplotlib.rcParams['font.family'] = self.config.FONT
        font = dict(family=self.config.FONT)
        matplotlib.rc('font', **font)

    def setup_mecab(self):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)

    def setup_part_of_speech_data(self):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)

    def setup_full_half_length_counter(self):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)

    def __call__(self):
        self.load_line_data()
        self.start_morph_analysis()
        self.start_threads()
        self.setup_thresholds()
        self.setup_graph()

    def load_line_data(self):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)

    def start_morph_analysis(self):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)

    def start_threads(self):
        if len(self.threads) == 0:
            return

        for thread in self.threads:
            thread.daemon = True
            thread.start()

    def setup_thresholds(self):
        self.threshold_node = self.config.THRESHOLD_NODE
        self.threshold_edge = self.config.THRESHOLD_EDGE
        self.threshold_word = self.config.THRESHOLD_WORD

    def setup_graph(self):
        self.make_graph_data()
        self.apply_graph_to_networkx()
        self.apply_widgets_to_graph()
        self.is_1st_time = False
        manager = pyplot.get_current_fig_manager()
        manager.window.showMaximized()
        pyplot.show()
        pyplot.ion()

    def make_graph_data(self):
        nodeids_count = self.nodeids_count
        edges_count = self.edges_count
        nodeids_token = self.nodeids_token
        poses_node = self.poses_node
        edges = self.edges
        graphs = self.graphs
        graph = None

        if len(graphs) == 0:
            msg_nodes = f'nodeids_token[0]: {nodeids_token[0]}'
            msg_edges = f'edges[0]: {edges[0]}'
            self.logger.i(msg_nodes)
            self.logger.i(msg_edges)

            # Networkxに格納
            nodes_params = [
                (
                    idx,
                    {
                        'count': nodeids_count[idx],
                        'token': token,
                        'pos': poses_node[idx],
                    },
                )
                for idx, token in nodeids_token.items()
            ]
            edges_params = [
                (
                    idx_s,
                    idx_e,
                    {
                        'count': edges_count[(idx_s, idx_e)],
                    },
                )
                for idx_s, idx_e in edges
            ]
            graph = nx.Graph()
            # graph = nx.OrderedGraph()
            # graph = nx.MultiGraph()
            # graph = nx.DiGraph()
            # graph = nx.OrderedDiGraph()
            graph.number_of_nodes()
            graph.add_nodes_from(nodes_params)
            graph.add_edges_from(edges_params)
        else:
            if len(graphs) < 1:
                err = f'Invalid a number of graphs data: {len(graphs)}'
                raise Exception(err)
            graph = graphs[0]

        graphs.clear()
        graphs.append(graph)

        # Node・Edgeでの剪定
        # 破壊的操作のため各段階でgraphインスタンスを複製しバックアップを取っている
        # ここでの操作でグラフに表示する内容選択を行う
        self.filter_out_wanted_nodes_and_edges(graphs)

        # 最終結果
        graph_final = graphs[-1]
        locations = nx.layout.spring_layout(graph_final, k=0.6, seed=10)  # 2次元平面の座標決定
        labels = {id: nodeids_token[id] for id in locations.keys()}
        nodes_size = self.calc_node_sizes(nodeids_count, locations)

        nodes_data = []
        nodes = graph_final.nodes()
        for is_selected, pos, color_pos, color_edge in self.config.POSES_PARAM[1:]:
            if not is_selected:
                continue
            nodes_n, sizes_n = self.get_data_by_word_pos(nodes, poses_node, nodes_size, pos)
            nodes_data.append((
                nodes_n,
                sizes_n,
                color_pos,
                color_edge,
            ))

        self.graph = graph_final
        self.locations = locations
        self.labels = labels
        self.nodes_data = nodes_data

        edges = graph_final.edges()
        _a = 1
        _c = 255
        _w = self.config.SIZE_MAX_EDGE
        self.edge_alphas = [min(edges_count[e] + 0, _a) for e in edges]
        self.edge_colors = [min(edges_count[e] + 0, _c) for e in edges]
        self.edge_widths = [min(int((edges_count[e] + 1) * 0.5), _w) for e in edges]

    def filter_out_wanted_nodes_and_edges(self, graphs):
        # フィルタ単語調査用
        nodes_matched = []
        edges_matched = []
        threshold_node = self.threshold_node
        threshold_edge = self.threshold_edge
        poses_node = self.poses_node
        flags_onoff = [(is_selected, word_pos) for is_selected, word_pos, color_pos, color_edge in self.config.POSES_PARAM[1:]]
        word = self.threshold_word.replace('　', ' ')
        words = word.split(' ')
        msg = f'keywords for filter: {words}'
        self.logger.i(msg)

        # Node: defaultでは "count >= 10" で剪定 (threshold_node)
        # Node: フィルタ単語であるか調査
        # Edgeが無くなったNodeは、そのまま
        source = graphs[-1]
        target = copy.deepcopy(source)
        for node, attr in source.nodes().items():
            for is_selected, word_pos in flags_onoff:
                if (node in poses_node[word_pos]) and is_selected:
                    break
            else:
                data = list(source.edges(node))
                target.remove_edges_from(data)
                continue
            if attr['count'] < threshold_node:
                data = list(source.edges(node))
                target.remove_edges_from(data)
                continue
            for word in words:
                if word not in attr['token']:
                    continue
                nodes_matched.append(node)
        graphs.append(target)

        # Edge: defaultでは "count >= 2" で剪定 (threshold_edge)
        # Edge: フィルタ単語に接続しているか調査
        # Edgeが無くなったNodeは、そのまま
        source = graphs[-1]
        target = copy.deepcopy(source)
        for edge, attr in source.edges().items():
            if attr['count'] < threshold_edge:
                target.remove_edge(*edge)
                continue
            for match in nodes_matched:
                if match in edge:
                    edges_matched.append(edge)
                    break
        graphs.append(target)

        if 0:
            msg_nodes = f'nodes which have the keyrod: {nodes_matched}'
            msg_edges = f'edges conneced to the keyrod: {edges_matched}'
            self.logger.i(msg_nodes)
            self.logger.i(msg_edges)

        # Word: defaultではフィルタ目的の単語が '' なので全てのnodeを表示
        # Edgeが無くなったNodeは、そのまま
        source = graphs[-1]
        target = copy.deepcopy(source)
        for edge, attr in source.edges().items():
            if edge not in edges_matched:
                target.remove_edge(*edge)
        graphs.append(target)

        # Edgeが無くなったNodeを削除
        source = graphs[-1]
        target = copy.deepcopy(source)
        for node in list(source.nodes()):
            if len(source[node]) == 0:
                target.remove_node(node)
        graphs.append(target)

    def calc_node_sizes(self, nodeids_count, locations):
        size_max = self.config.SIZE_MAX_NODE
        nodes_size = [min(nodeids_count[idx] * 50, size_max) for idx in locations.keys()]
        return nodes_size

    def get_data_by_word_pos(self, nodes, poses_node, nodes_size, word_pos):
        data_n = []
        data_s = []
        data_n_append = data_n.append
        data_s_append = data_s.append
        for idx, node in enumerate(nodes):
            if node not in poses_node[word_pos]:
                continue
            data_n_append(node)
            data_s_append(nodes_size[idx])
        return data_n, data_s
#           self.logger.i(word_pos)
#           self.logger.i(poses_node[word_pos])
#           self.logger.i(node)
#             --> 助詞
#             --> [3, 12, 14, 17, 20, 22, 24, 35, 39, 57, 74, 81, ...]
#             --> 2

    def apply_graph_to_networkx(self):
        # self.fig, self.ax = pyplot.subplots(
        #     figsize=self.FIG_SIZE,
        # )
        # self.fig.tight_layout()
        # self.fig.set_tight_layout(0.0)

        self.fig = pyplot.figure(
            figsize=self.config.FIG_SIZE,
        )
        self.fig.canvas.manager.set_window_title(self.config.TITLE)
        self.fig.canvas.mpl_connect(
            'key_press_event',
            self.on_press_key,
        )
        self.fig.canvas.mpl_connect(
            'button_press_event',
            self.on_clicked_any_position,
        )
        self.fig.patch.set_facecolor(self.config.BG_COL_FRAME)
        self.ax = pyplot.gca()
        self.ax.set_facecolor(self.config.BG_COL_GRAPH)

        for data in self.nodes_data:
            nx.draw_networkx_nodes(
                self.graph,
                self.locations,
                nodelist=data[0],
                node_size=data[1],
                node_color=data[2],
                alpha=0.6,
                # ax=self.ax,
            )
        else:
            nx.draw_networkx_edges(
                self.graph,
                self.locations,
                alpha=0.5,
                width=self.edge_widths,
                edge_color=self.edge_colors,
                edge_vmin=-4,  # color density min
                edge_vmax=+4,  # color density max
                edge_cmap=pyplot.cm.Blues,  # Select a color from the sequential. https://matplotlib.org/examples/color/colormaps_reference.html
                # ax=self.ax,
            )
            nx.draw_networkx_labels(
                self.graph,
                self.locations,
                self.labels,
                font_size=10,
                font_family=self.config.FONT,
                # ax=self.ax,
            )

    def apply_widgets_to_graph(self):
        self.RaiseError(name=__name__, ExceptionClass=self.NoOverwrittenError)

    def on_press_key(self, event):
        msg = f'pressed key: {event.key}'
        self.logger.i(msg)
        if event.key == 'escape':
            self.sys.exit()
        if event.key == 'f2':
            self.on_update_filter_words()

    def on_clicked_any_position(self, event):
        msg = 'event info:'
        self.logger.i(msg)
        self.logger.i(f'    button: {event.button}')
        self.logger.i(f'         x: {event.x}')
        self.logger.i(f'         y: {event.y}')
        self.logger.i(f'     xdata: {event.xdata}')
        self.logger.i(f'     ydata: {event.ydata}')

    def on_clicked_all_onoff(self, *args):
        if args[0] != self.config.POSES_PARAM[0][1]:
            return

        def get_all_onoff_checkbox_status():
            checkbox = self.checkboxs[0]
            status = checkbox.get_status()[0]   # Retuns "0 or 1".
            status = True if status else False  # Make it "True or False".
            return status

        status = get_all_onoff_checkbox_status()
        if status == self.status_onoff_all:
            msg = 'no execute all onoff.'
            self.logger.i(msg)
            return
        else:
            msg = 'execute all onoff.'
            self.logger.i(msg)
            self.status_onoff_all = status

        if status:
            for checkboxs in self.checkboxs:
                data = checkboxs.get_status()
                for idx, is_selected in enumerate(data):
                    if is_selected:
                        continue
                    checkboxs.set_active(idx)
        else:
            for checkboxs in self.checkboxs:
                data = checkboxs.get_status()
                for idx, is_selected in enumerate(data):
                    if not is_selected:
                        continue
                    checkboxs.set_active(idx)

    def on_update_filter_words(self, *args):
        if self.is_1st_time:
            return

        if self.is_1st_time_kivy:
            from ai_gui_kivy_inputbox import (
                Inputbox,
                Reset,
            )
            self.Inputbox = Inputbox
            self.Reset = Reset
            self.args_inputbox = [
                self.path_morph_file_white,
                '',
            ]

        self.Reset()
        self.args_inputbox[-1] = self.inputbox_word.text
        app = self.Inputbox()
        app.args = self.args_inputbox
        app.run()
        text_new = app.get_filter_text()
        text_new = text_new.replace('　', ' ')

        if text_new == self.inputbox_word.text:
            return

        self.threshold_word = text_new
        self.inputbox_word.set_val(text_new)
        self.on_update_node_or_edge('')

    def on_clicked_button(self, *args):
        self.on_update_node_or_edge('')

    def on_update_node_or_edge(self, *args):
        self.threshold_node = self.slider_node.val
        self.threshold_edge = self.slider_edge.val
        # pyplot.clf()

        status = []
        for checkboxs in self.checkboxs:
            data = list(checkboxs.get_status())
            status.extend(data)

        msg = f'flags: {status}'
        self.logger.i(status)

        for idx, is_selected in enumerate(status):
            self.config.POSES_PARAM[idx][0] = is_selected

        self.make_graph_data()
        self.apply_graph_to_networkx()
        self.apply_widgets_to_graph()

        numbers = pyplot.get_fignums()
        msg = f'a number of frames: {numbers}'
        self.logger.i(msg)
        if len(numbers) == 0:
            raise Exception()

        manager = pyplot.get_current_fig_manager()
        manager.window.showMaximized()
        pyplot.close(numbers[0])


Classes = reversed((
    CoOccurrenceNetworkBase,
    CoOccurrenceNetworkMorphAnalyzer,
    CoOccurrenceNetworkWidget,
))


@attach_common
class CoOccurrenceNetwork(*Classes):
    pass


if __name__ == '__main__':
    network = CoOccurrenceNetwork()
    network()
