import os
import glob
import invoice
import expenses
import subprocess
    

# 校验发票报销条件
print('step0. check invoices availability:', flush=True)
invoices_pdf_path = '/data/computer/practice/make_life_easier/invoice_helper/test_invoice/*.pdf'
valid_invoice_cnt = 0  # 有效 PDF 数量
valid_amount_total_int = 0  # 有效 PDF 金额
valid_invoices = list()
for invoice_pdf_path in (glob.glob(invoices_pdf_path)):
    invoice_pdf_name = os.path.basename(invoice_pdf_path)
    print('\t', invoice_pdf_name, 'processing...', end=' ', flush=True)
    invoice_ = invoice.Invoice(invoice_pdf_path)
    if not invoice_.isValid():
        print('not valid!')
        continue
    valid_invoices.append(invoice_)
    print('valid')
    amount_int = int(float((invoice_.getAmount())))
    valid_amount_total_int += amount_int
    valid_invoice_cnt += 1
print(F'\tvalid invoices {valid_invoice_cnt}, valid amount total ￥{valid_amount_total_int}. ', flush=True)

# 生成报销单
print()
print('step1. create expenses:', flush=True)
bottom_sheet_path = '/data/computer/practice/make_life_easier/invoice_helper/bottom_sheet.bmp'
font_path = '/home/yangyang/.local/share/fonts/liguofu.ttf'
for valid_invoice in valid_invoices:
    invoice_pdf_name = os.path.basename(valid_invoice.getPath())
    print('\t', invoice_pdf_name, 'processing...', end=' ', flush=True)
    expenses.Expenses(valid_invoice.getPath(), bottom_sheet_path, font_path, str(int(float((valid_invoice.getAmount())))))
    print('done')

# 将多张图片转换为 PDF 并合并为单个文件，以便一次性打印
print()
print('step2. create finally printable expense PDF file:', end=' ', flush=True)
invoices_dir_path = os.path.dirname(invoices_pdf_path)
final_pdf_path = os.path.join(invoices_dir_path, 'final.pdf')
subprocess.check_call(F'convert {os.path.join(invoices_dir_path, "*.png")} -quality 100 {final_pdf_path}', shell=True)
print('done.')

# 删除报销单图片
print()
print('step3. delete tmp images:', end=' ', flush=True)
for expense_img_path in (glob.glob(os.path.join(invoices_dir_path, "*.png"))):
    os.remove(expense_img_path)
print('done.')

# 显示处理结果
print()
print(F'step4. now U can print finally expense {final_pdf_path}. ', flush=True)
print()
