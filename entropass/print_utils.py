from colorama import Fore, Back, Style

START_SUCCESS = Fore.GREEN+Style.BRIGHT+'[*] '+Style.RESET_ALL

def cprint(*args, fore='', back='', style='',
           start=START_SUCCESS, sep=' ', end='\n', **kwargs):
    """
    """
    strargs = sep.join([str(a) for a in args])

    text = start+fore+back+style+strargs+Style.RESET_ALL

    print(text, end=end)

def success(*args, sep=' ', end='\n', **kwargs):
    start = START_SUCCESS
    fore = Fore.WHITE
    style = Style.BRIGHT
    back = Back.GREEN
    cprint(*args, fore=fore, back=back, style=style, start=start,
           sep=sep, end=end)

def warning(*args, sep=' ', end='\n', **kwargs):
    start = Fore.YELLOW+Style.BRIGHT+'[!] '+Style.RESET_ALL
    fore = Fore.WHITE
    style = Style.BRIGHT
    back = Back.YELLOW
    cprint(*args, fore=fore, back=back, style=style, start=start,
           sep=sep, end=end)

def error(*args, sep=' ', end='\n', **kwargs):
    start = Fore.RED+Style.BRIGHT+'[!!!] '+Style.RESET_ALL
    fore = Fore.WHITE
    style = Style.BRIGHT
    back = Back.RED
    cprint(*args, fore=fore, back=back, style=style, start=start,
           sep=sep, end=end)
