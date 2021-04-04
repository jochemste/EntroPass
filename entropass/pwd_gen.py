import itertools
import toml

class Pwd_gen():
    """
    """
    def __init__(self, config_fd):
        self.config = toml.load(config_fd)

    def word_perms(self, words, nr_in_result,
                   add_cmmn_sep=True, add_cmmn_end=True):
        """
        Permutations of given words, using a given amount of  words per
        result. For example: words=['hello', 'world', '!'], nr_in_result=2 
        would give results like: 'hello!', 'helloworld', '!world', etc.
        """
        perms = itertools.permutations([c for c in words], nr_in_result)
        if add_cmmn_sep:
            cmmn_sep = self.config['common-separators']['list']
            perms2 = itertools.permutations([c for c in words]+cmmn_sep,
                                            nr_in_result+1)
        if add_cmmn_end:
            cmmn_end = self.config['common-end']['list']
            perms3 = itertools.permutations([c for c in words]+cmmn_end,
                                            nr_in_result+1)
        return [''.join(p) for p in perms]+[''.join(p) for p in perms2]+[''.join(p) for p in perms3]

    def rep_cmmn_chars(self, word: str, count=None, iterations=2):
        """
        Iterations exponentially increase 
        """
        res = [word]

        for cmmn_char in self.config['common-replacements']:
            for char in self.config['common-replacements'][cmmn_char]:
                if not(count):
                    res.append(word.replace(cmmn_char, char))
                else:
                    res.append(word.replace(cmmn_char, char, count))

        new_res_ph = []
        if iterations <= 1:
            iterations = 0
        else:
            iterations -= 1
        for i in range(iterations):
            new_res = []
            for cmmn_char in self.config['common-replacements']:
                for char in self.config['common-replacements'][cmmn_char]:
                    if not(count):
                        for i in range(len(res)):
                            new_res.append(res[i].replace(cmmn_char, char))
                    else:
                        for i in range(len(res)):
                            new_res.append(res[i].replace(cmmn_char, char,
                                                          count))
            new_res_ph += new_res
            
        res += new_res_ph
        return res

    def rep_cmmn_chars_temp(self, word: str, count=None):
        """
        TODO: Make function replace more than a single type character.
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

