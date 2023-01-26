# -*- coding: utf-8 -*-
import time
import xlwt
import os
# import logging.config
# from settings import logger_config

#
# logging.config.dictConfig(logger_config)
# logger = logging.getLogger('app_logger.' + __name__)

def sber(line: str,period:str) -> str:
    face_number='NONE'
    lst = line.split('|')
    if '_' in line:
        i = line.index('_')
        face_number = line[i + 1:i + 10]
    payment_date = lst[2]
    pachka = payment_date.split('.')[0]
    payment=lst[6]

    return f"insert into lspayment values (gen_id ('lspayment',1)," \
        f"{period},{face_number} ,5,9,24,0,'{payment_date}',276,5{pachka}17,{payment}," \
        f"0.00,'knv_tanja' ,today(),0,1,0,null,null,null);"

class Working_with_file:
    def __init__(self,path:str):
        self._path=path
        # self._file=file

    def search_for_a_file_in_a_folder(self)->str:
        for root, dirs, files in os.walk(self._path):
            for file in files:
                if file.endswith(".BDD"):
                    return os.path.join(self._path, file)

    def delete_a_file(self,file):
        if os.path.isfile(os.path.join(self._path,file)):
            os.remove(os.path.join(self._path,file))


# ***********************************************************************
# -----------------------------------------------------------------------
#
def main():
    period=input('Введите какой период закачивать:')
    work=Working_with_file('.\mydir')
    work.delete_a_file('1.sql')
    work.delete_a_file('2.xls')
    file_data=work.search_for_a_file_in_a_folder()
    a = ''
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Python Sheet 1")
    i=0
    with open(file_data, 'r', encoding="cp1251") as f:
        for line in f:
            if all(['BDPD|' in line, 'ПАО СБЕРБАНК//' in line,'_' in line]):
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

    # logger.info("Start ")
    #
    # logger.info("End")


# -----------------------------------------------------------------------
if __name__ == '__main__':
    main()
