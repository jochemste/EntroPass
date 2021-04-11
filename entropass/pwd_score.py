import toml
from threading import Thread

class Pwd_score():
    form_fd = ''
    char_fd = ''
    forms = {}
    chars = {}

    def __init__(self, config_fd):
        """
        """
        self.config = toml.load(config_fd)
        dir = self.config['processed-data']['dir']
        self.form_fd = dir+self.config['processed-data']['format']
        self.char_fd = dir+self.config['processed-data']['char']
        self.__parse_formats()
        self.__parse_chars()
        
    def score_pwd(self, pwd):
        """
        """
        self.score = 0.0

        #t1 = Thread(target=self.__score_forms_thr, args=(pwd,))
        #t2 = Thread(target=self.__score_chars_thr, args=(pwd,))

        #t1.start()
        #t2.start()

        #t1.join()
        #t2.join()

        self.__score_forms(pwd)
        self.__score_chars(pwd)
        
        #for form, occ in self.forms.items():
        #    self.score += self.score_pwd_format(pwd=pwd, format_=form,
        #                                   occurrences=occ)

        #for char, occ in self.chars.items():
        #    self.score += self.score_pwd_chars(pwd=pwd, char=char, occurrences=occ)

        score = self.score
        self.score = 0.0
        return score

    def score_pwd_format(self, pwd, format_, occurrences, format_weight=1.0):
        """
        """
        score = 0.0
        max_score = 1.0
        char_weight = (max_score-score)/len(format_)

        if abs(len(pwd)-len(format_)):
            return 0.0

        for i in range(min(len(pwd), len(format_))):
            if pwd[i].isdigit() and (format_[i]=='d'):
                score += char_weight
            elif pwd[i].isalpha() and format_[i].lower()=='c':
                if pwd[i].isupper() and format_[i].isupper():
                    score += char_weight
                elif not(pwd[i].isupper()) and not(format_[i].isupper()):
                    score += char_weight
                else:
                    score += (char_weight/2.0)
            elif not(pwd[i].isalpha() or pwd[i].isdigit()) \
                 and not(format_[i].lower()=='c' or format_[i]=='d'):
                score += char_weight

        return round(score*(occurrences*format_weight))

    def score_pwd_chars(self, pwd, char, occurrences, chars_weight=0.1):
        """
        """
        score = 0.0
        max_score = 1.0
        weight = (max_score-score)/len(pwd)

        for c in pwd:
            if c == char:
                score += weight

        return round(score*(occurrences*chars_weight))

    def __score_forms(self, pwd):
        for form, occ in self.forms.items():
            self.score += self.score_pwd_format(pwd=pwd, format_=form,
                                           occurrences=occ)

    def __score_chars(self, pwd):
        for char, occ in self.chars.items():
            self.score += self.score_pwd_chars(pwd=pwd, char=char, occurrences=occ)
    
    def __parse_formats(self):
        """
        """
        with open(self.form_fd, 'r') as fd:
            for line in fd:
                form, occ = line.split(' ')
                self.forms[form] = int(occ)

    def __parse_chars(self):
        """
        """
        with open(self.char_fd, 'r') as fd:
            for line in fd:
                char, occ = line.split(' ')
                self.chars[char] = int(occ)

if __name__=='__main__':
    p = Pwd_score('../config/entropass_conf.toml')

    #    score = p.score_pwd_format('hello2ooo', 'cccccd', 7979)
    #    print('final',score)
    #    
    #    score = p.score_pwd_format('hello', 'ccccc', 7979)
    #    print('final',score)
    #        
    #    score = p.score_pwd_format('hello', 'Cccccc', 34)
    #    print('final',score)
    #
    #    score = p.score_pwd_chars('hallo', 'a', 12202)
    #    print('char:', score)
    #

    print('hello', p.score_pwd('hello'))
    print('he110', p.score_pwd('he110'))
    print('12345', p.score_pwd('12345'))
