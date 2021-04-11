import toml

class Pwd_score():
    form_fd = ''

    def __init__(self, config_fd):
        self.config = toml.load(config_fd)
        

    def score_pwd_format(self, pwd, format_, occurrences, format_weight=1.0):
        """
        """
        score = 0.0
        max_score = 1.0
        char_weight = (max_score-score)/len(format_)

        diff = abs(len(pwd)-len(format_))
        score -= (diff*char_weight)

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

    def score_pwd_chars(self, pwd, char, occurrences, chars_weight=1.0):
        """
        """
        score = 0.0
        max_score = 1.0
        weight = (max_score-score)/len(pwd)

        for c in pwd:
            if c == char:
                score += weight

        return round(score*(occurrences*chars_weight))
        

if __name__=='__main__':
    p = Pwd_score('../config/entropass_conf.toml')

    score = p.score_pwd_format('hello2ooo', 'cccccd', 7979)
    print('final',score)
    
    score = p.score_pwd_format('hello', 'ccccc', 7979)
    print('final',score)
        
    score = p.score_pwd_format('hello', 'Cccccc', 34)
    print('final',score)
