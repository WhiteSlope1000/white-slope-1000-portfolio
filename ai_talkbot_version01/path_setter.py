import sys
import os.path
import os


def main():
    path_crr = os.path.dirname(__file__)
    paths = (
        os.path.join(path_crr, 'application'),
    )
    for path in paths:
        add_to_sys_path(path)
    return sys.path[:]


def add_to_sys_path(path):
    flags = (
        path not in sys.path,
        os.path.exists(path),
        os.path.isdir(path),
    )
    if all(flags):
        sys.path.append(path)


if __name__ != '__main__':
    main()

if __name__ == '__main__':
    import py_compile

    py_compile.compile(__file__)
    path_a = sys.path[:]
    path_b = main()
    path_c = set(path_b) - set(path_a)

    msgs = [
        ' default sys path:',
        'added to sys path:',
    ]

    print(msgs[0])
    for path in sorted(list(path_a)):
        print(f'    {path}')
    print()

    print(msgs[1])
    for path in sorted(list(path_c)):
        print(f'    {path}')
    print()
