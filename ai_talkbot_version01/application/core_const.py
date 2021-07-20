class Const(object):
    guard_from_loop = False

    class ConstError(Exception):
        pass

    def __setattr__(self, name, value):
        if self.guard_from_loop:
            self.guard_from_loop = False
            return

        if hasattr(self, name):
            err = f"Can't rebind const variable: {name}"
            raise self.ConstError(err)

        self.guard_from_loop = True
        setattr(self, name, value)


if __name__ == '__main__':
    # How to make constant values (the immutables) by python standard module.
    from traceback import format_exc as traceback_format_exc
    from dataclasses import (
        dataclass,
        # field,
        FrozenInstanceError,
    )
    # from typing import (
    #     List,
    #     Tuple,
    # )

    @dataclass(frozen=True)  # Immutables!
    class Marzban(object):
        persons: tuple = (
            ('バフマン', 'Bahman'),
            ('ダリューン', 'Daryun'),
            ('ガルシャースフ', 'Garshasph'),
            ('カーラーン', 'Kharlan'),
            ('ハイル', 'Khayr'),
            ('キシュワード', 'Kishward'),
            ('クバード', 'Kubard'),
            ('クルプ', 'Khurup'),
            ('クシャエータ', 'Kushaeta'),
            ('マヌーチュルフ', 'Manuchurch'),
            ('シャプール', 'Shapur'),
            ('サーム', 'Sam'),
        )

    @dataclass(frozen=True)  # Immutables!
    class Daryun(object):
        name: tuple = ('ダリューン', 'Daryun')
        age: int = 27
        nickname: str = 'マルダーンフ・マルダーン'
        nicknames: tuple = (
            'マルダーンフ・マルダーン',
            'ショラ・セーナニー',
            'エル・エーラーン',
            '黒衣の騎士',
            '戦士の中の戦士',
            '猛虎将軍',
            '大将軍格',
        )

    @dataclass  # Mutables!
    class Kishward(object):
        name: tuple = ('キシュワード', 'Kishward')
        age: int = 29
        nickname: str = 'ターヒール'
        nicknames: tuple = (
            'ターヒール',
            'エーラーン',
            '双刀将軍',
            '生ける城壁',
            '双刀将軍キシュワードあるかぎりミスル軍はディジレ河を越えるあたわず',
            '大将軍',
        )

    marzban = Marzban()
    print(f'万騎長 (Marzban):')  # NOQA: F541
    for person in marzban.persons:
        print(f'    {person}')
    try:
        marzban.persons[0] = ('エステル', 'Ester')
        print(marzban.persons[0])
    except TypeError:
        err = 'TypeError: "tuple" object does not support item assignment'
        print(err)
    finally:
        print()

    person = Daryun()
    print(f'名前: {person.name[0]} ({person.name[1]})')
    print(f'年齢: {person.age}')
    print(f'異名:')  # NOQA: F541
    for nickname in person.nicknames:
        print(f'    {nickname}')
    try:
        person.age = 30
        print(person.age)
    except FrozenInstanceError:
        err = 'FrozenInstanceError: cannot assign to field'
        print(err)
    finally:
        print()

    person = Kishward()
    print(f'名前: {person.name[0]} ({person.name[1]})')
    print(f'年齢: {person.age}')
    print(f'異名:')  # NOQA: F541
    for nickname in person.nicknames:
        print(f'    {nickname}')
    try:
        person.age = '二十九歳'
        print(person.age)
    except:  # NOQA: E722
        err = traceback_format_exc()
        print(err)
    finally:
        print()
