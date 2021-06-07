
from string import ascii_lowercase
import itertools
import toml
from threading import Thread
import os
import re

class Pwd_gen():
    """
    A class to handle generating passwords, by using permutations, upper/lower 
    character combinations, replacement of characters, and more.
    """
    def __init__(self, config_fd):
        """
        Loads a specified configuration file.

        Parameters
        ----------
        config_fd : str
            File path of the configuration file.
        """
        self.config = toml.load(config_fd)
        if self.config['generating-rules']['use-regex']:
            self.regex = self.config['generating-rules']['regex']
        if self.config['generating-rules']['use-formats']:
            self.formats = self.config['generating-rules']['formats']
        elif self.config['generating-rules']['use-top-formats']:
            self.formats = self.__get_top_x_formats(x=self.config['generating-rules']['top-formats'])
        else:
            self.formats = False
            

    def upper_perms(self, word):
        """
        Change characters in word to upper characters. Changes single characters first: 
        Test, tEst, teSt. Followed by all chars left to right: test, Test, TEst, TESt
        Followed by the inverse: TEST, tEST, teST, tesT.
        Removes duplicates before returning.
        Runs in three threads for speed.

        Parameters
        ----------
        word : str
            Word to base the new results on.

        Returns
        -------
        results : list
            Results from the three threads.
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

    def reverse(self, word):
        """
        Reverse a word. For example, "word" turns into "drow".

        Parameters
        ----------
        word : str
            Word to reverse
        """
        reverse = word[::-1]
        return reverse

    def fraction(self, word):
        """
        Returns fractions of the given word. For example, 
        for "word" it will return ['w', 'wo', 'wor']
        """
        fracs = []
        for i in range(len(word)):
            fracs.append(word[:i])
        return fracs

    def word_perms(self, words, nr_in_result=2,
                   add_cmmn_sep=True, add_cmmn_end=True):
        """
        Permutations of given words, using a given amount of  words per
        result. For example: words=['hello', 'world', '!'], nr_in_result=2 
        would give results like: 'hello!', 'helloworld', '!world', etc.

        Parameters
        ----------
        words : list
            List of words to create permutations of.
        nr_in_result : int
            Number of words in the final results.
        add_cmmn_sep : bool, default = True
            Adds a commonly used separator to be used in the permutations.
        add_cmmn_end : bool, default = True
            Adds a commonly used end to be used in the permutations.

        Returns
        -------
        results : list
            Resulting permutations.
        """
        results = []
        for i in range(1, nr_in_result+1):
            perms = itertools.permutations([c for c in words], i)
            #perms = itertools.permutations([c for c in words], nr_in_result)
            if add_cmmn_sep:
                cmmn_sep = self.config['common-separators']['list']
                perms2 = itertools.permutations([c for c in words]+cmmn_sep, i)
                #perms2 = itertools.permutations([c for c in words]+cmmn_sep,
                #                                nr_in_result+1)
            if add_cmmn_end:
                cmmn_end = self.config['common-end']['list']
                #perms3 = itertools.permutations([c for c in words]+cmmn_end,
                #                                nr_in_result+1)
                perms3 = itertools.permutations([c for c in words]+cmmn_end, i)

            results += [''.join(p) for p in perms]+[''.join(p) for p in perms2]+\
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

        Parameters
        ----------
        word : str
            Word to replace common characters from.
        count : int, default = None
            Nr of characters to replace every time. For example, if the word is 'all' and 'l' 
            would be replaced by '|', having count=None would result in 'a||', while having count=1
            would result in 'a|l'.
        iterations : int, default = 4
            Number of times to parse previous results. This can allow words like 'all' to 
            become words like '@||' for example.

        Returns
        -------
        results : list
            List of results
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

    def add_cmmn_chars(self,  word: str):
        """
        """
        

    def filter(self, results):
        """
        Filters the given results to only match the formats, specified in the configuration.
        The configuration allows users to specify formats of use the top formats from 
        the processed passwords, or not filter at all.
        
        Parameters
        ----------
        results : list
            Results to be checked and filtered.
        
        Returns
        -------
        results : list
            Results from the filtering.
        """
        ctr=0
        reg_res = []
        if self.regex:
            temp_results = results[:]
            for res in temp_results:
                for regex in self.regex:
                    if re.match(pattern=regex, string=res):
                        reg_res.append(res)
        if self.formats:
            temp_results = results[:]
            results = []
            for res in temp_results:
                ctr += 1
                for format in self.formats:
                    if self.__check_if_format_match(word=res, format=format):
                        results.append(res)

        results = list(dict.fromkeys(results+reg_res))
        return results

    def __single_c_upper(self, word):
        """
        Takes a word and creates all possible combinations of this word with one upper character.
        For example, changes 'word' into 'Word', 'wOrd', 'woRd' and 'worD'. Adds all these words 
        to the self.results member.

        Parameters
        ----------
        word : str
            Word to use for upper char combinations
        """
        for i in range(len(word)): # Single Upper chars
            new_word = word[:i] + word[i].upper() + word[i+1:]
            self.results.append(new_word)

    def __c_upper_ltr(self, word):
        """
        Takes a word and creates all possible combinations of this word with upper characters, 
        from left to right.
        For example, changes 'word' into 'Word', 'WOrd', 'WORd' and 'WORD'. Adds all these words 
        to the self.results member.

        Parameters
        ----------
        word : str
            Word to use for upper char combinations
        """
        for i in range(0, len(word)): # Upper chars, incrementing from left
            new_word = word[:i].upper() + word[i:]
            self.results.append(new_word)

    def __c_upper_rtl(self, word):
        """
        Takes a word and creates all possible combinations of this word with upper characters, 
        from right to left.
        For example, changes 'word' into 'worD', 'woRD', 'wORD' and 'WORD'. Adds all these words 
        to the self.results member.

        Parameters
        ----------
        word : str
            Word to use for upper char combinations
        """
        upper_w = word.upper()
        for i in range(0, len(upper_w)): #Upper chars, decrementing from left
            new_word = upper_w[:i].lower() + upper_w[i:]
            self.results.append(new_word)

    def __check_if_format_match(self, word, format):
        """
        Checks if the format of a word matches to a given format.

        Parameters
        ----------
        word : str
            Word to check for matching format.
        format : str
            Format to check against word.

        Returns
        -------
        .bool
            Returns True if matching, False if not.
        """
        if not(len(word) == len(format)):
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

            if not(c == format[i]):
                return False
                    
        return True

    def __get_top_x_formats(self, x):
        """
        Gets the top x formats from processed passwords, where x is defined in 
        the configuration file. These formats are used in filtering.
        
        Parameters
        ----------
        x : int
            The number of formats to retrieve.

        Returns
        -------
        formats : list
            The formats from processed passwords, to be used for filtering.
        """
        file_ = os.path.dirname(os.path.abspath(__file__))+'/'+self.config['processed-data']['dir']+self.config['processed-data']['format']
        formats = []

        with open(file_, 'r') as fd:
            lines = fd.readlines()[-x:]
            for line in lines:
                form, occ = line.split(' ')

                formats.append(form)

        return formats
            
if __name__=='__main__':
    pwd_gen = Pwd_gen('../config/entropass_conf.toml')    
    #print(pwd_gen.word_perms(['harry', 'potter', 'quiditch', 'hedwig'], 2))
    #print(pwd_gen.upper_perms('test'))

    list_ = ['johann', 'johan']
    print(pwd_gen.filter(list_))
