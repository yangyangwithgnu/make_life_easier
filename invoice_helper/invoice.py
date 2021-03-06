import re
import enum
import datetime
import platform
import subprocess
import chinese_calendar


class Invoice:

    @enum.unique
    class SellerCompany(enum.Enum):
        PetroChina = 0      # 中国石油
        YanchangShell = 1   # 延长壳牌
        Unkown = 2          # 未知

    @staticmethod
    def ___convertPdf2Txt(pdf_path: str) -> str:
        # 执行外部命令 pdftotxt，提取 PDF 中的文本
        if platform.system() == 'Linux':
            return(subprocess.check_output(F'pdftotext "{pdf_path}" -', shell=True).decode('utf-8'))
        elif platform.system() == 'Windows':
            return(subprocess.check_output(F'pdftotext.exe -q "{pdf_path}" -', shell=True, cwd='xpdf-utils-for-win').decode('gbk'))
        else:
            raise(Exception('ERROR! unkown OS.'))

    def __init__(self, pdf_path: str):
        
        self._pdf_path = pdf_path
        
        # 提取 PDF 中的文本
        self._txt = Invoice.___convertPdf2Txt(pdf_path)
        
        # 粗略确认是否为油发票
        self._b_oil_invoice = '成品油' in self._txt
        if not self._b_oil_invoice:
            return
        
        # 识别销售方
        PETERO_CHINA_KW = '中国石油'
        YANCHANG_SHELL_KW = '延长壳牌'
        UNKOWN = '未知油企'
        if PETERO_CHINA_KW in self._txt:
            self._seller_company = Invoice.SellerCompany.PetroChina
            self._seller_company_name = PETERO_CHINA_KW
        elif YANCHANG_SHELL_KW in self._txt:
            self._seller_company = Invoice.SellerCompany.YanchangShell
            self._seller_company_name = YANCHANG_SHELL_KW
        else:
            self._seller_company = Invoice.SellerCompany.Unkown
            self._seller_company_name = UNKOWN
        
        # 获取发票代码
        KEYOWRD = '发票代码'
        begin_idx = self._txt.index(KEYOWRD)
        end_idx = self._txt.index('\n', begin_idx)
        line = self._txt[begin_idx:end_idx]
        (self._invoice_code, *_) = filter(None, re.split(R'[^0-9]', line))
        
        # 获取发票号码
        KEYOWRD = '发票号码'
        begin_idx = self._txt.index(KEYOWRD)
        end_idx = self._txt.index('\n', begin_idx)
        line = self._txt[begin_idx:end_idx]
        (self._invoice_no, *_) = filter(None, re.split(R'[^0-9]', line))
        
        # 获取校验码
        KEYOWRD = '校 验 码'
        begin_idx = self._txt.index(KEYOWRD)
        end_idx = self._txt.index('\n', begin_idx)
        line = self._txt[begin_idx:end_idx]
        self._invoice_checkcode = ''.join(filter(None, re.split(R'[^0-9]', line)))
        
        # 获取开票日期
        # 样例：开票日期: 2019 年02 月27 日
        KEYOWRD = '开票日期'
        begin_idx = self._txt.index(KEYOWRD)
        end_idx = self._txt.index('\n', begin_idx)
        line = self._txt[begin_idx:end_idx]
        (self._year, self._month, self._day, *_) = filter(None, re.split(R'[^0-9]', line))  # 提取年月日，以非数字作为分隔符，等同于 R'[^0-9]'
        
        # 开票日期是否为工作日
        self._b_workday = chinese_calendar.is_workday(datetime.date(int(self._year), int(self._month), int(self._day)))
        
        # 开票日期是否当年
        self._b_curryear = (str(datetime.date.today().year) == self._year)
        
        # 获取发票金额
        KEYOWRD = '小写'
        begin_idx = self._txt.index(KEYOWRD)
        if self._seller_company == Invoice.SellerCompany.YanchangShell or self._seller_company == Invoice.SellerCompany.Unkown:
            # 壳牌样例：
            # （小写）
            #
            # ￥ 230.00
            NEXT_N_NEWLINE = 3
            end_idx = begin_idx
            for i in range(NEXT_N_NEWLINE):
                end_idx = self._txt.index('\n', end_idx + 1)
        elif self._seller_company == Invoice.SellerCompany.PetroChina:
            # 中石油样例：(小写)¥400.00
            end_idx = self._txt.index('\n', begin_idx)
        line = self._txt[begin_idx:end_idx]
        (self._amount, *_) = filter(None, re.split(R'[^0-9.]', line))

    def isValidOilInvoice(self):
        return(self._b_oil_invoice)

    def getPath(self):
        return(self._pdf_path)

    def getTxt(self):
        return(self._txt)

    def getCheckcode(self):
        return(self._invoice_checkcode)

    def getDate(self):
        return(self._year, self._month, self._day)

    def getAmount(self):
        return(self._amount)

    def getSellerCompName(self):
        return(self._seller_company_name)

    def getInvoiceCode(self):
        return(self._invoice_code)

    def getInvoiceNo(self):
        return(self._invoice_no)

    def isValidDate(self):
        # 开票日期只能为当年的工作日
        return(self._b_curryear and self._b_workday)

    def isValidAmount(self):
        # 发票金额不能超过 1000
        AMOUNT_MAX = 1000
        return(float(self._amount) <= AMOUNT_MAX)

    def isValidBuyer(self):
        # 购买方名称必须为中国移动通信集团四川有限公司
        KEYOWRD = '中国移动通信集团四川有限公司'
        return(KEYOWRD in self._txt)

    def isValid(self):
        return(self.isValidOilInvoice() and self.isValidDate() and self.isValidAmount() and self.isValidBuyer())

