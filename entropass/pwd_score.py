import toml

class Pwd_score():
    form_fd = ''

    def __init__(self, config_fd):
        self.config = toml.load(config_fd)
        

    def score_pwd_format(self, pwd, format_, occurrences):
        """
        """
        score = 0.0
        if len(pwd)>len(format_):
            weight = (min(len(format_),
                                      len(pwd))/max(len(pwd),
                                                    len(format_)))
        else:
            weight = (len(pwd)/len(format_))
        match = True
            
        for i in range(min(len(pwd), len(format_))):
            if pwd[i].isdigit() and (format_[i]=='d'):
                score += weight
            elif pwd[i].isalpha() and format_[i].lower()=='c':
                if pwd[i].isupper() and format_[i].isupper():
                    score += weight
                elif not(pwd[i].isupper()) and not(format_[i].isupper()):
                    score += weight
                else:
                    score += (weight/2.0)
            elif not(pwd[i].isalpha() or pwd[i].isdigit()) \
                 and not(format_[i].lower()=='c' or format_[i]=='d'):
                score += weight

        print('raw',score)
        return round(score*occurrences)

if __name__=='__main__':
    p = Pwd_score('../config/entropass_conf.toml')

    score = p.score_pwd_format('hello2ooo', 'cccccd', 7979)
    print('final',score)
    
    score = p.score_pwd_format('hello', 'ccccc', 7979)
    print('final',score)
        
    score = p.score_pwd_format('hello', 'Cccccc', 34)
    print('final',score)
