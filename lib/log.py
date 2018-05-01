# -*- coding: utf-8 -*-
import logging
from AutoPlatMS.settings import BASE_DIR

log_level_dic = {
    'debug': logging.DEBUG,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
}

def log(logname, level='info', path=None):
    if path:
        log_path = path + '/'
    else:
        log_path = BASE_DIR

    logging.basicConfig(level=log_level[level],
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        # format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y%m%d %H:%M:%S',
                        filename=log_path+logname,
                        filemode='ab+',
                        )
    return logging.basicConfig