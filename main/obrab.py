# -*- coding: utf-8 -*-
import time
import xlwt
import os
import logging

class Working_with_file:
    def __init__(self,path:str):
        self._path=path
    def search_for_a_file_in_a_folder(self,endswith:str)->str:
        for root, dirs, files in os.walk(self._path):
            for file in files:
                if file.endswith(endswith):
                    return os.path.join(self._path, file)

    def delete_a_file(self,file):
        if os.path.isfile(os.path.join(self._path,file)):
            os.remove(os.path.join(self._path,file))

class Sort_text:
    book=xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Таблица 1")
    id=0
    list_sql_sber = []
    def __init__(self,line:str):
        self.line=line
        self.list_line=line.split('|')
        self.uin = self.list_line[28]
        self.parse_line()

    def parse_line(self):
        if len(self.uin)==25:
            if 'ПАО СБЕРБАНК//' in self.line:
                list_parameters_sql=self.parse_sber()
                self.list_sql_sber.append(list_parameters_sql)
            else:
                print('1')
        else:
            self.make_excel_file()

    def check_kbk(self,kbk1,payment_):
        if kbk1=='120':
            return payment_,'0.00'
        elif kbk1=='140':
            return '0.00',payment_


    def parse_sber(self):
        source_bank='5'
        face_number=self.seach_in_lsuin()
        payment_date = self.list_line[2]
        pachka ='5'+str(payment_date.split('.')[0])+'17'
        payment_ = self.list_line[6]
        kbk = self.list_line[32]
        kbk1 = kbk[17:20]
        payment,payment_0=self.check_kbk(kbk1,payment_)
        return [face_number,source_bank,payment_date,pachka,payment,payment_0]




    def seach_in_lsuin(self):
        with open('.//mydir//lsuin.dat', 'r', encoding="cp1251") as f:
            for line in f:
                if self.uin in line:
                    lst = line.split(',')
                    result = lst[2]
            return result

    def make_excel_file(self):
        Sort_text.id += 1
        row = self.sheet1.row(Sort_text.id)
        for index, col in enumerate(self.list_line):
            value = col
            row.write(index, value)

    def create_script_sql(self,lst):
        print(lst)
        # period_1=str(int(period)-1)
        # return f"insert into lspayment values (gen_id ('lspayment',1)," \
        # f"f,{lst[0]} ,{lst[1]},9,24,0,'fff',{period_1},{lst[3]},{lst[4]}," \
        # f"{lst[5]},'knv_tanja' ,today(),0,1,0,null,null,null);"


# -----------------------
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




# ***********************************************************************
# -----------------------------------------------------------------------
#
def main():
    dirs='.\mydir'
    list_files=['sber.sql','other.sql','other_excel.xls']
    logging.basicConfig(level=logging.INFO, filename='Log.log', filemode='w', format='%(levelname)s - %(message)s')
    logger = logging.getLogger('logger')

    logger.info("Start ")
    period=input('Введите какой период закачивать:')
    logger.info('период:'+period)

    work=Working_with_file(dirs)
    [work.delete_a_file(x) for x in list_files ]

    file_data=work.search_for_a_file_in_a_folder(".BDD")

    text_bdd=[]

    with open(file_data, 'r', encoding="cp1251") as f:
        text_bdd=[line for line in f if any(['BDPD|' in line, 'BDPL|' in line])]
        logger.info('количество строк для сортировки:'+str(len(text_bdd)))
        for x in text_bdd:
            Sort_text(x)
        Sort_text.book.save(os.path.join(dirs,list_files[2]))
        logger.info('количество строк в excel файле:'+str(Sort_text.id))
        with open(os.path.join(dirs, list_files[0]), 'a+') as fi:
            print(Sort_text.list_sql_sber)
            for x in Sort_text.list_sql_sber:
                x.append(period)
                print(x)
                a=Sort_text.create_script_sql('55')
                # fi.write(a+'\n')


        # with open(os.path.join(dirs,list_files[0]), 'a+') as fi:
        #     [fi.write(x) for x in Sort_text.list_sql_sber]





        # for line in f:
        #     if all(['BDPD|' in line, 'ПАО СБЕРБАНК//' in line]):
        #         # , '_' in line
        #         a = sber(line,period)
        #         with open(os.path.join(dirs,list_files[0]), 'a+') as fi:
        #             fi.write(a+'\n')
        #
        #     elif any(['BDPD|' in line, 'BDPL|' in line]):
        #         i += 1
        #         row = sheet1.row(i)
        #         cols = line.split('|')
        #         for index, col in enumerate(cols):
        #             value = col
        #             row.write(index, value)
    # Save the workbook
    # book.save(os.path.join(dirs,list_files[2]))


    #
    logger.info("End")


# -----------------------------------------------------------------------
if __name__ == '__main__':
    main()

