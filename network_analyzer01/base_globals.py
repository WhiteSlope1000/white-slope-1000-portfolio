class GlobalsChecker(object):
    targets = (
        'pos',
        'nodes_n',
        'nodes_size',
        'ax',
    )

    def __init__(self):
        data = globals().copy()
        for target in self.targets:
            for key, val in data.items():
                if key != target:
                    continue
                self.output_debug_info(key, val)
                break

    def output_debug_info(self, name, val):
        try:
            length = len(val)
        except:  # NOQA: E722
            length = None
        print(f'"{name}": {length},  {val}')


if __name__ == '__main__':
    pos = 100
    nodes_n = {"これは": 0, "テスト": 1}
    nodes_size = [0, 1]
    ax = GlobalsChecker()

    GlobalsChecker()
