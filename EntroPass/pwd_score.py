from string import ascii_lowercase
import toml
import re
import os

class Pwd_score():
    """
    """
    form_fd = ''
    char_fd = ''
    forms = {}
    chars = {}

    def __init__(self, config_fd):
        """
        Initialises Pwd_score object. Takes the path to a toml config file and processes it.

        Parameters
        ----------
        config_fd: str
            Path to toml configuration file.
        """
        self.config = toml.load(config_fd)
        dir = os.path.dirname(os.path.abspath(__file__))+'/'+self.config['processed-data']['dir']
        self.form_fd = dir+self.config['processed-data']['format']
        self.char_fd = dir+self.config['processed-data']['char']

        self.__parse_formats()
        self.__parse_chars()

        self.__parse_categories()
        
    def score_pwd(self, pwd):
        """
        Scores the given password, based on format, used chars, presence in categories 
        and known patterns. Returns the score.

        Parameters
        ----------
        pwd : str
            The password to score.

        Returns
        -------
        score : int
            The score of the password.
        """
        self.score = 0.0

        self.__score_forms(pwd)
        self.__score_chars(pwd)
        self.__score_pwd_cat(pwd)
        s = self.score
        self.__score_patterns(pwd)

        score = self.score
        self.score = 0.0
        return score

    def score_pwd_format(self, pwd, format_, occurrences, format_weight=100.0):
        """
        Scores the given password on the given format.
        
        Parameters
        ----------
        pwd : str
            The password to score
        format_ : str
            The format to compare the password against
        occurrences : int
            The number of times the format occurred. This is used to give a weight to the score.
        format_weight : float, 100.0
            The weight that formats receive in the entire scoring process.
        
        Returns
        -------
        .int
            The rounded score as an integer.
        """
        score = 0.0
        max_score = 1.0
        char_weight = (max_score-score)/len(format_)

        if abs(len(pwd)-len(format_)):
            return 0.0

        for i in range(min(len(pwd), len(format_))):
            if pwd[i].isdigit() and (format_[i]=='d'):
                score += char_weight
            elif self.isalphabet(pwd[i]) and format_[i].lower()=='c':
                if pwd[i].isupper() and format_[i].isupper():
                    score += char_weight
                elif not(pwd[i].isupper()) and not(format_[i].isupper()):
                    score += char_weight
                else:
                    score += (char_weight/2.0)
            elif not(self.isalphabet(pwd[i]) or pwd[i].isdigit()) \
                 and not(format_[i].lower()=='c' or format_[i]=='d'):
                score += char_weight

        return round(score*(occurrences*format_weight))

    def score_pwd_chars(self, pwd, char, occurrences, chars_weight=0.1):
        """
        Scores the given password based on used characters.
        
        Parameters
        ----------
        pwd : str
            The password to score
        char : str
            The character to check the password for.
        occurrences : int
            The number of times the character occurred.
        chars_weight : float, 0.1
            The weight that character score have in the scoring process.

        Returns
        -------
        .int
            The rounded score as an integer.
        """
        score = 0.0
        max_score = 1.0
        weight = (max_score-score)/(len(pwd)+1)

        if char in pwd:
            for c in pwd:
                if c == char:
                    score += weight

        return round(score*(occurrences*chars_weight))

    def score_pwd_name(self, pwd, name, name_weight=10000.0):
        """
        Scores the password based on a name being present.

        Parameters
        ----------
        pwd : str
            The password to score
        name : str
            The name to check the password for.
        occurrences : int
            The number of times the name occurred.
        chars_weight : float, 10000.0
            The weight that name scores have in the scoring process.

        Returns
        -------
        .int
            The rounded score as an integer.
        """
        score = 0.0
        max_score = 1.0
        weight = (max_score-score)
        
        if name in pwd:
            score += weight

        return round(score*name_weight)

    def score_pwd_pattern(self, pwd, pattern, patt_weight=100.0):
        """
        Scores a pwd for a specific pattern.
        
        Parameters
        ----------
        pwd : str
            The password to score
        pattern : str
            The regex pattern to check the password for.
        patt_weight : float, 10000.0
            The weight that pattern scores have in the scoring process.

        Returns
        -------
        .int
            The rounded score as an integer.
        """
        score = 0.0
        max_score = 1.0
        weight = (max_score-score)
        
        match = re.match(pattern=pattern, string=pwd)
        if match:
            score += weight
        return round(score*patt_weight)
    
    def __score_pwd_cat(self, pwd):
        """
        Scores a password based on information categories.

        Parameters
        ----------
        pwd : str
            The password to score
        """
        for name in self.names:
            self.score += self.score_pwd_name(pwd=pwd, name=name)

    def __score_patterns(self, pwd):
        """
        Scores a password based on regex patterns.

        Parameters
        ----------
        pwd : str
            The password to score
        """
        for key in self.config['patterns']:
            pattern = self.config['patterns'][key]
            self.score += self.score_pwd_pattern(pwd=pwd, pattern=pattern)

    def __score_forms(self, pwd):
        """
        Scores a password based on formats.

        Parameters
        ----------
        pwd : str
            The password to score
        """
        for form, occ in self.forms.items():
            self.score += self.score_pwd_format(pwd=pwd, format_=form,
                                                occurrences=occ)

    def __score_chars(self, pwd):
        """
        Scores a password based on characters.

        Parameters
        ----------
        pwd : str
            The password to score
        """
        for char, occ in self.chars.items():
            self.score += self.score_pwd_chars(pwd=pwd, char=char, occurrences=occ)
    
    def __parse_formats(self):
        """
        Scores a password based on formats.

        Parameters
        ----------
        pwd : str
            The password to score
        """
        with open(self.form_fd, 'r') as fd:
            for line in fd:
                form, occ = line.split(' ')
                self.forms[form] = int(occ)

    def __parse_chars(self):
        """
        Parses the characters and nr of occurrences.
        """
        with open(self.char_fd, 'r') as fd:
            for line in fd:
                char, occ = line.split(' ')
                self.chars[char] = int(occ)

    def __parse_names(self):
        """
        Parses the names category.
        """
        self.names = []
        with open(self.name_fd, 'r') as fd:
            for name in fd:
                name = name.split('\n')[0]
                self.names.append(name)

    def __parse_foods(self):
        """
        Parses the foods category.
        """
        self.foods = []
        with open(self.foods_fd, 'r') as fd:
            for food in fd:
                food = food.split('\n')[0]
                self.foods.append(food)

    def __parse_dates(self):
        """
        Parses the dates category.
        """
        self.dates = []
        with open(self.dates_fd, 'r') as fd:
            for date in fd:
                date = date.split('\n')[0]
                self.dates.append(date)

    def __parse_erotics(self):
        """
        Parses the erotics category.
        """
        self.erotics = []
        with open(self.erotics_fd, 'r') as fd:
            for erotic in fd:
                erotic = erotic.split('\n')[0]
                self.erotics.append(erotic)

    def __parse_hobbys(self):
        """
        Parses the hobby's category.
        """
        self.hobbys = []
        with open(self.hobbys_fd, 'r') as fd:
            for hobby in fd:
                hobby = hobby.split('\n')[0]
                self.hobbys.append(hobby)

    def __parse_keystrokes(self):
        """
        Parses the keystrokes category.
        """
        self.keystrokes = []
        with open(self.keystrokes_fd, 'r') as fd:
            for keystroke in fd:
                keystroke = keystroke.split('\n')[0]
                self.keystrokes.append(keystroke)

    def __parse_movies(self):
        """
        Parses the movies category.
        """
        self.movies = []
        with open(self.movies_fd, 'r') as fd:
            for movie in fd:
                movie = movie.split('\n')[0]
                self.movies.append(movie)

    def __parse_music(self):
        """
        Parses the music category.
        """
        self.music = []
        with open(self.music_fd, 'r') as fd:
            for m in fd:
                m = m.split('\n')[0]
                self.music.append(m)

    def __parse_places(self):
        """
        Parses the places category.
        """
        self.places = []
        with open(self.places_fd, 'r') as fd:
            for place in fd:
                place = place.split('\n')[0]
                self.places.append(place)

    def __parse_religions(self):
        """
        Parses the religions category.
        """
        self.religions = []
        with open(self.religions_fd, 'r') as fd:
            for religion in fd:
                religion = religion.split('\n')[0]
                self.religions.append(religion)

    def __parse_sports(self):
        """
        Parses the sports category.
        """
        self.sports = []
        with open(self.sports_fd, 'r') as fd:
            for sport in fd:
                sport = sport.split('\n')[0]
                self.sports.append(sport)

    def __parse_usernames(self):
        """
        Parses the usernames category.
        """
        self.usernames = []
        with open(self.usernames_fd, 'r') as fd:
            for username in fd:
                username = username.split('\n')[0]
                self.usernames.append(username)

    def __parse_vehicles(self):
        """
        Parses the vehicles category.
        """
        self.vehicles = []
        with open(self.vehicles_fd, 'r') as fd:
            for vehicle in fd:
                vehicle = vehicle.split('\n')[0]
                self.vehicles.append(vehicle)
                
    def __parse_categories(self):
        """
        Parses all categories.
        """
        self.name_fd = os.path.dirname(os.path.abspath(__file__))+'/'+self.config['categories']['names']['file']
        self.foods_fd = os.path.dirname(os.path.abspath(__file__))+'/'+self.config['categories']['foods']['file']
        self.dates_fd = os.path.dirname(os.path.abspath(__file__))+'/'+self.config['categories']['dates']['file']
        self.erotics_fd = os.path.dirname(os.path.abspath(__file__))+'/'+self.config['categories']['erotics']['file']
        self.hobbys_fd = os.path.dirname(os.path.abspath(__file__))+'/'+self.config['categories']['hobbys']['file']
        self.keystrokes_fd = os.path.dirname(os.path.abspath(__file__))+'/'+self.config['categories']['keystrokes']['file']
        self.movies_fd = os.path.dirname(os.path.abspath(__file__))+'/'+self.config['categories']['movies']['file']
        self.music_fd = os.path.dirname(os.path.abspath(__file__))+'/'+self.config['categories']['music']['file']
        self.places_fd = os.path.dirname(os.path.abspath(__file__))+'/'+self.config['categories']['place_or']['file']
        self.religions_fd = os.path.dirname(os.path.abspath(__file__))+'/'+self.config['categories']['religion']['file']
        self.sports_fd = os.path.dirname(os.path.abspath(__file__))+'/'+self.config['categories']['sport']['file']
        self.usernames_fd = os.path.dirname(os.path.abspath(__file__))+'/'+self.config['categories']['usernames']['file']
        self.vehicles_fd = os.path.dirname(os.path.abspath(__file__))+'/'+self.config['categories']['vehicle']['file']

        self.__parse_names()
        self.__parse_foods()
        self.__parse_dates()
        self.__parse_erotics()
        self.__parse_hobbys()
        self.__parse_keystrokes()
        self.__parse_movies()
        self.__parse_music()
        self.__parse_places()
        self.__parse_religions()
        self.__parse_sports()
        self.__parse_usernames()
        self.__parse_vehicles()

    def isalphabet(self, char):
        """
        Checks if a character is in the alphabet.

        Parameters
        ----------
        char : str
            Character to check.

        Returns
        -------
        .bool
            True if in alphabet, False otherwise
        """
        if char.isalpha():
            if char in ascii_lowercase:
                return True

        return False        
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
