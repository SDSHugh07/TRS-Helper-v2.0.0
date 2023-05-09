# /bin/env python
# coding: utf-8

#=================== Description ===================#
#   This script lists the latest version # for all ODNI Mono-Directional and Bi-Directional LPs by querying
#       'https://trs.systran.net/api/translationResources' API
#
#=================== ======== ===================#
from __future__ import print_function

import requests
import json
import datetime
import logging
import argparse
import os

from uuid import UUID

from utils.config import validate_uuid4, dct_language_codes, TRS_URL, API_KEY, LOG_FILE_LOG_LEVEL, LANGUAGE_LISTS_V9_FILE_NAME
from utils.classes import LanguagePairMatrix
from utils.reports import ReportAllLPs, ReportBestTRs, ReportTR_ID, ReportNMTv9, print_data_source

#Currently only writes to 'unit_test\<feature_folder>' if enabled 
__ENABLE_TESTING_FEATURES__ = False

    # NOTSET    0
    # DEBUG     10  Detailed information, typically of interest only when diagnosing problems.
    # INFO      20  Confirmation that things are working as expected.
    # WARNING   30  An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
    # ERROR     40  Due to a more serious problem, the software has not been able to perform some function.
    # CRITICAL  50  A serious error, indicating that the program itself may be unable to continue running.
logging.basicConfig(filename='helper.log', level=LOG_FILE_LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(funcName)s() - %(message)s')

# Simple datefmt
# logging.basicConfig(filename='trs_helper.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(funcName)s() - %(message)s', datefmt='%H:%M:%S')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
# formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

logger = logging.getLogger(__name__)

############## Advanced Logger ###############
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(funcName)s:%(message)s')
# file_handler = logging.FileHandler('log.txt')
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)
# logging.config.fileConfig('logging.conf')
##############################################

if __name__ == "__main__":

    now = datetime.datetime.now()
    str_fname_out_root = str(now).replace(' ', '_').replace('-','').replace(':', '-').split('.')[0]
    str_simul_in_fname_src = ''

    parser = argparse.ArgumentParser(description='TRS Helper v2.0')

    parser.add_argument("api_key", type=str, nargs='?', default=API_KEY, help='TRS UUIDv4 API Key')
    parser.add_argument('-d', '--dump', action='store_true', help='Dump TRS data to JSON file')
    parser.add_argument('-a', '--all', action='store_true', help='List all SYSTRAN Generic LPs')
    parser.add_argument('-b', '--best_trs', action='store_true', help='Display best TRs availability list')
    parser.add_argument('-id', '--TR_ID', action='store_true', help='Display Version and TR ID for LPs')
    parser.add_argument('-v9', '--NMT_v9', action='store_true', help='List NMT v9.x LPs')
    parser.add_argument('-p', '--previous_json', type=argparse.FileType('r'), help='Previous TRS JSON dump file to compare.')
    parser.add_argument('-in', '--simulated_input', type=argparse.FileType('r'), help='Process report from a TRS JSON dump file instead of HTTP request to https://trs.systran.net')
    parser.add_argument('-t', '--enable_test', action='store_true', help='Enable Testing Conditions - Developer Use Only')
    
    args = parser.parse_args()
    logger.debug(args)

    if args.enable_test:
        __ENABLE_TESTING_FEATURES__ = args.enable_test
        logger.info('Setting Test Flag - {}'.format(__ENABLE_TESTING_FEATURES__))

    logger.info('Starting TRS Helper'.format())

    if not args.NMT_v9 and args.previous_json:
        logger.critical('Error - Previous TRS JSON dump file can only be provided as simulated input if \'-v9\' option is specified. Exiting...'.format())
        raise SystemExit
        
    if args.simulated_input:
        logger.info('Reading from simulated input data file - \'{}\''.format(args.simulated_input.name))

        str_simul_in_dir_name = os.path.dirname(args.simulated_input.name)
        str_simul_in_fname_w_ext = os.path.basename(args.simulated_input.name)
        str_simul_in_fname_no_ext = os.path.splitext(str_simul_in_fname_w_ext)[0]
        str_simul_in_dir_test_out = str_simul_in_dir_name + '\\test_run_1\\'

        str_simul_in_fname_src = str_simul_in_dir_test_out + str_simul_in_fname_w_ext

        if __ENABLE_TESTING_FEATURES__:
            str_fname_out_root = str_simul_in_dir_test_out + str_simul_in_fname_no_ext 
            logger.info('TEST_FILE_SAVE_LOCATION \'{}.json\''.format(str_fname_out_root))
        else:
            str_fname_out_root = str_simul_in_fname_no_ext
            
        try:
            with open(args.simulated_input.name, 'r') as json_file:
                dct_translation_resources_current = json.load(json_file)

        except json.decoder.JSONDecodeError as ex:
            logging.critical('Invalid JSON file \'{}\' - {}. Exiting...'.format(args.simulated_input.name, ex))
            raise SystemExit

        #validate that the .json actually contains a TRS dump
        try:
            dct_translation_resources_current['translationResources']
        except KeyError as ex:
            logging.critical('Incorrectly formatted TRS JSON dump. \'{}\' does not exist. Exiting...'.format(ex))
            raise SystemExit

        if not (args.dump or args.all or args.best_trs or args.TR_ID or args.NMT_v9):
            logger.info('No report requested.  Exiting...')
            raise SystemExit

    else:
        if args.api_key:
            if(validate_uuid4(args.api_key)):
                logger.info('API Key is valid UUIDv4 - {}'.format(args.api_key))

                if args.dump or args.all or args.best_trs or args.TR_ID or args.NMT_v9:
                    logger.info('Reading live data from TRS - \'{}\''.format(TRS_URL))
                    logger.debug('TIMING - before request.get(\'{}\''.format(TRS_URL))
                    before = datetime.datetime.now()

                    try:
                        response = requests.get(TRS_URL, params={'apikey':args.api_key})
                    except requests.exceptions.ConnectionError as ex:
                        logging.critical("Unable to connect to \'{}\'. Exiting...".format(TRS_URL))
                        raise SystemExit

                    logger.debug('TIMING - after request.get(\'{}\''.format(TRS_URL))
                    after = datetime.datetime.now()
                    delta = after - before
                    logger.debug('TIMING - time pull live data from TRS - {}'.format(delta))
                        
                    try:
                        dct_translation_resources_current = json.loads(response.content)
                    except json.decoder.JSONDecodeError as ex:
                        logging.critical('Invalid JSON file \'{}\' - {}. Exiting...'.format(args.simulated_input.name, ex))
                        raise SystemExit

                    #validate that the .json actually contains a TRS dump
                    try:
                        dct_translation_resources_current['translationResources']
                    except KeyError as ex:
                        logging.critical('Incorrectly formatted TRS JSON dump. \'{}\' does not exist. Exiting...'.format(ex))
                        raise SystemExit

                else:
                    logger.info('No report requested.  Exiting...')
                    raise SystemExit
            else:
                error_msg = 'Error - invalid API Key provided - \'{}\'. Exiting...'.format(args.api_key)
                logger.critical(error_msg)
                raise SystemExit
        else:
            error_msg = 'Error - No API Key provided. Exiting...'.format()
            logger.critical(error_msg)
            raise SystemExit

    obj_language_pair_matrix_all_current = LanguagePairMatrix()

    logger.debug('TIMING - before LanguagePairMatrix.fill_lp_matrix_all() - current'.format())
    
    before = datetime.datetime.now()
    LanguagePairMatrix.fill_lp_matrix_all(obj_language_pair_matrix_all_current, dct_translation_resources_current, dct_language_codes)
    after = datetime.datetime.now()
    delta = after - before
    logger.debug('TIMING - after LanguagePairMatrix.fill_lp_matrix_all() - current'.format())
    logger.debug('TIMING - time to fill matrix - {}'.format(delta))

    if args.dump:
        str_fname_dump = str_fname_out_root + '_trs_dump.json'
        
        with open(str_fname_dump, 'w') as f_dump_file:
            json.dump(dct_translation_resources_current, f_dump_file)
        logger.info('Dumping TRS data to JSON file \'{}\'\n'.format(str_fname_dump))
 
    if args.all:
        logger.info('Running Report: All SYSTRAN Generic LPs'.format())

        str_fname_all = str_fname_out_root + '_all'
        logger.info('Writing report to \'{}.txt/.csv\''.format(str_fname_all))

        with open(str_fname_all + '.txt', 'w') as f_std_out, open(str_fname_all + '.csv', 'w') as f_csv_out:
            print_data_source(args.simulated_input, TRS_URL, str_simul_in_fname_src, f_std_out, f_csv_out)      
            f_std_out.write('\n')
            f_csv_out.write('\n')      

            ReportAllLPs.report_all_lps(obj_language_pair_matrix_all_current, f_std_out, f_csv_out)
        
    if args.best_trs:
        logger.info('Running Report: Best TRs Available'.format())

        str_fname_best_trs = str_fname_out_root + '_best_trs'
        logger.info('Writing report to \'{}.txt/.csv\''.format(str_fname_best_trs))
        
        with open(str_fname_best_trs + '.txt', 'w') as f_std_out, open(str_fname_best_trs + '.csv', 'w') as f_csv_out:
            print_data_source(args.simulated_input, TRS_URL, str_simul_in_fname_src, f_std_out, f_csv_out)   
            f_std_out.write('\n')
            f_csv_out.write('\n')         

            ReportBestTRs.report_best_trs(obj_language_pair_matrix_all_current, f_std_out, f_csv_out)

    if args.TR_ID:
        logger.info('Running Report: Version and TR ID'.format())
        
        str_fname_tr_id = str_fname_out_root + '_tr_id'
        logger.info('Writing report to \'{}.txt/.csv\''.format(str_fname_tr_id))

        with open(str_fname_tr_id + '.txt', 'w') as f_std_out, open(str_fname_tr_id + '.csv', 'w') as f_csv_out:
            print_data_source(args.simulated_input, TRS_URL, str_simul_in_fname_src, f_std_out, f_csv_out)  
            f_std_out.write('\n')
            f_csv_out.write('\n')          

            ReportTR_ID.report_tr_id(obj_language_pair_matrix_all_current, f_std_out, f_csv_out)

    if args.NMT_v9:

        try:
            with open(LANGUAGE_LISTS_V9_FILE_NAME, 'r') as json_file:  
                dct_user_v9_language_lists = json.load(json_file)
        except json.decoder.JSONDecodeError as ex:
            logging.critical("Invalid JSON file \'{}\'' - {}. Exiting...".format(LANGUAGE_LISTS_V9_FILE_NAME, ex))
            raise SystemExit
        except FileNotFoundError as ex:
            logging.critical("{}. Exiting...".format(ex)) 
            raise SystemExit

        if args.simulated_input and __ENABLE_TESTING_FEATURES__:
            str_fname_meta = str_simul_in_dir_test_out + 'SYSTRAN-GENERIC-V9-' + str_simul_in_fname_no_ext + '.txt'
        elif args.simulated_input:
            str_fname_meta = 'SYSTRAN-GENERIC-V9-' + str_simul_in_fname_no_ext + '.txt'
        else:
            str_fname_meta = 'SYSTRAN-GENERIC-V9-' + str_fname_out_root[0:17] + '.txt'

        if args.previous_json:
            logger.info('Running Report: Compare NMT v9.x LPs against previous TRS JSON dump file.'.format())

            try:
                with open(args.previous_json.name, 'r') as json_file:
                    dct_translation_resources_previous = json.load(json_file)
                dct_translation_resources_previous['translationResources']
            except KeyError as ex:
                logging.critical("Incorrectly formatted TRS JSON dump \'{}\'. {} does not exist. Exiting...".format(args.previous_json.name, ex))
                raise SystemExit
            except json.decoder.JSONDecodeError as ex:
                logging.critical("Invalid JSON file \'{}\'' - {}. Exiting...".format(args.previous_json.name, ex))
                raise SystemExit

            obj_language_pair_matrix_all_previous = LanguagePairMatrix()

            logger.debug('TIMING - before LanguagePairMatrix.fill_lp_matrix_all() - Previous'.format())
            
            before = datetime.datetime.now()
            LanguagePairMatrix.fill_lp_matrix_all(obj_language_pair_matrix_all_previous, dct_translation_resources_previous, dct_language_codes)
            after = datetime.datetime.now()
            delta = after - before
            logger.debug('TIMING - after LanguagePairMatrix.fill_lp_matrix_all - Previous'.format())
            logger.debug('TIMING - time to fill matrix - {}'.format(delta))

            str_fname_nmt_v9 = str_fname_out_root + '_nmt_v9_diff'

            with open(str_fname_nmt_v9 + '.txt', 'w') as f_std_out, open(str_fname_nmt_v9 + '.csv', 'w') as f_csv_out, open(str_fname_meta, 'w') as f_meta_out:
                print_data_source(args.simulated_input, TRS_URL, str_simul_in_fname_src, f_std_out, f_csv_out, f_meta_out)

                str_to_write = 'Comparing against previous JSON TRS dump file - {}'.format(args.previous_json.name)
                logger.info(str_to_write.replace(args.previous_json.name, '\'' + args.previous_json.name + '\''))

                logger.info('Writing report to \'{}.txt/.csv\''.format(str_fname_nmt_v9))

                f_meta_out.write('\n')
                f_std_out.write(str_to_write)
                f_std_out.write('\n\n')
                f_csv_out.write(str_to_write)
                f_csv_out.write('\n\n')
                
                ReportNMTv9.report_nmt_v9(obj_language_pair_matrix_all_current, dct_user_v9_language_lists, f_std_out, f_csv_out, obj_lp_matrix_previous = obj_language_pair_matrix_all_previous)
                ReportNMTv9.print_meta(dct_translation_resources_current, f_meta_out)

        else:
            logger.info('Running Report: NMT v9.x LPs'.format())

            str_fname_nmt_v9 = str_fname_out_root + '_nmt_v9'
            logger.info('Writing report to \'{}.txt/.csv\''.format(str_fname_nmt_v9))

            with open(str_fname_nmt_v9 + '.txt', 'w') as f_std_out, open(str_fname_nmt_v9 + '.csv', 'w') as f_csv_out, open(str_fname_meta, 'w') as f_meta_out:
                print_data_source(args.simulated_input, TRS_URL, str_simul_in_fname_src, f_std_out, f_csv_out, f_meta_out)
                f_meta_out.write('\n')
                f_std_out.write('\n')
                f_csv_out.write('\n')

                ReportNMTv9.report_nmt_v9(obj_language_pair_matrix_all_current, dct_user_v9_language_lists, f_std_out, f_csv_out)
                ReportNMTv9.print_meta(dct_translation_resources_current, f_meta_out)

       


        


