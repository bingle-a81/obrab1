# -*- coding: utf-8 -*-
import time
import xlwt
# import logging.config
# from settings import logger_config

#
# logging.config.dictConfig(logger_config)
# logger = logging.getLogger('app_logger.' + __name__)


# ***********************************************************************
# -----------------------------------------------------------------------
#
def main():
    def sber(a: str) -> str:
        lst = a.split('|')
        if '_' in a:
            i=a.index('_')
            k=a[i+1:i+10]
        z=f"insert into lspayment values (gen_id ('lspayment',1)," \
          f"277,{k} ,5,9,24,0,{lst[2]},276,51317,{lst[6]},0.00,'knv_tanja' ,today(),0,1,0,null,null,null)"
        return z

    # book = xlwt.Workbook(encoding="utf-8")
    # sheet1 = book.add_sheet("Python Sheet 1")
    a = ''
    zzz=''
    with open('783D3294O02.BDD', 'r', encoding="cp1251") as f:
        for line in f:
            if all(['BDPD|' in line, 'ПАО СБЕРБАНК//' in line]):
                a = sber(line)
                with open('1', 'a+') as fi:
                    fi.write(a+'\n')
            elif any(['BDPD|' in line, 'BDPL|' in line]):
                with open('2', 'a+') as fi:
                    fi.write(line+'\n')







    # input('введите число ')
    # print('hello world')
    # time.sleep(50)
    # book = xlwt.Workbook(encoding="utf-8")
    #
    # # Add a sheet to the workbook
    # sheet1 = book.add_sheet("Python Sheet 1")
    #
    # cols = ["A", "B", "C", "D", "E"]
    # txt = [0, 1, 2, 3, 4]
    #
    # # Loop over the rows and columns and fill in the values
    # for num in range(5):
    #     row = sheet1.row(num)
    #     for index, col in enumerate(cols):
    #         value = txt[index] + num
    #         row.write(index, value)
    #
    # # Save the workbook
    # book.save("spreadsheet.xls")

    # logger.info("Start ")
    #
    # logger.info("End")


# -----------------------------------------------------------------------
if __name__ == '__main__':
    main()
