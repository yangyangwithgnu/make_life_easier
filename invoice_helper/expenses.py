import os
import subprocess

class Expenses:

    @staticmethod
    def __addTxtToImg(txt: str, img_path: str, new_img_path, font_path: str, font_size: str, x: int, y: int):
        subprocess.check_call(F'convert {img_path} -font {font_path} -pointsize {font_size} -annotate {x}{y} {txt} {new_img_path}', shell=True)

    def __init__(self, invoice_pdf_path: str, bottom_sheet_path: str, font_path: str, amount: str):
        
        # /path/to/myfile.pdf -> /path/to/myfile
        path_n_basename = os.path.splitext(invoice_pdf_path)[0]
        
        # 将电子发票转换为图片
        invoice_img_path = F'{path_n_basename}_invoice.png'
        subprocess.check_call(F'pdftoppm -png -scale-to 900 {invoice_pdf_path} > {invoice_img_path}', shell=True)
        
        # 将电子发票图片覆盖至粘贴底单上
        expenses0_path = F'{path_n_basename}_expenses0.png'
        (x, y) = ('+60', '+120')  # 位置
        subprocess.check_call(F'composite -geometry {x}{y} {invoice_img_path} {bottom_sheet_path} {expenses0_path}', shell=True)
        
        # 填写内容及用途
        expenses1_path = F'{path_n_basename}_expenses1.png'
        (x, y) = ('+968', '+96')  # 位置
        font_size = 26
        txt = '车辆运行费'
        Expenses.__addTxtToImg(txt, expenses0_path, expenses1_path, font_path, font_size, x, y)
        
        # 填写普通发票张数
        expenses2_path = F'{path_n_basename}_expenses2.png'
        (x, y) = ('+1045', '+262')  # 位置
        font_size = 35
        txt = '1'
        Expenses.__addTxtToImg(txt, expenses1_path, expenses2_path, font_path, font_size, x, y)
        
        # 填写普通发票金额
        expenses3_path = F'{path_n_basename}_expenses3.png'
        (x, y) = ('+1035', '+295')  # 位置
        font_size = 27
        Expenses.__addTxtToImg(amount, expenses2_path, expenses3_path, font_path, font_size, x, y)
        
        # 填写经办人
        expenses_path = F'{path_n_basename}_expenses.png'
        (x, y) = ('+990', '+580')  # 位置
        font_size = 27
        txt = '刘德华'
        Expenses.__addTxtToImg(txt, expenses3_path, expenses_path, font_path, font_size, x, y)
        
        os.remove(invoice_img_path)
        os.remove(expenses0_path)
        os.remove(expenses1_path)
        os.remove(expenses2_path)
        os.remove(expenses3_path)
    
