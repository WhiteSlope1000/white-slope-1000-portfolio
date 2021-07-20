from ai_list_common import (
    ListInterface,
    ListBase,
    ListTypeMorpheme,
    TestRunnerNoCheckNgram,
)


class MemorizeList(ListTypeMorpheme, ListBase, ListInterface):
    def update_starting_token_list(self):
        txt = self.msg_by_user
        self.logger.i('msg_by_user:')
        self.logger.i(f'    {txt}')

        size_old = len(self.starting_token_list)
        size_new = size_old

        start_morph_list = []
        num = len(txt)
        if num < 1:
            pass
        elif num == 1:
            if self.sort_chr_type(txt) == 2:
                start_morph_list = [txt]
        else:
            start_morph_list = self.make_type_name_list(txt)
        self.starting_token_list = start_morph_list + self.starting_token_list
        size_new = len(self.starting_token_list)
        size_dif = len(start_morph_list)

        msg_size = 'starting token size:'
        msg_size_old = f'    old: {size_old}'
        msg_size_new = f'    new: {size_new}'
        msg_size_dif = f'    dif: {size_dif}'
        msg_dif_text = f'  added: {start_morph_list}'
        self.logger.i(msg_size)
        self.logger.i(msg_size_old)
        self.logger.i(msg_size_new)
        self.logger.i(msg_size_dif)
        self.logger.i(msg_dif_text)

    def update_token_list(self):
        txt = self.msg_by_user
        self.logger.i('msg_by_user:')
        self.logger.i(f'    {txt}')

        size_old = len(self.token_list)
        size_new = size_old

        morph_list = []
        num = len(txt)
        if num < 1:
            pass
        elif num == 1:
            morph_list = [txt]
        else:
            morph_list = self.make_morph_list(txt)
        self.token_list = morph_list + self.token_list
        size_new = len(self.token_list)
        size_dif = len(morph_list)

        msg_size = 'token size:'
        msg_size_old = f'    old: {size_old}'
        msg_size_new = f'    new: {size_new}'
        msg_size_dif = f'    dif: {size_dif}'
        msg_dif_text = f'  added: {morph_list}'
        self.logger.i(msg_size)
        self.logger.i(msg_size_old)
        self.logger.i(msg_size_new)
        self.logger.i(msg_size_dif)
        self.logger.i(msg_dif_text)


if __name__ == '__main__':
    TestRunnerNoCheckNgram(MemorizeList)
