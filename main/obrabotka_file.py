# -*- coding: utf-8 -*-
import time
import xlwt
import os
import logging


logging.basicConfig(level=logging.INFO, filename='Log.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('logger')

class Working_with_file:
    def __init__(self,path:str,*args):
        self.path=path
        self.list_file=list(args)

    def search_for_a_file_in_a_folder(self,endswith:str)->str:
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith(endswith):
                    return os.path.join(self.path, file)

    def delete_a_file(self):
        for x in self.list_file:
            if os.path.isfile(os.path.join(self.path,x)):
                os.remove(os.path.join(self.path,x))

class Parsing_file:
    def __init__(self,period):
        self.period=period
        self.book = xlwt.Workbook(encoding="utf-8")
        self.sheet1 = self.book.add_sheet("Таблица 1")
        self.ecxel_id=-1
        self.text_sber=''
        self.text_other_bank=''
        self.text_tinkoff_bank = ''
        self.text_promsviaz=''
        self.counter_shared=0
        self.counter_script_sber = 0
        self.counter_script_tinkoff = 0
        self.counter_script_promsviaz = 0
        self.counter_script_other_bank = 0
        self.counter_excel=0

    def parse_line(self,line:str):
        self.list_line = line.split('|')
        if any(x in line for x in ['BDPD|','BDPL|']):
            self.counter_shared+=1
            self.uin = self.list_line[28]
            if len(self.uin) == 25 and self.uin!='0411530702012000000695906':
                if 'ПАО СБЕРБАНК//' in line:
                    self.list_param_sql=self.parse_sber()
                    if self.list_param_sql[4]!='NONE' and self.list_param_sql[0]!='NONE':
                        self.counter_script_sber += 1
                        a=self.create_script_sql()
                        self.text_sber+=f'{a} \n'
                    else:
                        self.counter_excel += 1
                        self.make_excel_file()
                elif '"ПРОМСВЯЗЬБАНК"' in line:
                    self.list_param_sql=self.parse_promsviaz()
                    if self.list_param_sql[4]!='NONE' and self.list_param_sql[0]!='NONE':
                        self.counter_script_promsviaz += 1
                        a=self.create_script_sql()
                        self.text_promsviaz+=f'{a} \n'
                    else:
                        self.counter_excel += 1
                        self.make_excel_file()
                else:
                    self.list_param_sql = self.parse_other_bank()
                    # print(self.list_param_sql)
                    if self.list_param_sql[4]!='NONE' and self.list_param_sql[0]!='NONE':
                        self.counter_script_other_bank += 1
                        a = self.create_script_sql()
                        self.text_other_bank += f'{a} \n'
                    else:
                        self.counter_excel += 1
                        self.make_excel_file()
            else:
                if '"ТИНЬКОФФ БАНК"' in line and 'ЛС' in line :
                    self.list_param_sql = self.parse_tinkoff()
                    if self.list_param_sql[4]!='NONE' and self.list_param_sql[0]!='NONE':
                        self.counter_script_tinkoff += 1
                        a = self.create_script_sql()
                        self.text_tinkoff_bank += f'{a} \n'
                    else:
                        self.counter_excel += 1
                        self.make_excel_file()
                else:
                    self.counter_excel += 1
                    self.make_excel_file()


    def create_script_sql(self):
        period_1=str(int(self.period)-1)
        return f"insert into lspayment values (gen_id ('lspayment',1)," \
        f"{self.period},{self.list_param_sql[0]} ,{self.list_param_sql[1]},9,24,0,'{self.list_param_sql[2]}',{period_1}," \
               f"{self.list_param_sql[3]},{self.list_param_sql[4]}," \
                f"{self.list_param_sql[5]},'knv_tanja' ,today(),0,1,0,null,null,null);"

    def parse_other_bank(self):
        source_bank = '10'
        face_number = self.seach_in_lsuin()
        payment_date = self.list_line[2]
        pachka='10'+str(payment_date.split('.')[0])
        payment_ = self.list_line[6]
        kbk = self.list_line[32]
        kbk1 = kbk[17:20]
        payment,payment_0=self.check_kbk(kbk1,payment_)
        return [face_number, source_bank, payment_date, pachka, payment, payment_0]

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

    def parse_promsviaz(self):
        source_bank='73'
        face_number=self.seach_in_lsuin()
        payment_date = self.list_line[2]
        pachka ='73'+str(payment_date.split('.')[0])
        payment_ = self.list_line[6]
        kbk = self.list_line[32]
        kbk1 = kbk[17:20]
        payment,payment_0=self.check_kbk(kbk1,payment_)
        return [face_number,source_bank,payment_date,pachka,payment,payment_0]


    def parse_tinkoff(self):
        source_bank = '10'
        a=';'.join([x for x in self.list_line if 'ЛС' in x])
        b=' '.join([x for x in a.split(';') if 'ЛС' in x])
        face_number = b.split()[1]
        payment_date = self.list_line[2]
        pachka='10'+str(payment_date.split('.')[0])
        payment_ = self.list_line[6]
        kbk = self.list_line[32]
        kbk1 = kbk[17:20]
        payment,payment_0=self.check_kbk(kbk1,payment_)
        return [face_number, source_bank, payment_date, pachka, payment, payment_0]

    def check_kbk(self,kbk1,payment_):
        if kbk1=='120':
            return payment_,'0.00'
        elif kbk1=='140':
            return '0.00',payment_
        else:
            return 'NONE', 'NONE'

    def seach_in_lsuin(self):
        result="NONE"
        if os.path.isfile('.//mydir//lsuin.dat'):
            with open('.//mydir//lsuin.dat', 'r', encoding="cp1251") as f:
                for line in f:
                    if self.uin in line:
                        lst = line.split(',')
                        result = lst[2]
                return result
        else:
            logger.info('нет файла lsuin.dat в папке')
            raise FileExistsError('нет файла в папке')


    def make_excel_file(self):
        self.ecxel_id+=1
        row = self.sheet1.row(self.ecxel_id)
        for index, col in enumerate(self.list_line):
            value = col
            row.write(index, value)



# ***********************************************************************
# -----------------------------------------------------------------------
#
def main():
    period = input('Введите какой период закачивать:')
    logger.info('Ввели период :'+period)
    dirs='.\mydir'
    list_files=['script.sql','other_excel.xls']

    w=Working_with_file(dirs,*list_files)
    w.delete_a_file()
    file_data = w.search_for_a_file_in_a_folder(".BDD")
    if file_data==None:
        logger.info('нет файла .BDD в папке')
        raise FileExistsError('нет файла  в папке')
    pf=Parsing_file(period)
    with open(file_data, 'r', encoding="cp1251") as f:
        for line in f:
            pf.parse_line(line)
        pf.book.save(os.path.join(w.path,w.list_file[1]))
        with open(os.path.join(w.path, w.list_file[0]), 'a+') as fi1:
            fi1.write(pf.text_sber)
            fi1.write(pf.text_other_bank)
            fi1.write(pf.text_tinkoff_bank)
            fi1.write(pf.text_promsviaz)
    logger.info('записей обработано:'+str(pf.counter_shared))
    logger.info('записей в скрипте сбер:' + str(pf.counter_script_sber))
    logger.info('записей в скрипте промсвязь:' + str(pf.counter_script_promsviaz))
    logger.info('записей в скрипте тинькоф:' + str(pf.counter_script_tinkoff))
    logger.info('записей в скрипте другие:' + str(pf.counter_script_other_bank))
    script=pf.counter_script_sber+pf.counter_script_promsviaz+pf.counter_script_tinkoff+pf.counter_script_other_bank
    logger.info('Итого в скрипте:' + str(script))
    logger.info('записей в excel:' + str(pf.counter_excel))
    if pf.counter_shared-(script+pf.counter_excel)!=0:
        logger.info('Количество записей не совпадает!')

# -----------------------------------------------------------------------
if __name__ == '__main__':
    main()
