from colorama import Fore, Back, Style

START_SUCCESS = Fore.GREEN+Style.BRIGHT+'[*] '+Style.RESET_ALL # Start of the success messages

def cprint(*args, fore='', back='', style='',
           start=START_SUCCESS, sep=' ', end='\n', **kwargs):
    """
    Print messages with a colour. Resets all colour settings after printing.

    Parameters
    ----------
    args : list
        The text arguments. Can be any type of variable.
    fore : str
        Code to set the colour of the text.
    back : str
        Code to set the colour of the background of the text.
    style : str
        Code to set the style of the text.
    start : str, default = START_SUCCESS
        Starting string of the text.
    sep : str, default = ' '
        Separator for in between arguments.
    end : str, default = \n
        End of the text.
    kwargs : dict
        Unused
    """
    strargs = sep.join([str(a) for a in args])

    text = start+fore+back+style+strargs+Style.RESET_ALL

    print(text, end=end)

def success(*args, sep=' ', end='\n', **kwargs):
    """
    Print a success message with the accompanying colour.

    Parameters
    ----------
    args : list
        The text arguments. Can be any type of variable.
    sep : str, default = ' '
        Separator for in between arguments.
    end : str, default = \n
        End of the text.
    kwargs : dict
        Unused
    """
    start = START_SUCCESS
    fore = Fore.WHITE
    style = Style.BRIGHT
    back = Back.GREEN
    cprint(*args, fore=fore, back=back, style=style, start=start,
           sep=sep, end=end)

def warning(*args, sep=' ', end='\n', **kwargs):
    """
    Print a warning message with the accompanying colour.

    Parameters
    ----------
    args : list
        The text arguments. Can be any type of variable.
    sep : str, default = ' '
        Separator for in between arguments.
    end : str, default = \n
        End of the text.
    kwargs : dict
        Unused
    """
    start = Fore.YELLOW+Style.BRIGHT+'[!] '+Style.RESET_ALL
    fore = Fore.WHITE
    style = Style.BRIGHT
    back = Back.YELLOW
    cprint(*args, fore=fore, back=back, style=style, start=start,
           sep=sep, end=end)

def error(*args, sep=' ', end='\n', **kwargs):
    """
    Print a error message with the accompanying colour.

    Parameters
    ----------
    args : list
        The text arguments. Can be any type of variable.
    sep : str, default = ' '
        Separator for in between arguments.
    end : str, default = \n
        End of the text.
    kwargs : dict
        Unused
    """
    start = Fore.RED+Style.BRIGHT+'[!!!] '+Style.RESET_ALL
    fore = Fore.WHITE
    style = Style.BRIGHT
    back = Back.RED
    cprint(*args, fore=fore, back=back, style=style, start=start,
           sep=sep, end=end)
