import matplotlib.pyplot as pyplot
from matplotlib.widgets import (
    TextBox,
    Slider,
    CheckButtons,
    Button,
)


class CoOccurrenceNetworkWidget(object):
    slider_node = None
    slider_edge = None
    inputbox_word = None
    button_redraw = None
    checkboxs = [None] * 4

    parts_spin = ('left', 'right', 'bottom', 'top')

    checkbox_rect_color_bg = (0.0, 0.0, 1.0)
    checkbox_rect_color_fg = (0.0, 1.0, 1.0)
    checkbox_width_x_mark = 3

    def apply_widgets_to_graph(self):
        self.label_nodes = self.config.LABEL_NODE
        self.label_edges = self.config.LABEL_EDGE
        self.label_inputbox = self.config.LABEL_IBOX
        self.label_button = self.config.LABEL_BUTTON

        axes = self.get_axes_data()
        self.add_sliders(axes)
        self.add_inputboxes(axes)
        self.add_buttons(axes)
        self.add_checkboxes(axes)
        self.update_frame_colors(axes)

        if 0:
            print(*dir(), sep='\n')
            print(*dir(self.slider_edge.poly), sep='\n')
            print(*dir(self.slider_node.label), sep='\n')

    def get_axes_data(self):
        pyplot.subplots_adjust(
            left=0.00,
            right=1.00,
            top=1.00,
            bottom=0.12,
        )
        axes_dat = [  # x, y, width, height
            [0.14, 0.08, 0.48, 0.03],
            [0.14, 0.05, 0.48, 0.03],
            [0.22, 0.02, 0.40, 0.03],
            [0.68, 0.01, 0.06, 0.10],
            [0.74, 0.01, 0.06, 0.10],
            [0.80, 0.01, 0.06, 0.10],
            [0.86, 0.01, 0.06, 0.10],
            [0.94, 0.01, 0.04, 0.10],
        ]
        axes_key = (
            "slider_node",
            "slider_edge",
            "inputbox",
            "check_pos_1",
            "check_pos_2",
            "check_pos_3",
            "check_pos_4",
            "button",
        )
        axes_col = (
            self.config.BG_COL_NODE_AX,
            self.config.BG_COL_EDGE_AX,
            self.config.BG_COL_IBOX_AX,
            self.config.BG_COL_CHECKB_AX,
            self.config.BG_COL_CHECKB_AX,
            self.config.BG_COL_CHECKB_AX,
            self.config.BG_COL_CHECKB_AX,
            self.config.BG_COL_BUTTON_AX,
        )
        data_zip = zip(axes_key, axes_dat, axes_col)
        axes = {key: pyplot.axes(val, facecolor=col) for key, val, col in data_zip}
        return axes

    def add_sliders(self, axes):
        slider_node_ax = pyplot.axes(axes["slider_node"])
        slider_edge_ax = pyplot.axes(axes["slider_edge"])
        label_node = self.label_nodes
        label_edge = self.label_edges
        slider_node_default = self.threshold_node
        slider_edge_default = self.threshold_edge

        node = Slider(slider_node_ax, label_node, 1, 20, valinit=slider_node_default, valstep=1, valfmt='%2d')
        edge = Slider(slider_edge_ax, label_edge, 1, 10, valinit=slider_edge_default, valstep=1, valfmt='%2d')
        node.on_changed(self.on_update_node_or_edge)
        edge.on_changed(self.on_update_node_or_edge)

        node_e = node.label
        edge_e = edge.label
        node_e.set_color(self.config.FG_COL_NODE_LABEL)
        edge_e.set_color(self.config.FG_COL_EDGE_LABEL)
        node_e.set_backgroundcolor(self.config.BG_COL_NODE_LABEL)
        edge_e.set_backgroundcolor(self.config.BG_COL_EDGE_LABEL)

        node_e = node.valtext
        edge_e = edge.valtext
        node_e.set_color(self.config.FG_COL_NODE_LABEL)
        edge_e.set_color(self.config.FG_COL_NODE_LABEL)
        node_e.set_backgroundcolor(self.config.BG_COL_NODE_LABEL)
        edge_e.set_backgroundcolor(self.config.BG_COL_EDGE_LABEL)

        node_e = node.vline
        edge_e = edge.vline
        node_e.set_linewidth(5)
        edge_e.set_linewidth(5)
        node_e.set_linestyle('-')
        edge_e.set_linestyle('-')
        node_e.set_solid_capstyle('round')
        edge_e.set_solid_capstyle('round')
        node_e.set_color(self.config.BG_COL_NODE_VLINE)
        edge_e.set_color(self.config.BG_COL_EDGE_VLINE)

        node_e = node.poly
        edge_e = edge.poly
        node_e.set_edgecolor(self.config.BG_COL_NODE_POLY)
        edge_e.set_edgecolor(self.config.BG_COL_EDGE_POLY)
        node_e.set_facecolor(self.config.BG_COL_NODE_POLY)
        edge_e.set_facecolor(self.config.BG_COL_EDGE_POLY)

        self.slider_node = node
        self.slider_edge = edge

    def add_inputboxes(self, axes):
        kwargs = {
            "ax": axes["inputbox"],
            "label": self.label_inputbox,
            "initial": self.threshold_word,
            "hovercolor": self.config.BG_COL_IBOX_HOVER,
            "color": self.config.BG_COL_IBOX_SPACE,
        }
        widget = TextBox(**kwargs)

        element = widget.label
        element.set_color(self.config.FG_COL_IBOX_LABEL)
        element.set_backgroundcolor(self.config.BG_COL_IBOX_LABEL)

        element = widget.text_disp
        element.set_color(self.config.FG_COL_IBOX_DISP)
        element.set_backgroundcolor((1.0, 1.0, 1.0, 0.1))

        self.inputbox_word = widget

    def add_buttons(self, axes):
        kwargs = {
            "ax": axes["button"],
            "label": self.label_button,
            "hovercolor": self.config.BG_COL_BUTTON_HOVER,
            "color": self.config.BG_COL_BUTTON_SPACE,
        }
        widget = Button(**kwargs)

        element = widget.label
        element.set_color('black')

        widget.on_clicked(self.on_clicked_button)
        self.button_redraw = widget

    def add_checkboxes(self, axes):
        axes["check_pos_1"].set_facecolor((0.0, 0.8, 0.8, 0.3))
        axes["check_pos_2"].set_facecolor((0.0, 0.8, 0.8, 0.2))
        axes["check_pos_3"].set_facecolor((0.0, 0.8, 0.8, 0.1))
        axes["check_pos_4"].set_facecolor((0.0, 0.8, 0.8, 0.2))

        max = len(self.config.POSES_PARAM)
        self.checkbox_pos_1 = CheckButtons(
            axes["check_pos_1"],
            tuple(data[1] for data in self.config.POSES_PARAM[0:3]),
            tuple(data[0] for data in self.config.POSES_PARAM[0:3]),
        )
        self.checkbox_pos_2 = CheckButtons(
            axes["check_pos_2"],
            tuple(data[1] for data in self.config.POSES_PARAM[3:6]),
            tuple(data[0] for data in self.config.POSES_PARAM[3:6]),
        )
        self.checkbox_pos_3 = CheckButtons(
            axes["check_pos_3"],
            tuple(data[1] for data in self.config.POSES_PARAM[6:9]),
            tuple(data[0] for data in self.config.POSES_PARAM[6:9]),
        )
        self.checkbox_pos_4 = CheckButtons(
            axes["check_pos_4"],
            tuple(data[1] for data in self.config.POSES_PARAM[9:max]),
            tuple(data[0] for data in self.config.POSES_PARAM[9:max]),
        )
        self.checkboxs[0] = self.checkbox_pos_1
        self.checkboxs[1] = self.checkbox_pos_2
        self.checkboxs[2] = self.checkbox_pos_3
        self.checkboxs[3] = self.checkbox_pos_4

        self.checkbox_pos_1.on_clicked(self.on_clicked_all_onoff)

        col_bg = self.checkbox_rect_color_bg
        col_fg = self.checkbox_rect_color_fg
        width = self.checkbox_width_x_mark
        poses = self.config.POSES_PARAM
        for idx, checkbox in enumerate(self.checkboxs):
            for rect in checkbox.rectangles:
                rect.set_facecolor(col_bg)
                rect.set_edgecolor('k')
                rect.set_linewidth(0)
                rect.set_alpha(0.7)

            for lines in checkbox.lines:
                for line in lines:
                    line.set_color(col_fg)
                    line.set_linewidth(width)
                    line.set_alpha(0.5)

            if idx < 0 or idx > 3:
                pass
            elif idx == 0:
                for idx_l in range(0, 3):
                    idx_p = idx_l + (3 * idx)
                    color = poses[idx_p][2]
                    checkbox.labels[idx_l].set_color(color)
            elif idx == 1:
                for idx_l in range(0, 3):
                    idx_p = idx_l + (3 * idx)
                    color = poses[idx_p][2]
                    checkbox.labels[idx_l].set_color(color)
            elif idx == 2:
                for idx_l in range(0, 3):
                    idx_p = idx_l + (3 * idx)
                    color = poses[idx_p][2]
                    checkbox.labels[idx_l].set_color(color)
            elif idx == 3:
                for idx_l in range(0, 3):
                    idx_p = idx_l + (3 * idx)
                    color = poses[idx_p][2]
                    checkbox.labels[idx_l].set_color(color)

    def update_frame_colors(self, axes):
        color = self.config.BG_COL_FRAME
        for part in self.parts_spin:
            axes["slider_node"].spines[part].set_color(color)
            axes["slider_edge"].spines[part].set_color(color)
            axes["inputbox"].spines[part].set_color(color)
            axes["check_pos_1"].spines[part].set_color(color)
            axes["check_pos_2"].spines[part].set_color(color)
            axes["check_pos_3"].spines[part].set_color(color)
            axes["check_pos_4"].spines[part].set_color(color)
            axes["button"].spines[part].set_color(color)
            self.ax.spines[part].set_color(color)


if __name__ == '__main__':
    from ai_nx_analyzer import CoOccurrenceNetwork
    network = CoOccurrenceNetwork()
    network()
