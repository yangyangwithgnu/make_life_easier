import os
import fitz
from PIL import Image, ImageFont, ImageDraw


class Expenses:

    @staticmethod
    def ___addTxtToImg(txt: str, img: Image, font_path: str, font_size: int, x: int, y: int):
        font = ImageFont.truetype(font_path, font_size)
        ImageDraw.Draw(img).text((x, y), txt, font=font, fill=(0, 0, 0))

    def __init__(self, invoice_pdf_path: str, bottom_sheet_path: str, font_path: str, amount: str, name: str):
        
        # /path/to/myfile.pdf -> /path/to/myfile
        path_n_basename = os.path.splitext(invoice_pdf_path)[0]
        
        # 将电子发票转换为图片
        invoice_img_path = F'{path_n_basename}_invoice.png'
        doc = fitz.open(invoice_pdf_path)
        matrix = fitz.Matrix(1.45, 1.45)  # 缩放比例
        pixs = doc[0].getPixmap(matrix=matrix, alpha=False)  # 获取 PDF 第一页的所有像素
        pixs.writePNG(invoice_img_path)  # 将所有像素写入图片文件
        doc.close()
        
        # 粘贴底单信息填写
        with Image.open(invoice_img_path) as invoice_img, Image.open(bottom_sheet_path) as bottom_sheet_img:
            # 将电子发票图片覆盖至粘贴底单上
            bottom_sheet_img.paste(invoice_img, (52, 99))
            # 填写内容及用途
            Expenses.___addTxtToImg('车辆运行费', bottom_sheet_img, font_path, 26, 971, 78)
            # 填写普通发票张数
            Expenses.___addTxtToImg('1', bottom_sheet_img, font_path, 35, 1045, 242)
            # 填写普通发票金额
            Expenses.___addTxtToImg(amount, bottom_sheet_img, font_path, 27, 1035, 275)
            # 填写经办人
            Expenses.___addTxtToImg(name, bottom_sheet_img, font_path, 38, 983, 553)
            # 保存
            expense_pdf_path = F'{path_n_basename}_expense.pdf'
            bottom_sheet_img.save(expense_pdf_path, 'PDF', resolution=100)
        
        os.remove(invoice_img_path)
    
