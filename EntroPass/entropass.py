#!/usr/bin/env python3
from pwd_gen import Pwd_gen
from pwd_score import Pwd_score
from print_utils import *
from colorama import Fore, Style, Back
from threading import Thread
import subprocess
import argparse
import toml
import time
import sys
import os

RED = Fore.RED
GREEN = Fore.GREEN
RESET = Style.RESET_ALL

class EntroPass():
    """
    Main class that loads the configuration and controls all the other classes.
    """
    config_fd = '../config/entropass_conf.toml'
    passwords = []
    scored_pwds = {}
    pass_w_scores = []
    debug = False
    comp_pwd = None
    
    def __init__(self):
        """
        Load configuration file, parse the command line parameters and loads the seed words.
        """
        try:
            self.config = toml.load(self.config_fd)
            success('Loaded configuration from', self.config_fd)
        except Exception as e:
            error('Could not load', self.config_fd,
                  ':', e)
            sys.exit(1)
        parser = argparse.ArgumentParser()
        
        parser.add_argument('-d', '--debug', required=False, action='store_true')
        parser.add_argument('-u', '--update', required=False, action='store_true')
        parser.add_argument('-c', '--compare', required=False, help='Compare password to results')
        args = parser.parse_args()

        if args.update:
            self.run_update()
        
        if args.debug:
            self.debug = True
            
        self.comp_pwd = args.compare
            
        self.gen = Pwd_gen(self.config_fd)
        self.score_pwd = Pwd_score(self.config_fd)
        self.seed_words = [word.lower() for word in self.config['words']['list']]

    def run(self):
        """
        Main function to run the needed functions. Will start by expanding the number of seed words,
        followed by permutations, replacement of characters, removing duplicates, filtering 
        to match patterns, searching for the given password and finally scoring the passwords 
        and limiting number of passwords to a specified number.
        """
        try:

            self.run_seeding_expanse()

            self.run_permutations()
            
            self.run_replace()
                
            self.__rm_duplicates()
            self.run_filter()
            if self.comp_pwd:
                self.__search_for_pwd()

            self.__score_pwds()
        except KeyboardInterrupt:
            warning('Interrupt received, trying to write results to file')
            
        if self.config['print']['shell']:
            self.print_passwords()
            cprint('Generated', self.get_count(), 'passwords.')

        if self.config['results']['max_words']:
            self.__limit_words()
            
        if self.config['print']['file']:
            self.write_t_file()
            cprint('Wrote', self.get_count(), 'passwords to', self.config['print']['fd'])

    def run_update(self):
        """
        Calls the update script to process information in the password directory and generate 
        formats and such in the processed directory.
        """
        cmd = ['../update_psswd_form']
        cprint('Running updates')
        time.sleep(1)
        subprocess.Popen(cmd, stdin=sys.stdin,
                         stdout=sys.stdout,
                         stderr=sys.stderr)
        time.sleep(1)
        cprint('Finished running updates')
        sys.exit(0)
            
    def run_seeding_expanse(self):
        """
        Expand seeding words by generating all possible combinations of upper and lower 
        case characters of the words.
        """
        self.passwords.append(self.seed_words)

        length = len(self.seed_words)
        ctr = length
        for w in self.seed_words:
            res = self.gen.upper_perms(word=w)
            self.passwords.append(res)
            cprint('Expanding seed words: ', length, '->', ctr, end='\r')
            ctr += len(res)
        print()
        
    def run_permutations(self):
        """
        Generates permutations of the seed words and adds them to the password lists.
        """
        cprint('Generating permutations')
        self.passwords.append(self.gen.word_perms(words=self.seed_words,
                                                  nr_in_result=2))

    def run_replace(self):
        """
        Replaces characters in all words with common replacements. Does not overwrite any words,
        but simply adds the new ones.
        """
        cprint('Replacing characters')
        new_psswds = []
        ctr = 0
        for passwords in self.passwords:
            for p in passwords:
                new_psswds += self.gen.rep_cmmn_chars(word=p,
                                                      iterations=4)
                cprint('Resulting passwords:', ctr, end='\r')
                ctr = len(new_psswds)

        print()
        self.passwords.append(new_psswds)

    def run_filter(self):
        """
        Filter the found passwords to those that match the configured patterns.
        """
        cprint('Filtering passwords with patterns:', len(self.passwords), '...')
        self.passwords = self.gen.filter(self.passwords)
        cprint('Filtered passwords with patterns:', len(self.passwords))

    def get_count(self):
        """
        Gets the number of passwords.
        """
        count = len(self.passwords)

        return count

    def print_passwords(self):
        """
        Prints the passwords, separated by a comma.
        """
        print(', '.join(self.passwords))

    def write_t_file(self):
        """
        Writes the passwords to the configured file. Creates the specified directory if it 
        does not exist.
        """
        dir = self.config['print']['dir']
        os.makedirs(dir, exist_ok=True)
        with open(dir+self.config['print']['fd'], 'w') as fd:
            for p in self.passwords:
                fd.write(p+'\n')

    def __rm_duplicates(self):
        """
        Removes the duplicates from the list of passwords.
        """
        cprint('Removing duplicates')
        passwords = []
        for ps in self.passwords:
            passwords += ps
        passwords = list(dict.fromkeys(passwords))
        self.passwords = passwords
        cprint('Remaining:', len(self.passwords))

    def __score_pwds(self):
        """
        Scores the passwords according to the most popular formats, characters and more.
        """
        self.sorted_pwds = {}
        length = len(self.passwords)
        ctr = 1
        try:
            for password in self.passwords:
                if not(type(password) == str):
                    raise ValueError('Could not score passwords, passwords need to be '+\
                                     'of type str:'+str(password))
                cprint('Scoring password', ctr, 'of', length, end='\r')
                self.sorted_pwds[password] = self.score_pwd.score_pwd(pwd=password)
                ctr+=1
        except Exception as e:
            error('Could not complete scoring:', e)

        self.passwords = []
        print()
        cprint('Sorting passwords')

        self.sorted_pwds = self.__sort_scored(self.sorted_pwds)

        try:
            for pwd, score in self.sorted_pwds.items():
                self.passwords.append(pwd)
        except Exception as e:
            error('Could not append sorted scored passwords to list:', e)
            sys.exit(1)

        if self.comp_pwd and self.comp_pwd in self.passwords:
            for i in range(len(self.passwords)):
                if self.passwords[i]==self.comp_pwd:
                    warning('Password is #'+str(i), 'in the scored list.')

    def __sort_scored(self, scored):
        """
        Sorts the scored passwords, from highest score to lowest. Prints an error message and 
        exits if it cannot sort the values.

        Parameters
        ----------
        scored : dict
            A dictionary with the keys being the passwords and the values being the scores.

        Returns
        -------
        srtd : dict
            Same as scored parameter, only sorted from high score to low.
        """
        try:
            srtd = {key: value for  key, value in sorted(scored.items(), key=lambda item: item[1],
                                                         reverse=True)}
            return srtd
        except Exception as e:
            error('Could not sort scored passwords:', e)
            sys.exit(1)

    def __limit_words(self):
        """
        Limits the number of passwords to the specified number. Should be used on scored and 
        sorted password lists, to get only the top scored passwords.
        """
        cprint('Reducing number of passwords to write into file from', len(self.passwords),
               'to', self.config['results']['max_words'])
        self.passwords = self.passwords[:min(self.config['results']['max_words'], len(self.passwords))]

    def __search_for_pwd(self):
        """
        Searches for the specified password in the generated password. Returns once the 
        password was found.
        """
        run_as_str = False
        for pwd in self.passwords:
            if type(pwd) == str:
                run_as_str = True
                break
            elif self.comp_pwd in pwd:
                warning('Found the password in list of', sum([len(p) for p in self.passwords]), 'passwords')
                return

        if run_as_str and self.comp_pwd in self.passwords:
            warning('Found the password in list of', len(self.passwords), 'passwords')
        
if __name__=='__main__':
    ep = EntroPass()
    ep.run()
