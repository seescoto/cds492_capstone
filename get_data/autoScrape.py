# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 15:36:10 2022

@author: seesc

automate scraping and splitting q and a'
not sure if possible since each website is formatted very differently 
will see if possible
"""


def getQandA(url, container, startQMarker, startAMarker,
             answerDeliminator, answerCommand, exclude = None):
    '''
    Parameters
    ----------
    url : string, 
        url of website to get q/a's from.
    container : string
        html container identifier. i.e. div class, anything the questions are
        surrounded by so we can slim down the soup to parse through.
    startQMarker : string
        how to know when a new q/a is happening. i.e. li.
    startAMarker : string
        how to know when the a starts, i.e. strong for <strong> or em for <em>.
    exclude : string, optional
        any strings that, if included in an entry, shouldn't be put into the df.
        ex. if there are headings within the container that begin with the same 
        startQMarker but won't have a q and a to add to the df.
        The default is None.
    answerDeliminator : TYPE
        DESCRIPTION.
    answerCommand : string
        DESCRIPTION.

    Returns
    -------
    None.

    '''

