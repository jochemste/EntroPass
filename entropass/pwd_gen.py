
import itertools
import toml
from threading import Thread

class Pwd_gen():
    """
    """
    def __init__(self, config_fd):
        """
        Load specified configuration file
        """
        self.config = toml.load(config_fd)

    def upper_perms(self, word):
        """
        Change characters in word to upper characters. Changes single characters first: 
        Test, tEst, teSt. Followed by all chars left to right: test, Test, TEst, TESt
        Followed by the inverse: TEST, tEST, teST, tesT.
        Removes duplicates before returning.
        """
        word = word.lower()
        self.results = []

        t1 = Thread(target=self.__single_c_upper, args=(word,))
        t2 = Thread(target=self.__c_upper_ltr, args=(word,))
        t3 = Thread(target=self.__c_upper_rtl, args=(word,))

        t1.start()
        t2.start()
        t3.start()

        t1.join()
        t2.join()
        t3.join()

        results = list(dict.fromkeys(self.results))
        self.result = []
        return results

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

        results = [''.join(p) for p in perms]+[''.join(p) for p in perms2]+\
            [''.join(p) for p in perms3]
        results = list(dict.fromkeys(results))
        return results

    def rep_cmmn_chars(self, word: str, count=None, iterations=4):
        """
        Replace commonly replaced characters. Iterate the results a specified number of times 
        and replace more characters in results. For example: 'start' becomes '5tart' and is 
        added to results. After second iteration '5tart' becomes '57ar7', which is added to 
        the results as well. In iterations, all previous results are used, exponentially increasing
        the nr of results. Results are filtered from duplicates at the end, making that 5 
        iterations can provide the same nr of results as 100. However, this will make a 
        significant difference in the processing time.
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
        res = list(dict.fromkeys(res))
        return res

    def __single_c_upper(self, word):
        for i in range(len(word)): # Single Upper chars
            new_word = word[:i] + word[i].upper() + word[i+1:]
            self.results.append(new_word)

    def __c_upper_ltr(self, word):
        for i in range(0, len(word)): # Upper chars, incrementing from left
            new_word = word[:i].upper() + word[i:]
            self.results.append(new_word)

    def __c_upper_rtl(self, word):
        upper_w = word.upper()
        for i in range(0, len(upper_w)): #Upper chars, decrementing from left
            new_word = upper_w[:i].lower() + upper_w[i:]
            self.results.append(new_word)
    
if __name__=='__main__':
    pwd_gen = Pwd_gen('../config/entropass_conf.toml')    
    #print(pwd_gen.word_perms(['harry', 'potter', 'quiditch', 'hedwig'], 2))
    print(pwd_gen.upper_perms('test'))

