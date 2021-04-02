import itertools
import toml

class Pwd_gen():
    """
    """
    def __init__(self, config_fd):
        self.config = toml.load(config_fd)

    def word_perms(self, words, nr_in_result):
        """
        Permutations of given words, using a given amount of  words per
        result. For example: words=['hello', 'world', '!'], nr_in_result=2 
        would give results like: 'hello!', 'helloworld', '!world', etc.
        """
        perms = itertools.permutations([c for c in words], nr_in_result)
        return [''.join(p) for p in perms]

    def rep_cmmn_chars(self, word: str, count=None):
        """
        """
        res = []

        for cmmn_char in self.config['common-replacements']:
            new_word = ''
            for char in self.config['common-replacements'][cmmn_char]:
                if not(count):
                    res.append(word.replace(cmmn_char, char))
                else:
                    res.append(word.replace(cmmn_char, char, count))
                    
        return res


    
if __name__=='__main__':
    pwd_gen = Pwd_gen('../config/entropass_conf.toml')    
    print(pwd_gen.word_perms(['harry', 'potter', 'quiditch', 'hedwig'], 2))

