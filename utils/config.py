# /bin/env python
# coding: utf-8

#=================== Description ===================#
#   Storage location for user provided information.  Intended to allow user for more advanced configuration than available at cli
#=================== =========== ===================#

from uuid import UUID

import logging
logger = logging.getLogger(__name__)

    #####################################################
    ##  Description: User may set API here for convenience not having to type into cli argument
    ##      If API is stored here AND entered at cli, cli input will take precedence
    ##  
    #####################################################
API_KEY = ''

    #####################################################
    ##  Description: Language lists for NMT v9 Report
    ##  
    #####################################################
LANGUAGE_LISTS_V9_FILE_NAME = 'language_lists_v9.json'

    #####################################################
    ##  Description: TRS connection URL
    ##  
    #####################################################
TRS_URL = 'https://trs.systran.net/api/translationResources'

    # NOTSET    0
    # DEBUG     10  Detailed information, typically of interest only when diagnosing problems.
    # INFO      20  Confirmation that things are working as expected.
    # WARNING   30  An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
    # ERROR     40  Due to a more serious problem, the software has not been able to perform some function.
    # CRITICAL  50  A serious error, indicating that the program itself may be unable to continue running.
LOG_FILE_LOG_LEVEL = logging.INFO

    #####################################################
    # Description: Language code list used internally
    #  
    # Peter's suggestions 03/28
    # New -     "SR": "Serbian (Cyrillic/Latin)",
    # Remove -  "SB": "Serbian (Latin)",
    # New -     "TG": "Tajik (Cyrillic)",
    # Remove -  "TG": "Tajik (Farsi)",
    # Remove -  "TJ": "Tajik (Cyrillic)",
    #####################################################
dct_language_codes = {"SQ": "Albanian",
 "AM": "Amharic",
 "AR": "Arabic",
 "AI": "Arabizi",
 "HY": "Armenian",
 "AZ": "Azerbaijani",
 "EU": "Basque",
 "BN": "Bengali",
 "BS": "Bosnian (Latin)",
 "BC": "Bosnian (Cyrillic)",
 "BG": "Bulgarian",
 "CA": "Catalan",
 "KB": "Central Kurdish",
 "ZH": "Chinese (Simplified)",
 "ZT": "Chinese (Traditional)",
 "HR": "Croatian",
 "CS": "Czech",
 "DA": "Danish",
 "DR": "Dari",
 "NL": "Dutch",
 "EN": "English",
 "ET": "Estonian",
 "FI": "Finnish",
 "FR": "French",
 "KA": "Georgian",
 "DE": "German",
 "EL": "Greek",
 "HT": "Haitian",
 "HA": "Hausa",
 "HE": "Hebrew",
 "HI": "Hindi",
 "HU": "Hungarian",
 "IS": "Icelandic",
 "ID": "Indonesian",
 "IT": "Italian",
 "JA": "Japanese",
 "KM": "Khmer",
 "KO": "Korean",
 "KU": "Kurdish",
 "LV": "Latvian",
 "LT": "Lithuanian",
 "MS": "Malay",
 "ML": "Malayalam",
 "MT": "Maltese",
 "NE": "Nepali",
 "KT": "Northern Kurdish",
 "NO": "Norwegian",
 "PS": "Pashto",
 "FA": "Farsi",
 "PL": "Polish",
 "PT": "Portuguese",
 "PA": "Punjabi (Gurmukhi)",
 "PU": "Punjabi (Shahmukhi)",
 "RO": "Romanian",
 "RU": "Russian",
 "SR": "Serbian (Cyrillic)",
 "SB": "Serbian (Latin)",
 "SK": "Slovak",
 "SL": "Slovenian",
 "SO": "Somali",
 "ES": "Spanish",
 "SW": "Swahili",
 "SV": "Swedish",
 "TL": "Tagalog",
 "TG": "Tajik (Farsi)",
 "TJ": "Tajik (Cyrillic)",
 "TA": "Tamil",
 "TE": "Telugu",
 "TH": "Thai",
 "TR": "Turkish",
 "UK": "Ukrainian",
 "UR": "Urdu",
 "VI": "Vietnamese",
 "CY": "Welsh"}
    
#####################################################
##    Description:
##      validate a v4 UUID string
##      Reference - https://gist.github.com/ShawnMilo/7777304
##    Input:
##      string to be tested
##    Return:
##      True/False depending on whether the input string is a valid v4 UUID
#####################################################
def validate_uuid4(uuid_string):

    logger.debug('')

    try:
        val = UUID(uuid_string, version=4)
    except Exception:
        # If it's a value error, then the string 
        # is not a valid hex code for a UUID.
        return False

    return str(val).lower() == uuid_string.lower()


