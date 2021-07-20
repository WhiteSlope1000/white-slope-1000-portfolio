from ai_list_common import (
    ListInterface,
    ListBase,
    ListTypeMorpheme,
    TestRunnerNoCheckNgram,
)


class MorphemeList(ListTypeMorpheme, ListBase, ListInterface):
    def check_num_of_gram(self, num_of_gram):
        if super().check_num_of_gram(num_of_gram):
            return

    def update_starting_token_list(self):
        pass

    def update_token_list(self):
        pass


if __name__ == '__main__':
    TestRunnerNoCheckNgram(MorphemeList)
