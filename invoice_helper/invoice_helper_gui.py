import os
import fitz
import tkinter
import invoice
import expenses
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter.filedialog import askdirectory
    

def makeExpense():

    invoices_pdf_dir_path = invoices_pdf_dir_path_sv.get()
    name = name_sv.get()

    if not os.path.exists(invoices_pdf_dir_path) or not name:
        messagebox.showwarning('错误', '未指定汽油电子发票目录，或，未填入报销人姓名。')
        return

    # 校验发票报销条件
    text_ctrler.insert(tkinter.END, 'step0. check invoices availability:\n')
    valid_invoice_cnt = 0  # 有效 PDF 数量
    valid_amount_total_int = 0  # 有效 PDF 金额
    valid_invoices = list()
    for invoice_pdf_name in (fn for fn in os.listdir(invoices_pdf_dir_path) if fn.lower().endswith('.pdf')):
        invoice_pdf_path = os.path.join(invoices_pdf_dir_path, invoice_pdf_name)
        text_ctrler.insert(tkinter.END, F'\t{invoice_pdf_name} processing...')
        invoice_ = invoice.Invoice(invoice_pdf_path)
        if not invoice_.isValid():
            text_ctrler.insert(tkinter.END, 'invalid :-(\n')
            continue
        valid_invoices.append(invoice_)
        text_ctrler.insert(tkinter.END, 'valid :-)\n')
        amount_int = int(float((invoice_.getAmount())))
        valid_amount_total_int += amount_int
        valid_invoice_cnt += 1
        text_ctrler.update()
    text_ctrler.insert(tkinter.END, F'\tvalid invoices {valid_invoice_cnt}, valid amount total ￥{valid_amount_total_int}. \n')
    text_ctrler.insert(tkinter.END, '=-' * 32)
    text_ctrler.insert(tkinter.END, '\n\n')
    text_ctrler.update()

    # 生成报销单
    text_ctrler.insert(tkinter.END, 'step1. create expenses:\n')
    font_path = 'res/liguofu.ttf'
    bottom_sheet_path = 'res/bottom_sheet.jpg'
    for valid_invoice in valid_invoices:
        invoice_pdf_name = os.path.basename(valid_invoice.getPath())
        text_ctrler.insert(tkinter.END, F'\t{invoice_pdf_name} processing... ')
        expenses.Expenses(valid_invoice.getPath(), bottom_sheet_path, font_path, str(int(float((valid_invoice.getAmount())))), name)
        text_ctrler.insert(tkinter.END, 'done\n')
        text_ctrler.update()
    text_ctrler.insert(tkinter.END, '=-' * 32)
    text_ctrler.insert(tkinter.END, '\n\n')
    text_ctrler.update()

    # 将多报销单 PDF 并合并为单个文件，以便一次性打印
    text_ctrler.insert(tkinter.END, 'step2. create finally printable expense PDF file: ')
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
    text_ctrler.insert(tkinter.END, 'done. \n')
    text_ctrler.insert(tkinter.END, '=-' * 32)
    text_ctrler.insert(tkinter.END, '\n\n')
    text_ctrler.update()

    # 显示处理结果
    text_ctrler.insert(tkinter.END, F'step3. now U can print finally expense {all_in_one_name}! \n')
    text_ctrler.insert(tkinter.END, '=-' * 32)
    text_ctrler.insert(tkinter.END, '\n\n')
    text_ctrler.update()

    # 显示导入模版 excel
    text_ctrler.insert(tkinter.END, F'step4. copy excel import template date: \n')
    for valid_invoice in valid_invoices:
        text_ctrler.insert(tkinter.END, valid_invoice.getInvoiceCode())
        text_ctrler.insert(tkinter.END, '\t')
        text_ctrler.insert(tkinter.END, valid_invoice.getInvoiceNo())
        text_ctrler.insert(tkinter.END, '\t')
        text_ctrler.insert(tkinter.END, '-'.join(valid_invoice.getDate()))
        text_ctrler.insert(tkinter.END, '\t')
        text_ctrler.insert(tkinter.END, valid_invoice.getCheckcode()[-6:])
        text_ctrler.insert(tkinter.END, '\n')
        text_ctrler.update()

    


win = tkinter.Tk()
win.title("汽油发票助手")
win.resizable(False, False)

invoices_pdf_dir_path_lf = ttk.LabelFrame(win, text='汽油电子发票')
invoices_pdf_dir_path_lf.grid(row=0, column=0, pady=4)
invoices_pdf_dir_path_label = ttk.Label(invoices_pdf_dir_path_lf, text='PDF 目录：')
invoices_pdf_dir_path_label.grid(column=0, row=0, sticky='W')
invoices_pdf_dir_path_sv = tkinter.StringVar()
tkinter.Entry(invoices_pdf_dir_path_lf, width=40, textvariable=invoices_pdf_dir_path_sv).grid(row=0, column=1, padx=6)
tkinter.Button(invoices_pdf_dir_path_lf, text='选择', command=lambda: invoices_pdf_dir_path_sv.set(askdirectory())).grid(row=0, column=2)

name_lf = ttk.LabelFrame(win, text='报销人')
name_lf.grid(row=1, column=0, pady=4)
name_label = ttk.Label(name_lf, text='姓名：')
name_label.grid(column=0, row=0, sticky='W')
name_sv = tkinter.StringVar()
tkinter.Entry(name_lf, width=52, textvariable=name_sv).grid(row=0, column=1)

tkinter.Button(win, text='生成报销单', command=makeExpense).grid(row=2, column=0, pady=8)

text_ctrler = scrolledtext.ScrolledText(win, width=72, height=32, wrap=tkinter.WORD)
text_ctrler.grid(row=3, column=0)

win.mainloop()

