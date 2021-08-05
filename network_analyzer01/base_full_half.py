from unicodedata import east_asian_width


class ZenHan(object):
    def get_real_hankaku_length(self, strings):
        is_ZEN = 'FWAN'.find
        is_EAW = east_asian_width

        def core(strings):
            num_zen = 0
            for chr in strings:
                if is_ZEN(is_EAW(chr)) != -1:
                    num_zen += 1
            return len(strings) + num_zen

        result = core(strings)
        self.get_real_hankaku_length = core
        return result

    def get_valid_str_num(self, strings, max_num_han=1024):
        is_ZEN = 'FWAN'.find
        is_EAW = east_asian_width

        def core(strings, max_num_han=1024):
            num_han = sum((
                0,
                len(strings),
                len([None for chr in strings if is_ZEN(is_EAW(chr)) != -1]),
            ))
            if max_num_han < num_han:
                num_han_max = max_num_han
                num_zen = len([None for chr in strings[:num_han_max] if is_ZEN(is_EAW(chr)) != -1])
                if num_zen & 1:
                    # Odd number
                    num_han = num_han_max - num_zen + 1
                else:
                    # Even number
                    num_han = num_han_max - num_zen

                last_string = strings[num_han]
                if is_ZEN(is_EAW(last_string)) != -1:
                    num_han = num_han_max - num_zen - 1

                return (num_han, num_han_max)
            else:
                return (num_han, num_han)

        result = core(strings, max_num_han)
        self.get_valid_str_num = core
        return result


if __name__ == '__main__':
    from core_logger import Logging
    logger = Logging(__name__).get_logger()

    inst = ZenHan()

    def test_cases(inst):
        logger.info('')
        logger.info('')
        logger.info('')
        cases = (
            'xxxxxx_xxxxxx_xxxx_20170928155032',
            'manga_',
            '文字_20170924175936____',
            '文字列長_20170924175936',
            '70924175936____文字_201',
            '_20170924175936文字列長',
        )
        return cases

    def print_info(inst, cases, max_num_han):
        logger.info(f'{"#"*80}')
        logger.info(f'"半角での最大表示文字数": {max_num_han:2d}')
        logger.info(f'{"#"*80}')
        for target in cases:
            num_han, num_han_max = inst.get_valid_str_num(target, max_num_han)
            logger.info(f'                対象: "{target}"')
            logger.info(f'  標準関数での文字数: {len(target):2d}')
            logger.info(f'    半角長での文字数: {inst.get_real_hankaku_length(target):2d}')
            logger.info(f'          提案文字数: {num_han:2d}')
            logger.info(f'        省略適用方法: target[:{num_han}]')
            logger.info(f'                対象: "{target}"')
            logger.info(f'          省略適用後: "{target[:num_han]}"')
            logger.info('')
            logger.info('')
        logger.info('')

    cases = test_cases(inst)
    print_info(inst, cases, 16)  # NOQA: E241
    print_info(inst, cases,  8)  # NOQA: E241
    print_info(inst, cases, 50)  # NOQA: E241
