# /bin/env python
# coding: utf-8

#=================== Description ===================#
#   Maintains all classes referenced by this script
#
#=================== =========== ===================#

from distutils.version import LooseVersion
from enum import Enum
from collections import UserList, UserDict
from utils.config import dct_language_codes

import json
import logging
logger = logging.getLogger(__name__)

    #####################################################
    ##  Description: Enumeration for indexing into LanguageTechnologyList
    ##  
    #####################################################
class TechEnum(Enum):
    idx_NONE = -1
    idx_RBMT = 0
    idx_SMT = 1
    idx_SPE = 2
    idx_NMTv8 = 3
    idx_NMTv9_x = 4
    idx_NMTv9_2 = 5

    #####################################################
    ##  Description: Enum to used to index into standardized language display lists
    ##  
    #####################################################
class LPListEnum(Enum):
    idx_SRC_NAME = 0
    idx_TGT_NAME = 1
    idx_SRC_CODE = 2
    idx_TGT_CODE = 3
    
    #####################################################
    ##  Description: Represents a TranslationResource record with all pertinent information needed by this script
    ##  
    #####################################################
class TranslationResource:

    def __init__(self, version, tr_id, src_name, tgt_name, src_code, tgt_code, idx_tech):
        self.version = version
        self.tr_id = tr_id
        self.src_name = src_name
        self.tgt_name = tgt_name
        self.src_code = src_code
        self.tgt_code = tgt_code
        self.idx_tech = idx_tech

        # logger.debug('TranslationResource Created: {}'.format(self.__repr__()))

    def __lt__(self, other):
        return LooseVersion(self.version) < LooseVersion(other.version)

    def __le__(self, other):
        return LooseVersion(self.version) <= LooseVersion(other.version)

    def __eq__(self, other):
        return LooseVersion(self.version) == LooseVersion(other.version)

    def __ge__(self, other):
        return LooseVersion(self.version) >= LooseVersion(other.version)

    def __gt__(self, other):
        return LooseVersion(self.version) > LooseVersion(other.version)

    def __repr__(self):
        return "TranslationResource({}, {}, {}, {}, {}, {}, {})".format(self.version, self.tr_id, self.src_name, self.tgt_name, self.src_code, self.tgt_code, self.idx_tech)

    def __str__(self):
        return "TR({}, {}, v{})".format(self.src_code + self.tgt_code, self.idx_tech, self.version)

    def __del__(self):
        pass
        # logger.debug('TranslationResource Destructor: {}'.format(self.__repr__()))

    #####################################################
    ##  Description: Represents an LP.  Inherits 'UserList' so can be iterated and indexed like a regular list.
    ##      Each LanguageTechnologyList has slots to store a TranslationResource object.  One for each of currently maintained 
    ##          language technologies - RBMT, SMT, SPE, NMT v8-lua, NMT v9.0, NMT v9.2
    ##      WARNING!!! - should not insert into this list other than with the over-ridden function __setitem__().
    ##  
    #####################################################
class LanguageTechnologyList(UserList):
    
    def __init__(self, str_lp_code, info = [None, None, None, None, None, None]):
        UserList.__init__(self, info)
        self.str_lp_code = str_lp_code
        logger.debug('LanguageTechnologyList Created: {}'.format(self.__repr__()))

    #####################################################
    ##    Description: insert function overridden from super class UserList
    ##      Only adds the new TR if it is higher version number than current TR
    ##
    ##    Input:
    ##      
    ##    Return:
    #####################################################
    def __setitem__(self, idx_tech, obj_tr):
        b_was_added = False

        if not self.data[idx_tech.value]:
            self.data[idx_tech.value] = obj_tr
            b_was_added = True
            logger.debug('TR 1st inserted to LPMatrix: {}'.format(obj_tr.__repr__()))
        elif self.data[idx_tech.value] < obj_tr:
            logger.debug('TR replacing in LPMatrix: old TR - {}, new TR - {}'.format(self.data[idx_tech.value].__repr__(), obj_tr.__repr__()))
            self.data[idx_tech.value] = obj_tr
            b_was_added = True
            
        return b_was_added

    @property
    def lp_code(self):
        return self.str_lp_code

    @property
    def version_rbmt(self):
        if self.data[TechEnum.idx_RBMT.value]:
            return self.data[TechEnum.idx_RBMT.value].version
        else:
            return 'xxx'

    @property
    def version_smt(self):
        if self.data[TechEnum.idx_SMT.value]:
            return self.data[TechEnum.idx_SMT.value].version
        else:
            return 'xxx'        

    @property
    def version_spe(self):
        if self.data[TechEnum.idx_SPE.value]:
            return self.data[TechEnum.idx_SPE.value].version
        else:
            return 'xxx'    

    @property
    def version_nmtv8(self):
        if self.data[TechEnum.idx_NMTv8.value]:
            return self.data[TechEnum.idx_NMTv8.value].version
        else:
            return 'xxx'            

    @property
    def version_nmtv9_x(self):
        if self.data[TechEnum.idx_NMTv9_x.value]:
            return self.data[TechEnum.idx_NMTv9_x.value].version
        else:
            return 'xxx'            

    @property
    def version_nmtv9_2(self):
        if self.data[TechEnum.idx_NMTv9_2.value]:
            return self.data[TechEnum.idx_NMTv9_2.value].version
        else:
            return 'xxx'  

    @property
    def id_rbmt(self):
        if self.data[TechEnum.idx_RBMT.value]:
            return self.data[TechEnum.idx_RBMT.value].tr_id
        else:
            return 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'

    @property
    def id_smt(self):
        if self.data[TechEnum.idx_SMT.value]:
            return self.data[TechEnum.idx_SMT.value].tr_id
        else:
            return 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'        

    @property
    def id_spe(self):
        if self.data[TechEnum.idx_SPE.value]:
            return self.data[TechEnum.idx_SPE.value].tr_id
        else:
            return 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'    

    @property
    def id_nmtv8(self):
        if self.data[TechEnum.idx_NMTv8.value]:
            return self.data[TechEnum.idx_NMTv8.value].tr_id
        else:
            return 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'            

    @property
    def id_nmtv9_x(self):
        if self.data[TechEnum.idx_NMTv9_x.value]:
            return self.data[TechEnum.idx_NMTv9_x.value].tr_id
        else:
            return 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'            

    @property
    def id_nmtv9_2(self):
        if self.data[TechEnum.idx_NMTv9_2.value]:
            return self.data[TechEnum.idx_NMTv9_2.value].tr_id
        else:
            return 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx' 

    def __repr__(self):

        str_output = "["

        for tr in self.data:
            if tr:
                str_output += tr.__repr__()
            else:
                str_output += 'None'
            str_output += ', '

        str_output += ']'

        return "LanguageTechnologyList({}, {})".format(self.str_lp_code, str_output.replace(", ]", "]"))

    def __str__(self):

        str_output = "["

        for tr in self.data:
            if tr:
                str_output += str(tr)
            else:
                str_output += 'None'
            str_output += ', '

        str_output += "]"

        return "TechList: {} {}".format(self.str_lp_code, str_output.replace(", ]", "]"))

    def __del__(self):
        # pass
        logger.debug('LanguageTechnologyList Destructor: {}'.format(self.__repr__()))

    #####################################################
    ##  Description: Matrix of LP x Technology to maintain highest version TRs
    ##  
    #####################################################
class LanguagePairMatrix(UserDict):
    
    def __init__(self):
        UserDict.__init__(self)
        self._dct_all_lps_encountered = {}
        logger.debug('LanguagePairMatrix Created')
    
    #####################################################
    ##    Description: insert function overridden from super class UserDict
    ##      Only adds the new TR if it is higher version number than current TR
    ##
    ##        RBMT 
    ##            'redhat-7' == tr['description']['distrib']
    ##            'RBMT' == tr['selectors']['tech']['type']
    ##
    ##      SMT
    ##          'all' == tr['description']['distrib']:
    ##            'SMT' == tr['selectors']['tech']['type']:
    ##
    ##        SPE
    ##            'all' == tr['description']['distrib']:
    ##            'SPE' == tr['selectors']['tech']['type']:
    ##
    ##        NMT v8-lua
    ##            'redhat-7' == tr['description']['distrib']
    ##            2 == tr['version']['major'] or 3 == tr['version']['major']
    ##
    ##        NMT v9.x
    ##            'redhat-7' == tr['description']['distrib']
    ##            9 == tr['version']['major']:
    ##            2 > tr['version']['minor']:
    ##
    ##        NMT v9.2
    ##            'redhat-7' == tr['description']['distrib']
    ##            9 == tr['version']['major']:
    ##            2 == tr['version']['minor']:
    ##
    ##
    ##    Input:
    ##      
    ##    Return:
    #####################################################
    def __setitem__(self, key, tr):
        idx_technology = TechEnum.idx_NONE
        b_add = False
        b_was_added = False
        # b_lp_absent = False 
        obj_new_tr = None

        str_src_lang_code = tr['description']['sourceLanguage'].upper()
        str_tgt_lang_code = tr['description']['targetLanguage'].upper()
        str_lp_code = str_src_lang_code + str_tgt_lang_code

        if dct_language_codes[str_src_lang_code]:
            str_src_lang_name = dct_language_codes[str_src_lang_code]
        else:
            str_src_lang_name = 'Unknown Language (%s): ' % str_src_lang_code

        if dct_language_codes[str_tgt_lang_code]:
            str_tgt_lang_name = dct_language_codes[str_tgt_lang_code]
        else:
            str_tgt_lang_name = 'Unknown Language (%s): ' % str_tgt_lang_code

        version = ('%d.%d.%d' % (tr['version']['major'], tr['version']['minor'], tr['version']['patch']))
        tr_id = ('%s' % (tr['description']['key']))

        #RBMT and NMT cases are expected to be 'redhat-7' distribution
        if 'redhat-7' == tr['description']['distrib']:
            if 'RBMT' == tr['selectors']['tech']['type']:
                b_add = True
                idx_technology = TechEnum.idx_RBMT

            elif 'NMT' == tr['selectors']['tech']['type']:
                if 2 == tr['version']['major'] or 3 == tr['version']['major']:
                    b_add = True
                    idx_technology = TechEnum.idx_NMTv8
                
                elif 9 == tr['version']['major']:
                    if 2 == tr['version']['minor']:
                        b_add = True
                        idx_technology = TechEnum.idx_NMTv9_2
                    elif 2 > tr['version']['minor']:
                        b_add = True
                        idx_technology = TechEnum.idx_NMTv9_x
            
        #SMT and SPE cases are expected to be 'all' distribution
        elif 'all' == tr['description']['distrib']:
            if 'SMT' == tr['selectors']['tech']['type']:
                b_add = True
                idx_technology = TechEnum.idx_SMT
                
            elif 'SPE' == tr['selectors']['tech']['type']:
                b_add = True
                idx_technology = TechEnum.idx_SPE
                
        if b_add:
            obj_new_tr = TranslationResource(version, tr_id, str_src_lang_name, str_tgt_lang_name, str_src_lang_code, str_tgt_lang_code, idx_technology)

            if str_lp_code not in self.data:
                # b_lp_absent = True
                self.data[str_lp_code] = LanguageTechnologyList(str_lp_code)
                # logger.debug('TechList Absent - adding {}'.format(self.data[str_lp_code].__repr__()))

            b_was_added = self.data[str_lp_code][idx_technology] =  obj_new_tr

            if b_was_added:
                self._dct_all_lps_encountered[str_lp_code] = [str_src_lang_name, str_tgt_lang_name, str_src_lang_code, str_tgt_lang_code]
                # logger.debug('TR Added to LP Matrix: {}'.format(str(obj_new_tr)))
        
        return b_was_added
    
    @property
    def dct_all_lps_encountered(self):
        return self._dct_all_lps_encountered

    @property
    def dct_v9_lps(self):

        _dct_v9_lps = {}

        for str_lp_code in self.data:
            if self.data[str_lp_code][TechEnum.idx_NMTv9_x.value] or self.data[str_lp_code][TechEnum.idx_NMTv9_2.value]:
                _dct_v9_lps[str_lp_code] = self._dct_all_lps_encountered[str_lp_code]

        return _dct_v9_lps

    #####################################################
    ##    Description: returns a binary representation of it's underlying LP matrix[][].
    ##      '1' - TR for LP/Technology exists
    ##      '0' - TR for LP/Technology DNE
    ##      
    ##    Input:
    ##      
    ##    Return:
    #####################################################
    def generate_existence_matrix(self, lst_lp_list):

        logger.debug('')
        
        lst_existence_row = []
        lst_existence_col = []

        for lp in lst_lp_list:
            str_lp_code = lp[1] + lp[2]

            lst_existence_col = []
            
            if str_lp_code in self.data:
                obj_tech_list = self.data[str_lp_code]
            else:
                obj_tech_list = LanguageTechnologyList(str_lp_code)
                logger.debug('data[{}] DNE.  Created obj_tech_list - {}'.format(str_lp_code, obj_tech_list))

            for obj_tech in obj_tech_list:
                if obj_tech:
                    lst_existence_col.append(1)
                else:
                    lst_existence_col.append(0)


            if lst_existence_col[TechEnum.idx_SMT.value] or lst_existence_col[TechEnum.idx_SPE.value]:
                lst_existence_col[TechEnum.idx_SMT.value] = 1
                lst_existence_col[TechEnum.idx_SPE.value] = 1

            lst_existence_row.append(lst_existence_col)
            
        return lst_existence_row

    #TODO - Pythonize
    #####################################################
    ##    Description: return intersection matrix of two existence matrices
    ##      
    ##    Input:
    ##      
    ##    Return:
    #####################################################
    @staticmethod
    def get_intersection_matrix(lst_matrix_a, lst_matrix_b):
        
        logger.debug('')

        b_same_rows = True
        b_same_cols = True

        num_cols = 0
        num_rows = 0

        lst_output_matrix = []

        if len(lst_matrix_a) == len(lst_matrix_b):
            num_rows = len(lst_matrix_a)
        else:
            b_same_rows = False

        if b_same_rows:
            for i in range(num_rows):
                if len(lst_matrix_a[i]) != len(lst_matrix_b[i]):
                    b_same_cols = False

            if (b_same_rows and b_same_cols):
                
                num_cols = len(lst_matrix_a[0])

                lst_output_matrix = [[0 for x in range(num_cols)] for y in range(num_rows)]

                for i in range(num_rows):
                    for j in range(num_cols):
                        lst_output_matrix[i][j] = (lst_matrix_a[i][j] and lst_matrix_b[i][j])
        else:
            logger.error('Matrices are not the same size.  Cannot generate intersection matrix.')

        return lst_output_matrix

    #####################################################
    ##    Description: fills the LanguagePairMatrix
    ##      Filters out TRs that are not 'master', 'runnable', 'stages' = 'stable', and 'validated'
    ##      
    ##    Input:
    ##      
    ##    Return:
    #####################################################
    @staticmethod
    def fill_lp_matrix_all(obj_lp_matrix_to_fill, dct_all_trs, dct_lang_codes):

        logger.debug('')

        lst_dbg_tr_list = []
            
        for itr_tr in dct_all_trs['translationResources']:

    ###################### Test Block - Dump out unfiltered TR JSON
            # if 'description' in itr_tr and  'selectors' in itr_tr and 'domain' in itr_tr['selectors']\
            #    and 'Generic' == itr_tr['selectors']['domain'] and 'owner' in itr_tr['selectors'] and 'Systran' == itr_tr['selectors']['owner']\
            #    and 'sourceLanguage' in itr_tr['description'] and 'targetLanguage' in itr_tr['description']:

            #     if 'redhat-7' == itr_tr['description']['distrib'] and 'NMT' == itr_tr['selectors']['tech']['type'] and 9 == itr_tr['version']['major'] and 2 > itr_tr['version']['minor']:
            #         str_src_lang_code = itr_tr['description']['sourceLanguage'].upper()
            #         str_tgt_lang_code = itr_tr['description']['targetLanguage'].upper()
            #         str_lp_code = str_src_lang_code + str_tgt_lang_code

            #         if 'KOVI' == str_lp_code:
            #             lst_dbg_tr_list.append(itr_tr)

    ######################

            if 'master' in itr_tr and itr_tr['master'] and 'description' in itr_tr and 'runnable' in itr_tr['description'] and itr_tr['description']['runnable']\
               and 'validated' in itr_tr and itr_tr['validated'] and 'stages' in itr_tr and 'stable' in itr_tr['stages'] and 'selectors' in itr_tr and 'domain' in itr_tr['selectors']\
               and 'Generic' == itr_tr['selectors']['domain'] and 'owner' in itr_tr['selectors'] and 'Systran' == itr_tr['selectors']['owner']\
               and 'sourceLanguage' in itr_tr['description'] and 'targetLanguage' in itr_tr['description']:

                str_src_lang_code = itr_tr['description']['sourceLanguage'].upper()
                str_tgt_lang_code = itr_tr['description']['targetLanguage'].upper()
                str_lp_code = str_src_lang_code + str_tgt_lang_code

                obj_lp_matrix_to_fill[str_lp_code] = itr_tr

    ###################### Test Block - Dump out unfiltered TR JSON
        # with open('KOVI_TR.json', 'w') as outfile:
        #     json.dump(lst_dbg_tr_list, outfile, indent = 2)
    ######################

    #####################################################
    ##    Description: very rudimentary print function to print all TRs in LP Matrix
    ##      should only be used for testing purposes in it's current form
    ##      
    ##    Input:
    ##      
    ##    Return:
    #####################################################
    @staticmethod
    def print_test_matrix(lp_matrix):
        
        logger.debug('')

        str_out = ""

        for row in lp_matrix.data.values():
            str_out = row.str_language_pair + ' - '
            for col in row.lst_language_technologies:
                if col:
                    str_out += (col.version + ', ')
                else:
                    str_out += 'None, '

            print(str_out)
            str_out = ""

    def __del__(self):
        logger.debug('LanguagePairMatrix Destructor'.format())