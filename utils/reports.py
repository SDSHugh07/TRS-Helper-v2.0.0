# /bin/env python
# coding: utf-8

#=================== Description ===================#
#   File to mainting logic/display/formatting routines for all available reports
#
#=================== =========== ===================#

import logging
import moment

from utils.language_lists import get_odni_bidir_lps_enxx, get_odni_bidir_lps_xxen, get_odni_monodir_lps_xxen
from utils.classes import LanguagePairMatrix, LanguageTechnologyList, TechEnum, LPListEnum

logger = logging.getLogger(__name__)

    #####################################################
    ##    Description: Prints data source, live TRS or simulated data in file, to output files
    ##      
    ##    Input:
    ##      
    ##    Return:
    #####################################################
def print_data_source(b_simulated_input, str_trs_url, str_fname_root, f_std_out, f_csv_out, f_meta_out = None):
                
    if b_simulated_input:
        str_to_write = 'Reading from simulated input data file - {}'.format(str_fname_root)
    else:
        str_to_write = 'Reading live data from TRS - {}'.format(str_trs_url)
    
    if f_meta_out:
	    f_meta_out.write(str_to_write)
	    f_meta_out.write('\n')

    f_std_out.write(str_to_write)
    f_std_out.write('\n')
    f_csv_out.write(str_to_write)
    f_csv_out.write('\n')

    #####################################################
    ##  Description: Class to maintain the 'All LPs' report and all supporting static functions
    ##  
    #####################################################
class ReportAllLPs:

	#####################################################
    ##    Description: kicks off the 'All LPs' report
    ##      
    ##    Input:
    ##      
    ##    Return:
    #####################################################
	@staticmethod
	def report_all_lps(obj_lp_matrix, f_std_out, f_csv_out):
		logger.debug('Starting All LPs Report'.format())
		print('\n')

		ReportAllLPs.print_lp_matrix_all(obj_lp_matrix, f_std_out, f_csv_out)

    #####################################################
    ##    Description: writes the existence matrix of all lps to out files
    ##      
    ##    Input:
    ##      
    ##    Return:
    #####################################################
	@staticmethod
	def print_lp_matrix_all(obj_lp_matrix, f_std_out, f_csv_out):

		logger.debug('')

		str_to_write = 'Language Pairs'

		print(str_to_write)
		f_std_out.write(str_to_write)
		f_std_out.write('\n')
		f_csv_out.write('Language Pairs')
		f_csv_out.write('\n')

		str_to_write = '%s %s %s%s   %s %s %s %s %s %s' % ('{0: <24}'.format('Source Language'), '{0: <24}'.format('Target Language'), '{0: <2}'.format('  '),\
						'{0: <2}'.format('  '), '{0: <7}'.format('RBMT'), '{0: <7}'.format('SMT'), '{0: <7}'.format('Hybrid'), '{0: <7}'.format('v8'),\
						'{0: <7}'.format('v9.x'), '{0: <7}'.format('v9.2'))

		print(str_to_write)
		f_std_out.write(str_to_write)
		f_std_out.write('\n')

		f_csv_out.write('%s, %s, %s, %s, %s, %s, %s, %s, %s, %s' % ('{0: <23}'.format('Source Lanuage'), '{0: <23}'.format('Target Language'), '{0: <2}'.format(' '),\
						'{0: <2}'.format(' '), '{0: <6}'.format('RBMT'), '{0: <6}'.format('SMT'), '{0: <6}'.format('Hybrid'), '{0: <6}'.format('v8'),\
						'{0: <6}'.format('v9.x'), '{0: <6}'.format('v9.2')))
		f_csv_out.write('\n')
		
		label_nmtv9_2 = ''
		label_nmtv9_x = ''
		label_nmtv8 = ''
		label_spe = ''
		label_smt = ''
		label_rbmt = ''

		lp_strings = list(obj_lp_matrix.dct_all_lps_encountered.values())

		#sort inplace on target name first
		lp_strings.sort(key=lambda x: x[1])
		#then sort inplace on source name
		lp_strings.sort(key=lambda x: x[0])

		for lp_string in lp_strings:
			label_nmtv9_2 = ''
			label_nmtv9_x = ''
			label_nmtv8 = ''
			label_spe = ''
			label_smt = ''
			label_rbmt = ''

			lp_code = lp_string[2] + lp_string[3]

			if lp_code in obj_lp_matrix:
				if obj_lp_matrix[lp_code][TechEnum.idx_NMTv9_2.value]:
					label_nmtv9_2 = '=*='
				if obj_lp_matrix[lp_code][TechEnum.idx_NMTv9_x.value]:
					label_nmtv9_x = '=*='
				if obj_lp_matrix[lp_code][TechEnum.idx_NMTv8.value]:
					label_nmtv8 = '=*='
				if obj_lp_matrix[lp_code][TechEnum.idx_SPE.value]:
					label_spe = '=*='
				if obj_lp_matrix[lp_code][TechEnum.idx_SMT.value]:
					label_smt = '=*='
				if obj_lp_matrix[lp_code][TechEnum.idx_RBMT.value]:
					label_rbmt = '=*='

				str_to_write = '%s %s %s%s - , %s, %s, %s, %s, %s, %s, ' % ('{0:.<24}'.format(lp_string[0] + ' '), '{0:.<24}'.format(lp_string[1] + ' '), '{0: <2}'.format(lp_string[2]), '{0: <2}'.format(lp_string[3]),\
				 '{0: ^6}'.format(label_rbmt), '{0: ^6}'.format(label_smt), '{0: ^6}'.format(label_spe), '{0: ^6}'.format(label_nmtv8), '{0: ^6}'.format(label_nmtv9_x), '{0: ^6}'.format(label_nmtv9_2))
				print(str_to_write)
				f_std_out.write(str_to_write)
				f_std_out.write('\n')   

				f_csv_out.write('%s, %s, %s, %s, %s, %s, %s, %s, %s, %s' % ('{0: <23}'.format(lp_string[0]), '{0: <23}'.format(lp_string[1]), lp_string[2], lp_string[3], '{0: ^6}'.format(label_rbmt), '{0: ^6}'.format(label_smt), '{0: ^6}'.format(label_spe),\
				 '{0: ^6}'.format(label_nmtv8), '{0: ^6}'.format(label_nmtv9_x), '{0: ^6}'.format(label_nmtv9_2)))
				f_csv_out.write('\n')
		
    #####################################################
	##  Description: Class to maintain the 'Best TRs' report and all supporting static functions
    ##  
    #####################################################
class ReportBestTRs:

    #####################################################
	##    Description: kicks off the 'Best TRs' report
    ##      
    ##    Input:
    ##      
    ##    Return:
    #####################################################
	@staticmethod
	def report_best_trs(obj_lp_matrix, f_std_out, f_csv_out):
		logger.debug('Starting Best TRs Report'.format())

		str_bidir_key_enxx = 'Bi-Dir LPs English -> Foreign'
		lst_bidir_lps_enxx = get_odni_bidir_lps_enxx()[str_bidir_key_enxx]
		logger.debug('Outputting list - {}'.format(str_bidir_key_enxx))
		ReportBestTRs.print_list(str_bidir_key_enxx, lst_bidir_lps_enxx, obj_lp_matrix, f_std_out, f_csv_out)
		
		str_bidir_key_xxen = 'Bi-Dir LPs Foreign -> English'
		lst_bidir_lps_xxen = get_odni_bidir_lps_xxen()[str_bidir_key_xxen]
		logger.debug('Outputting list - {}'.format(str_bidir_key_xxen))
		ReportBestTRs.print_list(str_bidir_key_xxen, lst_bidir_lps_xxen, obj_lp_matrix, f_std_out, f_csv_out)
		
		lst_language_pair_matrix_existence_bidir_enxx = []
		lst_language_pair_matrix_existence_bidir_enxx = []
		lst_language_pair_matrix_existence_bidir_intersect = []

		lst_language_pair_matrix_existence_bidir_enxx = obj_lp_matrix.generate_existence_matrix(get_odni_bidir_lps_enxx()[str_bidir_key_enxx])
		lst_language_pair_matrix_existence_bidir_xxen = obj_lp_matrix.generate_existence_matrix(get_odni_bidir_lps_xxen()[str_bidir_key_xxen])
		lst_language_pair_matrix_existence_bidir_intersect = LanguagePairMatrix.get_intersection_matrix(lst_language_pair_matrix_existence_bidir_enxx,\
										 																lst_language_pair_matrix_existence_bidir_xxen)
		str_bidir_matrix_header = 'Bi-Dir LPs - Matrix'
		logger.debug('Outputting best matrix - {}'.format(str_bidir_matrix_header))
		ReportBestTRs.print_lp_matrix_best(str_bidir_matrix_header, get_odni_bidir_lps_enxx()[str_bidir_key_enxx], lst_language_pair_matrix_existence_bidir_intersect, f_std_out, f_csv_out)
		
		str_monodir_key_xxen = 'Mono-Dir LPs Foreign -> English'
		logger.debug('Outputting list - {}'.format(str_monodir_key_xxen))
		lst_monodir_lps_xxen = get_odni_monodir_lps_xxen()[str_monodir_key_xxen]
		ReportBestTRs.print_list(str_monodir_key_xxen, lst_monodir_lps_xxen, obj_lp_matrix, f_std_out, f_csv_out)
		
		lst_language_pair_matrix_existence_mono = []

		lst_language_pair_matrix_existence_mono = obj_lp_matrix.generate_existence_matrix(get_odni_monodir_lps_xxen()[str_monodir_key_xxen])

		str_monodir_matrix_header = 'Mono-Dir LPs - Matrix'
		logger.debug('Outputting best matrix - {}'.format(str_monodir_matrix_header))
		ReportBestTRs.print_lp_matrix_best(str_monodir_matrix_header, get_odni_monodir_lps_xxen()[str_monodir_key_xxen], lst_language_pair_matrix_existence_mono, f_std_out, f_csv_out)

    #####################################################
    ##    Description: Prints the list of TR versions for each LP in input list
    ##      
    ##    Input:
    ##      
    ##    Return:
    #####################################################
	@staticmethod
	def print_list(str_header_string, lst_lps, obj_lp_matrix, f_std_out, f_csv_out):

		logger.debug('')

		print(str_header_string)
		f_std_out.write(str_header_string)
		f_std_out.write('\n')

		f_csv_out.write(str_header_string)
		f_csv_out.write('\n')

		str_to_write = '%s %s%s   %s %s %s %s %s %s' % ('{0: <24}'.format(' '), '{0: <2}'.format(' '), '{0: <2}'.format(' '), '{0: <7}'.format('RBMT'),\
					   '{0: <7}'.format('SMT'), '{0: <7}'.format('SPE'), '{0: <7}'.format('v8-LUA'), '{0: <7}'.format('v9.x'), '{0: <7}'.format('v9.2'))
		print(str_to_write)
		f_std_out.write(str_to_write)
		f_std_out.write('\n')

		f_csv_out.write('%s, %s, %s, %s, %s, %s, %s, %s, %s' % ('{0: <23}'.format(' '), '{0: <2}'.format(' '), '{0: <2}'.format(' '), '{0: <6}'.format('RBMT'),\
					   '{0: <6}'.format('SMT'), '{0: <6}'.format('SPE'), '{0: <6}'.format('v8-LUA'), '{0: <6}'.format('v9.x'), '{0: <6}'.format('v9.2')))
		f_csv_out.write('\n')

		for item in lst_lps:
			str_lp_code = item[1] + item [2]

			if str_lp_code in obj_lp_matrix:
				obj_tech_list = obj_lp_matrix[str_lp_code]
			else:
				obj_tech_list = LanguageTechnologyList(str_lp_code)
				logger.debug('obj_lp_matrix[{}] DNE.  Created obj_tech_list - {}'.format(str_lp_code, obj_tech_list))

			str_to_write = '%s %s%s - %s %s %s %s %s %s' % ('{0:.<24}'.format(item[0] + ' '), '{0: <2}'.format(item[1]), '{0: <2}'.format(item[2]),\
						   '{0: <7}'.format(obj_tech_list.version_rbmt + ','), '{0: <7}'.format(obj_tech_list.version_smt + ','),\
						   '{0: <7}'.format(obj_tech_list.version_spe + ','), '{0: <7}'.format(obj_tech_list.version_nmtv8 + ','),\
						   '{0: <7}'.format(obj_tech_list.version_nmtv9_x + ','), '{0: <7}'.format(obj_tech_list.version_nmtv9_2))
			print(str_to_write)
			f_std_out.write(str_to_write)
			f_std_out.write('\n')

			f_csv_out.write('%s, %s, %s, %s, %s, %s, %s, %s, %s' % ('{0: <23}'.format(item[0]), item[1], item[2], '{0: <6}'.format(obj_tech_list.version_rbmt),\
						   '{0: <6}'.format(obj_tech_list.version_smt), '{0: <6}'.format(obj_tech_list.version_spe), '{0: <6}'.format(obj_tech_list.version_nmtv8),\
						   '{0: <6}'.format(obj_tech_list.version_nmtv9_x), '{0: <6}'.format(obj_tech_list.version_nmtv9_2)))
			f_csv_out.write('\n')

		print('\n')
		f_std_out.write('\n')
		f_csv_out.write('\n')

	#####################################################
	##	Description: prints the lp_matrix to out file and std_out
	##	Input:
	## 	  str_header_string - label to name the report
	##	  lst_lp_list - list of Lists of language names and codes of the format:
	##				['Arabic', 'EN', 'AR'],\
	##				['Chinese (simplified)','EN','ZH'],\
	##				...
	##				['Spanish','EN','ES'],\
	##				['Swedish','EN','SV']
	##	  matrix - matrix which holds, for each LP across technology (RBMT, SMT, SPE, NMT...), whether the LP exists or not
	##	  f_std_out/f_csv_out - csv/std out file to be written
	##
	##	Return:
	##	  N/A
	#####################################################
	
	# TODO - print_existenct_matrix_best
	@staticmethod
	def print_lp_matrix_best(str_header_string, lst_lp_list, matrix, f_std_out, f_csv_out):

		logger.debug('')

		print(str_header_string)
		f_std_out.write(str_header_string)
		f_std_out.write('\n')

		f_csv_out.write(str_header_string)
		f_csv_out.write('\n')

		str_to_write = '%s %s%s   %s %s %s %s' % ('{0: <25}'.format(' '), '{0: <2}'.format(' '), '{0: <2}'.format(' '), '{0: <7}'.format('RBMT'),\
										 '{0: <7}'.format('Hybrid'), '{0: <7}'.format('v9.x'), '{0: <7}'.format('v9.2'))
		print(str_to_write)
		f_std_out.write(str_to_write)
		f_std_out.write('\n')

		f_csv_out.write('%s, %s, %s, %s, %s, %s, %s' % ('{0: <23}'.format(' '), '{0: <2}'.format(' '), '{0: <2}'.format(' '), '{0: <6}'.format('RBMT'), '{0: <6}'.format('Hybrid'), '{0: <6}'.format('v9.x'), '{0: <6}'.format('v9.2')))
		f_csv_out.write('\n')

		if len(lst_lp_list) == len(matrix):
			label_nmtv9_2 = ''
			label_nmtv9_x = ''
			label_hybrid = ''
			label_rbmt = ''

			for row, lp in zip(matrix, lst_lp_list):
				label_nmtv9_2 = ''
				label_nmtv9_x = ''
				label_hybrid = ''
				label_rbmt = ''

				if row[TechEnum.idx_NMTv9_2.value]:
					label_nmtv9_2 = '=*='
				elif row[TechEnum.idx_NMTv9_x.value]:
					label_nmtv9_x = '=*='			   
				elif row[TechEnum.idx_SPE.value]:
					label_hybrid = '=*='
				elif row[TechEnum.idx_SMT.value]:
					label_hybrid = '=*='
				elif row[TechEnum.idx_RBMT.value]:
					label_rbmt = '=*='
				
				str_to_write = '%s %s%s - , %s, %s, %s, %s, ' % ('{0:.<24}'.format(lp[0] + ' '), '{0: <2}'.format(lp[1]), '{0: <2}'.format(lp[2]), '{0: ^6}'.format(label_rbmt.replace('=*=', ' * ')), '{0: ^6}'.format(label_hybrid.replace('=*=', ' * ')), '{0: ^6}'.format(label_nmtv9_x.replace('=*=', ' * ')), '{0: ^6}'.format(label_nmtv9_2.replace('=*=', ' * ')))

				print(str_to_write)
				f_std_out.write(str_to_write)
				f_std_out.write('\n')

				f_csv_out.write('%s, %s, %s, %s, %s, %s, %s' % ('{0: <23}'.format(lp[0]), lp[1], lp[2], '{0: ^6}'.format(label_rbmt), '{0: ^6}'.format(label_hybrid), '{0: ^6}'.format(label_nmtv9_x), '{0: ^6}'.format(label_nmtv9_2)))
				f_csv_out.write('\n')
		
		print('\n')
		f_std_out.write('\n')
		f_csv_out.write('\n')

    #####################################################
	##  Description: Class to maintain the 'TR IDs' report and all supporting static functions
    ##  
    #####################################################
class ReportTR_ID:

    #####################################################
	##    Description: kicks off the 'TR ID' report
    ##      
    ##    Input:
    ##      
    ##    Return:
    #####################################################
	@staticmethod
	def report_tr_id(obj_lp_matrix, f_std_out, f_csv_out):
		logger.debug('Starting TR ID Report'.format())

		str_bidir_key_enxx = 'Bi-Dir LPs English -> Foreign'
		lst_bidir_lps_enxx = get_odni_bidir_lps_enxx()[str_bidir_key_enxx]
		logger.debug('Outputting list - {}'.format(str_bidir_key_enxx))
		ReportTR_ID.print_list(str_bidir_key_enxx, lst_bidir_lps_enxx, obj_lp_matrix, f_std_out, f_csv_out)

		str_bidir_key_xxen = 'Bi-Dir LPs Foreign -> English'
		lst_bidir_lps_xxen = get_odni_bidir_lps_xxen()[str_bidir_key_xxen]
		logger.debug('Outputting list - {}'.format(str_bidir_key_xxen))
		ReportTR_ID.print_list(str_bidir_key_xxen, lst_bidir_lps_xxen, obj_lp_matrix, f_std_out, f_csv_out)

		str_monodir_key_xxen = 'Mono-Dir LPs Foreign -> English'
		logger.debug('Outputting list - {}'.format(str_monodir_key_xxen))
		lst_monodir_lps_xxen = get_odni_monodir_lps_xxen()[str_monodir_key_xxen]
		ReportTR_ID.print_list(str_monodir_key_xxen, lst_monodir_lps_xxen, obj_lp_matrix, f_std_out, f_csv_out)

    #####################################################
    ##    Description: Prints the list of TR versions and IDs for each LP in input list
    ##      
    ##    Input:
    ##      
    ##    Return:
    #####################################################
	@staticmethod
	def print_list(str_header_string, lst_lps, obj_lp_matrix, f_std_out, f_csv_out):

		logger.debug('')

		print(str_header_string)
		f_std_out.write(str_header_string)
		f_std_out.write('\n')

		f_csv_out.write(str_header_string)
		f_csv_out.write('\n')

		str_to_write = '%s %s%s   %s %s %s %s %s %s' % ('{0: <24}'.format(' '), '{0: <2}'.format(' '), '{0: <2}'.format(' '), '{0: <46}'.format('RBMT'),\
					   '{0: <46}'.format('SMT'), '{0: <46}'.format('SPE'), '{0: <46}'.format('v8-LUA'), '{0: <46}'.format('v9.x'), '{0: <46}'.format('v9.2'))
		print(str_to_write)
		f_std_out.write(str_to_write)
		f_std_out.write('\n')

		f_csv_out.write('%s, %s, %s, %s, %s, %s, %s, %s, %s' % ('{0: <23}'.format(' '), '{0: <2}'.format(' '), '{0: <2}'.format(' '),\
		 					 '{0: <45}'.format('RBMT'), '{0: <45}'.format('SMT'), '{0: <45}'.format('SPE'), '{0: <45}'.format('v8-LUA'), '{0: <45}'.format('v9.x'), '{0: <45}'.format('v9.2')))
		f_csv_out.write('\n')

		for item in lst_lps:
			str_lp_code = item[1] + item [2]

			if str_lp_code in obj_lp_matrix:
				obj_tech_list = obj_lp_matrix[str_lp_code]
			else:
				obj_tech_list = LanguageTechnologyList(str_lp_code)
				logger.debug('obj_lp_matrix[{}] DNE.  Created obj_tech_list - {}'.format(str_lp_code, obj_tech_list))

			str_to_write = '%s %s%s - %s %s %s %s %s %s' % ('{0:.<24}'.format(item[0] + ' '), '{0: <2}'.format(item[1]),\
						   '{0: <2}'.format(item[2]), '{0: <46}'.format(obj_tech_list.version_rbmt + ' - ' + obj_tech_list.id_rbmt + ','),\
						   '{0: <46}'.format(obj_tech_list.version_smt + ' - ' + obj_tech_list.id_smt + ','),\
						   '{0: <46}'.format(obj_tech_list.version_spe + ' - ' + obj_tech_list.id_spe + ','),\
						   '{0: <46}'.format(obj_tech_list.version_nmtv8 + ' - ' + obj_tech_list.id_nmtv8 +','),\
						   '{0: <46}'.format(obj_tech_list.version_nmtv9_x + ' - ' + obj_tech_list.id_nmtv9_x + ','),\
						   '{0: <46}'.format(obj_tech_list.version_nmtv9_2 + ' - ' + obj_tech_list.id_nmtv9_2))
			print(str_to_write)
			f_std_out.write(str_to_write)
			f_std_out.write('\n')

			f_csv_out.write('%s, %s, %s, %s, %s, %s, %s, %s, %s' % ('{0: <23}'.format(item[0]), item[1], item[2],\
								 '{0: <45}'.format(obj_tech_list.version_rbmt + ' - ' + obj_tech_list.id_rbmt),\
								 '{0: <45}'.format(obj_tech_list.version_smt + ' - ' + obj_tech_list.id_smt),\
								 '{0: <45}'.format(obj_tech_list.version_spe + ' - ' + obj_tech_list.id_spe),\
								 '{0: <45}'.format(obj_tech_list.version_nmtv8 + ' - ' + obj_tech_list.id_nmtv8),\
								 '{0: <45}'.format(obj_tech_list.version_nmtv9_x + ' - ' + obj_tech_list.id_nmtv9_x),\
								 '{0: <45}'.format(obj_tech_list.version_nmtv9_2 + ' - ' + obj_tech_list.id_nmtv9_2)))
			f_csv_out.write('\n')	

		print('\n')
		f_std_out.write('\n')
		f_csv_out.write('\n')	   

    #####################################################
	##  Description: Class to maintain the 'NMT v9' report and all supporting static functions
    ##  
    #####################################################
class ReportNMTv9:

    #####################################################
	##    Description: kicks off the 'NMT v9' report
    ##      
    ##    Input:
    ##      
    ##    Return:
    #####################################################
	@staticmethod
	def report_nmt_v9(obj_lp_matrix_current, dct_usr_v9_lang_lists, f_std_out, f_csv_out, obj_lp_matrix_previous = None):

		logger.debug('Starting NMT v9 Report'.format())

		if obj_lp_matrix_previous:
			b_previous = True
		else:
			b_previous = False

		if b_previous:
			dct_v9_lps_previous = obj_lp_matrix_previous.dct_v9_lps
			dct_v9_lps_current = obj_lp_matrix_current.dct_v9_lps
			dct_v9_lps_all = {**dct_v9_lps_previous, **dct_v9_lps_current}
		else:
			dct_v9_lps_all = obj_lp_matrix_current.dct_v9_lps

		for str_list_name in dct_usr_v9_lang_lists:
			ReportNMTv9.print_report_header(str_list_name, b_previous, f_std_out, f_csv_out)
			ReportNMTv9.print_report_body(str_list_name, obj_lp_matrix_current, dct_v9_lps_all, dct_usr_v9_lang_lists, False, f_std_out, f_csv_out, obj_lp_matrix_previous = obj_lp_matrix_previous)
			print('\n')
			f_std_out.write('\n')
			f_csv_out.write('\n')

		dct_other_v9_lang_lists = ReportNMTv9.process_other_lps(list(dct_v9_lps_all.values()), list(dct_v9_lps_all.values()))
		
		for str_list_name in dct_other_v9_lang_lists:
			ReportNMTv9.print_report_header(str_list_name, b_previous, f_std_out, f_csv_out)
			ReportNMTv9.print_report_body(str_list_name, obj_lp_matrix_current, dct_v9_lps_all, dct_other_v9_lang_lists, True, f_std_out, f_csv_out, obj_lp_matrix_previous = obj_lp_matrix_previous)
			print('\n')
			f_std_out.write('\n')
			f_csv_out.write('\n')

    #####################################################
    ##    Description: Prints to std_out and file_out format
    ##      
    ##    Input:
    ##      
    ##    Return:
    #####################################################
	@staticmethod
	def print_report_header(str_list_label, b_previous, f_std_out, f_csv_out):
		
		logger.debug('')

		print(str_list_label)
		f_std_out.write(str_list_label)
		f_std_out.write('\n')
		f_csv_out.write(str_list_label)
		f_csv_out.write('\n')

		if b_previous:
			str_to_write = '%s %s %s %s %s' % ('{0: <23}'.format(' '), '{0: <2}'.format('  '), '{0: <2}'.format('  '), '{0: >17}'.format('v9.x'), '{0: >17}'.format('v9.2'))

			print(str_to_write)
			f_std_out.write(str_to_write)
			f_std_out.write('\n')
			f_csv_out.write('%s, %s, %s, %s, %s, %s, %s, %s\n' % ('{0: <25}'.format(' '), '{0: <5}'.format(' '), '{0: >8}'.format(''), '{0: <2}'.format(' '), '{0: <8}'.format('v9.x'), '{0: >8}'.format(''),\
			                '{0: <2}'.format(''), '{0: <8}'.format('v9.2')))
			
			str_to_write = '%s %s %s %s %s\n' % ('{0: <26}'.format(' '), '{0: <2}'.format(' '), '{0: <2}'.format(' '), '{0: <17}'.format('(prev)    (curr)'), '{0: <18}'.format('(prev)    (curr)'))

			print(str_to_write)
			f_std_out.write(str_to_write)
			f_std_out.write('\n')
			f_csv_out.write('%s, %s, %s, %s, %s, %s, %s, %s' % ('{0: <25}'.format(' '), '{0: <5}'.format(' '), '{0: <8}'.format('(prev)'), '{0: <2}'.format(' '), '{0: <8}'.format('(curr)'),\
							'{0: <8}'.format('(prev)'), '{0: <2}'.format(' '), '{0: <8}'.format('(curr)')))
			f_csv_out.write('\n')

		else:
			str_to_write = '%s %s%s   %s %s' % ('{0: <25}'.format(' '), '{0: <2}'.format(' '), '{0: <2}'.format(' '), '{0: <7}'.format('v9.x'), '{0: <7}'.format('v9.2'))

			print(str_to_write)
			f_std_out.write(str_to_write)
			f_std_out.write('\n')
			f_csv_out.write('%s, %s, %s, %s' % ('{0: <23}'.format(' '), '{0: <5}'.format(' '), '{0: <6}'.format('v9.x'), '{0: <6}'.format('v9.2')))
			f_csv_out.write('\n')

    #####################################################
    ##    Description: Prints 'NMT v9' report body
    ##      
    ##    Input:
    ##      
    ##    Return:
    #####################################################
	@staticmethod
	def print_report_body(str_list_name, obj_lp_matrix_current, dct_v9_lps, dct_v9_lang_lists, b_dynamic_list, f_std_out, f_csv_out, obj_lp_matrix_previous = None):

		logger.debug('')

		if obj_lp_matrix_previous:
			b_previous = True
		else:
			b_previous = False

		b_found = False

		for lst_lp in dct_v9_lang_lists[str_list_name]:
			b_found = False
			
			if b_dynamic_list:
				str_lp_code = lst_lp[2] + lst_lp[3]
				str_reverse_lp_code = lst_lp[3] + lst_lp[2]
				idx_src_name, idx_tgt_name, idx_src_code, idx_tgt_code = 0, 1, 2, 3
			else:
				str_lp_code = lst_lp[1] + lst_lp[2]
				str_reverse_lp_code = lst_lp[2] + lst_lp[1]
				idx_src_name, idx_src_code, idx_tgt_code = 0, 1, 2

			if 'OTHER Bi-Dir LPs: Foreign <> Foreign' == str_list_name:
				str_leader = lst_lp[idx_src_name] + ' <> ' + lst_lp[idx_tgt_name]
			else:
				str_leader = lst_lp[idx_src_name]


			if obj_lp_matrix_current[str_lp_code][TechEnum.idx_NMTv9_x.value]:
				nmt_v9_x_curr = obj_lp_matrix_current[str_lp_code][TechEnum.idx_NMTv9_x.value].version
			else:
				nmt_v9_x_curr = '     '

			if obj_lp_matrix_current[str_lp_code][TechEnum.idx_NMTv9_2.value]:
				nmt_v9_2_curr = obj_lp_matrix_current[str_lp_code][TechEnum.idx_NMTv9_2.value].version
			else:
				nmt_v9_2_curr = '     '

			if b_previous:
				nmt_v9_x_operator, nmt_v9_x_prev = ReportNMTv9.get_comparison_operator(obj_lp_matrix_previous[str_lp_code][TechEnum.idx_NMTv9_x.value], obj_lp_matrix_current[str_lp_code][TechEnum.idx_NMTv9_x.value])
				nmt_v9_2_operator, nmt_v9_2_prev = ReportNMTv9.get_comparison_operator(obj_lp_matrix_previous[str_lp_code][TechEnum.idx_NMTv9_2.value], obj_lp_matrix_current[str_lp_code][TechEnum.idx_NMTv9_2.value])
			
			if b_previous:
				str_to_print = '%s %s>%s - %s %s %s, %s %s %s' % ('{0:.<24}'.format(str_leader + ' '), '{0: <2}'.format(lst_lp[idx_src_code]), '{0: <2}'.format(lst_lp[idx_tgt_code]), '{0: <6}'.format(nmt_v9_x_prev),\
				    '{0: <2}'.format(nmt_v9_x_operator), '{0: <6}'.format(nmt_v9_x_curr), '{0: <6}'.format(nmt_v9_2_prev), '{0: <2}'.format(nmt_v9_2_operator), '{0: <6}'.format(nmt_v9_2_curr))

				print(str_to_print)
				f_std_out.write(str_to_print)
				f_std_out.write('\n')
				f_csv_out.write('%s, %s>%s, %s, %s, %s, %s, %s, %s' % ('{0: <25}'.format(str_leader), lst_lp[idx_src_code], lst_lp[idx_tgt_code],  '{0: <8}'.format(nmt_v9_x_prev), '{0: <2}'.format(nmt_v9_x_operator),\
				        '{0: <8}'.format(nmt_v9_x_curr), '{0: <8}'.format(nmt_v9_2_prev), '{0: <2}'.format(nmt_v9_2_operator), '{0: <8}'.format(nmt_v9_2_curr)))
				f_csv_out.write('\n')

			else:
				str_to_write = '%s %s>%s - %s %s' % ('{0:.<24}'.format(str_leader + ' '), '{0: <2}'.format(lst_lp[idx_src_code]), '{0: <2}'.format(lst_lp[idx_tgt_code]), '{0: <7}'.format(nmt_v9_x_curr + ','), '{0: <7}'.format(nmt_v9_2_curr))

				print(str_to_write)
				f_std_out.write(str_to_write)
				f_std_out.write('\n')
				f_csv_out.write('%s, %s>%s, %s, %s' % ('{0: <23}'.format(str_leader), lst_lp[idx_src_code], lst_lp[idx_tgt_code], '{0: <6}'.format(nmt_v9_x_curr), '{0: <6}'.format(nmt_v9_2_curr)))
				f_csv_out.write('\n')

			if not b_dynamic_list:
				for item in dct_v9_lang_lists[str_list_name]:
					if str(item[1] + item[2]) == str_reverse_lp_code:
						b_found = True
						break

				if b_found:
					#we found a bi-dir lp, pop it off master list, because the opposite will be popped when we encounter it further on in this list
					dct_v9_lps.pop(str_lp_code, None)
				else:
					if str_reverse_lp_code in dct_v9_lps:
						#opposite was not found in this list, but the opposite is in master list, means it is a true Bi-Dir, but only displayed as a Mono-Dir
						#in this list, so leave it in master list so it can be displayed in OTHER Bi-Dir
						pass
					else:
						#opposite was not in this list, and not in master list, so it's a true Mono, so pop
						dct_v9_lps.pop(str_lp_code, None)

    #####################################################
    ##    Description: returns the comparison operator for 'NMT v9' report
    ##		'->' - a TR has been added to TRS
    ##      '<-' - a TR has been removed from TRS
    ## 		'>>' - TR version has been downgraded
    ##		'<<' - TR version has been upgraded
    ##    Input:
    ##      
    ##    Return:
    #####################################################
	@staticmethod
	def get_comparison_operator(obj_tr_previous, obj_tr_current):
		operator = ''
		previous = '     '

		if not obj_tr_previous and not obj_tr_current:
			operator = ''
			previous = '     '
		elif not obj_tr_previous and obj_tr_current:
			operator = "->"
			previous = '     '
		elif obj_tr_previous and not obj_tr_current:
			operator = "<-"
			previous = obj_tr_previous.version
		elif obj_tr_previous and obj_tr_current:
			if obj_tr_previous > obj_tr_current:
				operator = ">>"
				previous = obj_tr_previous.version
			elif obj_tr_previous < obj_tr_current:
				operator = "<<"
				previous = obj_tr_previous.version
			else:
				operator = "=="
				previous = '     '

		return operator, previous

    #####################################################
    ##    Description: subdivides remaining v9 LPs into 3 lists:
    ## 		* 'OTHER Bi-Dir LPs: Foreign <> English'
	##		* 'OTHER Bi-Dir LPs: Foreign <> Foreign'
	##		* 'OTHER Mono-Dir LPs'
    ##      
    ##    Input:
    ##      
    ##    Return:
    #####################################################

    # TODO use Dictionary
	@staticmethod
	def process_other_lps(lst_other_lps_a, lst_other_lps_b):

		logger.debug('')

		lst_other_lps_a.sort(key=lambda x: x[1])
		lst_other_lps_a.sort(key=lambda x: x[0])

		lst_other_lps_b.sort(key=lambda x: x[1])
		lst_other_lps_b.sort(key=lambda x: x[0])

		# TODO - name this better
		dct_lists = {}

		lst_bidir_xxen = []
		lst_bidir_xxxx = []
		lst_mono = []
		dct_uniques = {}

		for lst_lp_strings_a in lst_other_lps_a:
			b_match = False

			# ENXX
			if lst_lp_strings_a[2] == 'EN':
				for lst_lp_strings_b in lst_other_lps_b:
					if str(lst_lp_strings_a[2] + lst_lp_strings_a[3]).upper() == str(lst_lp_strings_b[3] + lst_lp_strings_b[2]).upper():
						b_match = True
				if not b_match:
					lst_lp_strings_a[0] = lst_lp_strings_a[1]
					lst_mono.append(lst_lp_strings_a)
			# XXEN
			elif lst_lp_strings_a[3] == 'EN':
				for lst_lp_strings_b in lst_other_lps_b:
					if str(lst_lp_strings_a[2] + lst_lp_strings_a[3]).upper() == str(lst_lp_strings_b[3] + lst_lp_strings_b[2]).upper():
						lst_lp_strings_b[0] = lst_lp_strings_a[0]
						lst_lp_strings_b[1] = lst_lp_strings_a[1]
						lst_bidir_xxen.append(lst_lp_strings_a)
						lst_bidir_xxen.append(lst_lp_strings_b)
						b_match = True
				if not b_match:
					lst_mono.append(lst_lp_strings_a)
			# XXXX
			elif 'EN' not in str(lst_lp_strings_a[2]) and 'EN' not in str(lst_lp_strings_a[3]):
				for lst_lp_strings_b in lst_other_lps_b:
					if str(lst_lp_strings_a[2] + lst_lp_strings_a[3]).upper() == str(lst_lp_strings_b[3] + lst_lp_strings_b[2]).upper():
						if str(lst_lp_strings_a[3] + lst_lp_strings_a[2]) not in dct_uniques:
							lst_lp_strings_b[0] = lst_lp_strings_a[0]
							lst_lp_strings_b[1] = lst_lp_strings_a[1]
							lst_bidir_xxxx.append(lst_lp_strings_a)
							lst_bidir_xxxx.append(lst_lp_strings_b)
							dct_uniques[str(lst_lp_strings_a[2] + lst_lp_strings_a[3])] = True
						b_match = True
				if not b_match:
					# Optional to switch the order of SRC/TGT Name
					# temp = lst_lp_strings_a[0]
					# lst_lp_strings_a[0] = lst_lp_strings_a[1]
					# lst_lp_strings_b[1] = temp
					lst_mono.append(lst_lp_strings_a)

		dct_lists['OTHER Bi-Dir LPs: Foreign <> English'] = lst_bidir_xxen
		dct_lists['OTHER Bi-Dir LPs: Foreign <> Foreign'] = lst_bidir_xxxx
		dct_lists['OTHER Mono-Dir LPs'] = lst_mono

		return dct_lists

	@staticmethod
	def print_meta(c, f_meta_out):
		selectedTRs = {}

		for tr in c['translationResources']:
			if 'master' in tr and tr['master'] and \
			   'selectors' in tr and 'owner' in tr['selectors'] and tr['selectors']['owner'] == 'Systran' and \
			      'domain' in tr['selectors'] and tr['selectors']['domain'] == 'Generic' and \
				  'tech' in tr['selectors'] and 'type' in tr['selectors']['tech'] and tr['selectors']['tech']['type'] == 'NMT' and \
				  'description' in tr and 'sourceLanguage' in tr['description'] and 'targetLanguage' in tr['description'] and 'key' in tr['description'] and\
			      'version' in tr and 'major' in tr['version'] and tr['version']['major'] is 9 and \
			      'updatedAt' in tr and 'validated' in tr and 'stages' in tr and 'key' in tr['description']: # and 'stable' in tr['stages'] and tr['validated']:
				updated = tr['updatedAt']

				m=moment.date(updated,'%Y-%m-%dT%H:%M:%SZ')
				if m.year <= 2018 and m.month <= 9: continue

				src = tr['description']['sourceLanguage']
				tgt = tr['description']['targetLanguage']
				ver = '%d.%d.%d' % (tr['version']['major'], tr['version']['minor'], tr['version']['patch'])
				stg = tr['stages']
				val = tr['validated']
				pid = tr['description']['key']
				key = updated
				selectedTRs[key] = (src, tgt, ver, stg, val, pid, updated)

		for idx, key in enumerate(sorted(selectedTRs), start=1):
			tp = selectedTRs[key]
			src=tp[0]
			tgt=tp[1]
			ver=tp[2]
			stg=tp[3]
			val=tp[4]
			pid=tp[5]

			f_meta_out.write('%s\t%d\t%s\t%s\t%s\t%s\t%s\t%s' % (key, idx, src.upper(), tgt.upper(), ver, 'https://trs.systran.net/tr/'+pid, stg, val))
			f_meta_out.write('\n')
