import os
import sys
import fitz
import invoice
import expenses
    

invoices_pdf_dir_path = sys.argv[1]
name: str = sys.argv[2]
if not os.path.exists(invoices_pdf_dir_path) or not name:
    print('usage:\n\tpython3 invoice_helper.py /path/to/invoices your_name')
    sys.exit(os.EX_USAGE)

# 校验发票报销条件
print('step0. check invoices availability:', flush=True)
valid_invoice_cnt = 0  # 有效 PDF 数量
valid_amount_total_int = 0  # 有效 PDF 金额
valid_invoices = list()
for invoice_pdf_name in (fn for fn in os.listdir(invoices_pdf_dir_path) if fn.lower().endswith('.pdf')):
    invoice_pdf_path = os.path.join(invoices_pdf_dir_path, invoice_pdf_name)
    print('\t', invoice_pdf_name, 'processing...', end=' ', flush=True)
    invoice_ = invoice.Invoice(invoice_pdf_path)
    if not invoice_.isValid():
        print('invalid :-(')
        continue
    valid_invoices.append(invoice_)
    print('valid :>')
    amount_int = int(float((invoice_.getAmount())))
    valid_amount_total_int += amount_int
    valid_invoice_cnt += 1
print(F'\tvalid invoices {valid_invoice_cnt}, valid amount total ￥{valid_amount_total_int}. ', flush=True)

# 生成报销单
print()
print('step1. create expenses:', flush=True)
font_path = 'res/liguofu.ttf'
bottom_sheet_path = 'res/bottom_sheet.jpg'
for valid_invoice in valid_invoices:
    invoice_pdf_name = os.path.basename(valid_invoice.getPath())
    print('\t', invoice_pdf_name, 'processing...', end=' ', flush=True)
    expenses.Expenses(valid_invoice.getPath(), bottom_sheet_path, font_path, str(int(float((valid_invoice.getAmount())))), name)
    print('done')

# 将多报销单 PDF 并合并为单个文件，以便一次性打印
print()
print('step2. create finally printable expense PDF file:', end=' ', flush=True)
all_in_one = fitz.open()
for expense_pdf_name in (fn for fn in os.listdir(invoices_pdf_dir_path) if fn.lower().endswith('_expense.pdf')):
    expense_pdf_path = os.path.join(invoices_pdf_dir_path, expense_pdf_name)
    expense_pdf = fitz.open(expense_pdf_path)
    all_in_one.insertPDF(expense_pdf)
    expense_pdf.close()
    os.remove(expense_pdf_path)
all_in_one_name = '----print_me----.pdf'
all_in_one.save(all_in_one_name, pretty=True)
all_in_one.close()
print('done.')

# 显示处理结果
print()
print(F'step3. now U can print finally expense {all_in_one_name}! ', flush=True)
print()
