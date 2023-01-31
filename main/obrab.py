# -*- coding: utf-8 -*-
import time
import xlwt
import os
import logging.config
import logging
from logging import StreamHandler, Formatter, LogRecord

class MegaHandler(logging.Handler):
    def __init__(self, filename):
        logging.Handler.__init__(self)
        self.filename = filename

    def emit(self, record):
        message = self.format(record)
        with open(self.filename, 'a') as file:
            file.write(message + '\n')


logger_config = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'std_format': {
            'format': '{asctime} - {levelname} - {name} - {message}',
            'style': '{'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'std_format',
            # 'filters': ['new_filter'],
        },
        'file': {
            '()': MegaHandler,
            'level': 'INFO',
            'filename': 'debug.log',
            'formatter': 'std_format',
        },
    },
    'loggers': {
        'app_logger': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            # 'propagate': False
        },
        'json_logger': {
            'level': 'DEBUG',
            'handlers': ['console','file'],
        },
    },
}
logging.config.dictConfig(logger_config)
logger = logging.getLogger('app_logger.' + __name__)
def seach_in_lsuin(uin:str):
    with open('.//mydir//lsuin.dat', 'r', encoding="cp1251") as f:
        for line in f:
            if uin in line:
                lst=line.split(',')
                result=lst[2]
        return result


def sber(line: str,period:str) -> str:
    face_number='NONE'
    lst = line.split('|')
    if '_' in line:
        i = line.index('_')
        face_number = line[i + 1:i + 10]
    else:
        uin=lst[28]
        face_number=seach_in_lsuin(uin)
    payment_date = lst[2]
    pachka = payment_date.split('.')[0]
    payment=lst[6]
    period_1=int(period)-1
    # print(len(lst))
    kbk=lst[32]
    kbk1=kbk[17:20]
    if kbk1=='120':
        result=f"insert into lspayment values (gen_id ('lspayment',1)," \
        f"{period},{face_number} ,5,9,24,0,'{payment_date}',{period_1},5{pachka}17,{payment}," \
        f"0.00,'knv_tanja' ,today(),0,1,0,null,null,null);"
    elif kbk1=='140':
        result=f"insert into lspayment values (gen_id ('lspayment',1)," \
        f"{period},{face_number} ,5,9,24,0,'{payment_date}',{period_1},5{pachka}17,0.00," \
        f"{payment},'knv_tanja' ,today(),0,1,0,null,null,null);"
    else:
        result=f'PROVER KBK(120-140): UIN-{face_number}'
    return result

class Working_with_file:
    def __init__(self,path:str):
        self._path=path
        # self._file=file

    def search_for_a_file_in_a_folder(self,endswith:str)->str:
        for root, dirs, files in os.walk(self._path):
            for file in files:
                if file.endswith(endswith):
                    return os.path.join(self._path, file)

    def delete_a_file(self,file):
        if os.path.isfile(os.path.join(self._path,file)):
            os.remove(os.path.join(self._path,file))


# ***********************************************************************
# -----------------------------------------------------------------------
#
def main():
    logger.info("Start ")
    period=input('Введите какой период закачивать:')
    work=Working_with_file('.\mydir')
    work.delete_a_file('1.sql')
    work.delete_a_file('2.xls')
    file_data=work.search_for_a_file_in_a_folder(".BDD")
    a = ''
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Таблица 1")
    i=0
    with open(file_data, 'r', encoding="cp1251") as f:
        for line in f:
            if all(['BDPD|' in line, 'ПАО СБЕРБАНК//' in line]):
                # , '_' in line
                a = sber(line,period)
                with open('.//mydir//1.sql', 'a+') as fi:
                    fi.write(a+'\n')

            elif any(['BDPD|' in line, 'BDPL|' in line]):
                i += 1
                row = sheet1.row(i)
                cols = line.split('|')
                for index, col in enumerate(cols):
                    value = col
                    row.write(index, value)
    # Save the workbook
    book.save(".//mydir//2.xls")


    #
    logger.info("End")


# -----------------------------------------------------------------------
if __name__ == '__main__':
    main()

