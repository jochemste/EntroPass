
from string import ascii_lowercase
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
        if self.config['generating-rules']['use-patterns']:
            self.patterns = self.config['generating-rules']['patterns']
        elif self.config['generating-rules']['use-top-patterns']:
            self.patterns = self.__get_top_x_patterns(x=self.config['generating-rules']['top-patterns'])
        else:
            self.patterns = False
            

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
        self.result = []
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
        results = [word]

        for cmmn_char in self.config['common-replacements']:
            for char in self.config['common-replacements'][cmmn_char]:
                if not(count):
                    results.append(word.replace(cmmn_char, char))
                else:
                    results.append(word.replace(cmmn_char, char, count))

        results = list(dict.fromkeys(results)) # remove duplicates

        new_results_ph = []
        if iterations <= 1:
            iterations = 0
        else:
            iterations -= 1

        for i in range(iterations):
            new_results = []
            for cmmn_char in self.config['common-replacements']:
                for char in self.config['common-replacements'][cmmn_char]:
                    if not(count):
                        for j in range(len(results)):
                            new_results.append(results[j].replace(cmmn_char, char))
                    else:
                        for j in range(len(results)):
                            new_results.append(results[j].replace(cmmn_char, char,
                                                          count))
            new_results_ph += new_results
            
        results += new_results_ph
        results = list(dict.fromkeys(results)) # remove duplicates
        self.result = []
        return results

    def filter(self, results):
        """
        """
        ctr=0
        if self.patterns:
            temp_results = results[:]
            results = []
            for res in temp_results:
                ctr += 1
                for pattern in self.patterns:
                    if self.__check_if_pattern_match(word=res, pattern=pattern):
                        results.append(res)

            results = list(dict.fromkeys(results))
        return results

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

    def __check_if_pattern_match(self, word, pattern):
        """
        """
        if not(len(word) == len(pattern)):
            return False
        
        for i in range(len(word)):
            c = ''
            if word[i].isdigit():
                c='d'
            elif word[i].isalpha and word[i] in ascii_lowercase:
                if word[i].isupper():
                    c='C'
                else:
                    c='c'
            else:
                c='s'

            if not(c == pattern[i]):
                return False
                    
        return True

    def __get_top_x_patterns(self, x):
        """
        """
        file_ = self.config['processed-data']['dir']+self.config['processed-data']['format']
        patterns = []

        with open(file_, 'r') as fd:
            lines = fd.readlines()[-x:]
            for line in lines:
                form, occ = line.split(' ')

                patterns.append(form)

        return patterns
            
if __name__=='__main__':
    pwd_gen = Pwd_gen('../config/entropass_conf.toml')    
    #print(pwd_gen.word_perms(['harry', 'potter', 'quiditch', 'hedwig'], 2))
    #print(pwd_gen.upper_perms('test'))

    list_ = ['johann', 'johan']
    print(pwd_gen.filter(list_))
