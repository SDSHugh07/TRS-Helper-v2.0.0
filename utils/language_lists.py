# /bin/env python
# coding: utf-8

#=================== Description ===================#
#   Lanuage lists used internally by the script to generate reportes
#=================== =========== ===================#

def get_pnmt_cloud_lps():
    return {'PNMT Cloud LPs':[\
            ['French', 'FR', 'EN'],\
            ['French','EN','FR'],\
            ['Italian','IT','EN'],\
            ['Italian','EN','IT'],\
            ['German','DE','EN'],\
            ['German','EN','DE'],\
            ['Spanish','ES','EN'],\
            ['Spanish','EN','ES'],\
            ['Portuguese','PT','EN'],\
            ['Portuguese','EN','PT'],\
            ['Arabic','AR','EN'],\
            ['Arabic','EN','AR'],\
            ['Russian','RU','EN'],\
            ['Russian','EN','RU'],\
            ['Chinese (simplified)','ZH','EN'],\
            ['Chinese (simplified)','EN','ZH'],\
            ['Japanese','JA','EN'],\
            ['Japanese','EN','JA'],\
            ['Korean','KO','EN'],\
            ['Korean','EN','KO']]}

def get_odni_bidir_lps():
    return {'ODNI Bi-Dir LPs': [\
            ['Arabic','AR','EN'],\
            ['Arabic', 'EN', 'AR'],\
            ['Chinese (simplified)','ZH','EN'],\
            ['Chinese (simplified)','EN','ZH'],\
            ['Chinese (traditional)','ZT','EN'],\
            ['Chinese (traditional)','EN','ZT'],\
            ['Dutch','NL','EN'],\
            ['Dutch','EN','NL'],\
            ['French','FR','EN'],\
            ['French','EN','FR'],\
            ['German','DE','EN'],\
            ['German','EN','DE'],\
            ['Greek','EL','EN'],\
            ['Greek','EN','EL'],\
            ['Italian','IT','EN'],\
            ['Italian','EN','IT'],\
            ['Japanese','JA','EN'],\
            ['Japanese','EN','JA'],\
            ['Korean','KO','EN'],\
            ['Korean','EN','KO'],\
            ['Polish','PL','EN'],\
            ['Polish','EN','PL'],\
            ['Portuguese','PT','EN'],\
            ['Portuguese','EN','PT'],\
            ['Russian','RU','EN'],\
            ['Russian','EN','RU'],\
            ['Spanish','ES','EN'],\
            ['Spanish','EN','ES'],\
            ['Swedish','SV','EN'],\
            ['Swedish','EN','SV']]}

def get_odni_monodir_lps():
    return {'ODNI Mono-Dir LPs':[\
            ['Albanian','SQ','EN'],\
            ['Croatian','HR','EN'],\
            ['Czech','CS','EN'],\
            ['Dari','DR','EN'],\
            ['Farsi','FA','EN'],\
            ['Hindi','HI','EN'],\
            ['Pashto','PS','EN'],\
            ['Punjabi (Shahmukhi)','PU','EN'],\
            ['Serbian (Cyrillic)','SR','EN'],\
            ['Slovak','SK','EN'],\
            ['Tajik (Farsi)','TG','EN'],\
            ['Ukrainian','UK','EN'],\
            ['Urdu','UR','EN']]}

def get_other_lps():
    return {'Other V9 Generic/Stable LPs':[\
            ['','DE','FR'],\
            ['','FR','DE'],\
            ['','ES','FR'],\
            ['','FR','ES'],\
            ['','EN','FA'],\
            ['','FI','EN'],\
            ['','EN','FI'],\
            ['','NL','FR'],\
            ['','FR','NL'],\
            ['','TR','EN'],\
            ['','EN','TR'],\
            ['','AR','FR'],\
            ['','KO','VI'],\
            ['','ID','EN'],\
            ['','EN','ID']]}

def get_odni_bidir_lps_enxx():
    return {'Bi-Dir LPs English -> Foreign':[\
            ['Arabic', 'EN', 'AR'],\
            ['Chinese (simplified)','EN','ZH'],\
            ['Chinese (traditional)','EN','ZT'],\
            ['Dutch','EN','NL'],\
            ['French','EN','FR'],\
            ['German','EN','DE'],\
            ['Greek','EN','EL'],\
            ['Italian','EN','IT'],\
            ['Japanese','EN','JA'],\
            ['Korean','EN','KO'],\
            ['Polish','EN','PL'],\
            ['Portuguese','EN','PT'],\
            ['Russian','EN','RU'],\
            ['Spanish','EN','ES'],\
            ['Swedish','EN','SV']]}

def get_odni_bidir_lps_xxen():
    return {'Bi-Dir LPs Foreign -> English':[\
            ['Arabic','AR','EN'],\
            ['Chinese (simplified)','ZH','EN'],\
            ['Chinese (traditional)','ZT','EN'],\
            ['Dutch','NL','EN'],\
            ['French','FR','EN'],\
            ['German','DE','EN'],\
            ['Greek','EL','EN'],\
            ['Italian','IT','EN'],\
            ['Japanese','JA','EN'],\
            ['Korean','KO','EN'],\
            ['Polish','PL','EN'],\
            ['Portuguese','PT','EN'],\
            ['Russian','RU','EN'],\
            ['Spanish','ES','EN'],\
            ['Swedish','SV','EN']]}

def get_odni_monodir_lps_xxen():
    return {'Mono-Dir LPs Foreign -> English':[\
            ['Albanian','SQ','EN'],\
            ['Croatian','HR','EN'],\
            ['Czech','CS','EN'],\
            ['Dari','DR','EN'],\
            ['Farsi','FA','EN'],\
            ['Hindi','HI','EN'],\
            ['Pashto','PS','EN'],\
            ['Punjabi (Gurmukhi)','PA','EN'],\
            ['Punjabi (Shahmukhi)','PU','EN'],\
            ['Urdu','UR','EN'],\
            ['Serbian (Cyrillic)','SR','EN'],\
            ['Serbian (Latin)','SB','EN'],\
            ['Slovak','SK','EN'],\
            ['Tajik (Cyrillic)','TJ','EN'],\
            ['Tajik (Farsi)','TG','EN'],\
            ['Ukrainian','UK','EN']]}
