<h2 align="center">油票女秘书</h2>

的确，我一直缺个女秘书！

### 事情缘起

每个季度单位允许我们报销一次交通费，只要把燃油发票按要求粘贴到报销底单就行。我大概要作几步操作：检查电子发票有效性、调整 PDF 版电子发票尺寸、将尺寸合适的电子发票截图为图片、打印发票图片、打印报销底单、将发票图片粘贴至报销底单的合适区域、填写底单信息，这样七步完成一张发票的处理，我有十六张发票啊，可不能把我累着了！

这些体力活儿挺麻烦的，我举几个例子，你随便感受下。

比如，检查电子发票有效性。在这个环保时代，油发票肯定是电子档 PDF 的，大概长这样子：
<p align="center">
  <img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/电子发票.png">
</p>
报销时必须满足四个条件：一是，开票日期得是当年的工作日，不能是周末、不能是节假日；二是，购买方名称必须是本单位，"中国xx集团四川有限公司"；三是，销售方必须为成都市的加油站；四是，发票金额不能超过 ￥1000。二三四点倒容易，眼睛扫下就能判断，第一点的工作日判断就麻烦了，开票时间既不是周末、也不是节假日，操作系统上的日期工具倒是可以查看周末但看不到节假日，所以我只能问百度，手工查看 20190124 是否为工作日：
![](https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/%E7%99%BE%E5%BA%A6%E8%8A%82%E5%81%87%E6%97%A5%E6%9F%A5%E8%AF%A2.png)

你建议我只在工作日加油（工作日我很加油 :-），那样开票时间就不会有问题。是的，你很贤慧，但平时我很少开车，发票基本靠三朋四友捐赠（鸣谢两位票友：文武兼备的勇哥、美丽与智慧并存的静静），既然是帮忙，又怎么好过多要求别人呢。

又如，调整电子发票尺寸。底单大概如下模样：
![](https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/%E7%A5%A8%E6%8D%AE%E7%B2%98%E8%B4%B4%E5%BA%95%E5%8D%95.png)
油发票应该粘贴至高亮区域。底单为 A4 大小，电子发票默认打印出来也是 A4 尺寸，直接粘贴肯定会覆盖掉底单上部和右部的信息，所以，我先得把 PDF 版电子发票按 60% 显示，再按此比例截图成 PNG 版电子发票，然后打印粘贴。

再如，填报底单信息。内容及用途要填写 车辆运行费，普通发票张数填写 1，普通发票金额按实填报，经办人写本人 南门张学友，16 张底单啊，把我累得不行了。

### 命令行实现半自动

我琢磨这些繁琐操作或许能让计算机代劳。试试看。

第一步，提取电子发票中的文字信息。所幸原始电子发票是文本版 PDF，而非扫描版，让我可以选择一款钟意的工具，轻松提取文字版 PDF 中的文字信息，poppler-utils（https://poppler.freedesktop.org/ ）就很不错，基于老牌开源库 xpdf 开发的一款 PDF 处理套件，ubuntu 安装：
```shell
sudo apt install poppler-utils poppler-data -y
```
之后系统上就有了多个独立工具，比如，将 PDF 转换为文本的工具 pdftotext、转换为图片的 pdftoppm，将多个 PDF 合并成单个的 pdfunite、反之单个拆分成多个的 pdfseparate，提取 PDF 元数据的 pdfinfo、提取内嵌文件的 pdfdetach，总之，装上就赚到。

执行如下命令：
```shell
pdftotext （未知加油站）160.pdf
```
将电子发票中的文本信息提取到同目录下的 （未知加油站）160.txt 中：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/提取电子发票中的文本信息.png" alt=""/><br>
</div>
第二步，校验发票是否满足报销要求。虽然从 PDF 提取出的文本信息不那么工整，但报销要求相关的几个要素都还是能以结构化的形式呈现。开票日期，提取 开票日期: 2019 年02 月27 日，查询百度，确认是否为工作日；购买方名称，全文搜索确认是否存在关键字 中国xx集团四川有限公司；发票金额，提取关键字 (小写) 随后的数字，确认是否不大于 1000。如果三个条件均为真，那么该张发票可报销。

第三步，PDF 版发票转换为 PNG 版。为了便于后续操作，先生成图片版电子发票，前面提过的 pdftoppm 派上用场了：
```shell
pdftoppm -png -scale-to 900 （未知加油站）160.pdf > （未知加油站）160.png
```
其中，-scale-to 选项设定 PDF 文档的水平边和垂直边较长者的像素，如，电子发票通常是横向排版，水平边较长，那么，-scale-to 900 就设定转换的图片水平为 900 像素、垂直边长自适应。

第四步，将电子发票图片覆盖至粘贴底单上。ImageMagick，我的老朋友了，两三年前它用魔图漏洞给我带来了无数个肉鸡：
![](https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/ImageMagick%20%E6%BC%8F%E6%B4%9E%E5%88%97%E8%A1%A8.png)
扯远了，ImageMagick 是 web 系统广泛使用的图片处理套件，包含叠加图片的 composite、加工图片的 convert，以及其他命令。

要达到粘贴的效果，也就要进行图片叠加操作，composite 很适合：
```shell
composite -geometry +60+120 （未知加油站）160.png bottom_sheet.bmp expenses0.png
```
其中，-geometry 设定发票图片从左上角的偏移位置。效果如下：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/已贴票的报销单.png" alt=""/><br>
</div>

第五步，模拟手工笔迹填写底单信息。填写信息，实际上就是在图片指定位置上添加文字，用手写体模拟即可。

网上找了一圈，李国夫手写体和我的笔迹挺像的：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/李国夫手写体.png" alt=""/><br>
</div>
下载安装好这款字体之后，找到它的安装路径：
```shell
yangyang@gnu:~$ fc-list | grep -i liguofu
/home/yangyang/.local/share/fonts/liguofu.ttf: liguofu:style=Regular
```

要想在 内容及用途 模拟手工签写 车辆运行费，只需用 convert 在图片上适当位置用手写体字体输出文本即可。填写内容及用途：
```shell
convert -font '/home/yangyang/.local/share/fonts/liguofu.ttf' -pointsize 26 -annotate +968+96 '车辆运行费' expenses0.png expenses1.png
```
其中，-annotate 指定输出文本的坐标位置。效果如下：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/已写内容及用途的报销单.png" alt=""/><br>
</div>

填写普通发票张数1：
```shell
convert -font '/home/yangyang/.local/share/fonts/liguofu.ttf' -pointsize 35 -annotate +983+228 '1' expenses1.png expenses2.png
```
填写普通发票金额 160：
```
convert -font '/home/yangyang/.local/share/fonts/liguofu.ttf' -pointsize 27 -annotate +978+256 '160' expenses2.png expenses3.png
```
填写经办人“南门张学友”：
```
convert -font '/home/yangyang/.local/share/fonts/liguofu.ttf' -pointsize 39 -annotate +990+580 '南门张学友' expenses3.png expense.png
```
完成信息填写：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/报销单.png" alt=""/><br>
</div>
这样就完成了一张发票的处理，生成报销单图片。重复一至五步，处理完所有发票，生成多张报销单图片。

第六步，将多张报销单图片转换、合并为单个 PDF 文件，以便一次性打印：
```
convert /path/to/expenses_img/*.png -quality 100 final.pdf
```
其中，-quality 指定转换质量为 100% 保真。

### 脚本实现全自动

虽然前面有命令辅助处理发票，但仍需我的指导和看管，这不是我的预期，计算机就应该替我做完绝大部分事，作为食物链顶端的我，最多是打印个 PDF，不能再多了。

你知道，我移居 linux 多年，只要用 bash 脚本把前面各个独立命令串联起来，释放双手的目的就达到了，但考虑到 win 用户，具体开发功能时，有 win 版的命令则直接调用命令，没有的则用 python 实现。在前面命令行推演实现半自动的基础上，python 实现全自动并不困难，其中几个关键点，简单聊下。

关键点一，python 启用外部命令。python 执行系统命令的方式很多，个人偏好 subprocess.check_output()，它能关注到命令输出结果以及退出状态：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/执行系统命令.png" alt=""/><br>
</div>
另外，路径或文件名相关的命令行参数，一定要带上引号，防止因文件名中含有空白字符导致命令执行失败：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/命令执行时应将路径放入引号中.png" alt=""/><br>
</div>
提醒下，脚本语言直接启用外部命令的场景中，很可能导致命令注入漏洞，即便用引号包裹了命令参数（引号闭合、引号转义），所以，该脚本切勿用于线上服务，只能用于本地程序！

关键点二，提取 PDF 中的文字信息。当前在维的、功能完善的 PDF 开源库有三个：PyPDF2（https://github.com/mstamy2/PyPDF2/ ）、pdfrw（https://github.com/pmaupin/pdfrw ）、PyMuPDF（https://github.com/pymupdf/PyMuPDF ），从口碑来看，PyPDF2 最赞，但就中文支持度而言，PyMuPDF 最优。

我尝试用 PyMuPDF 提取电子油票中的文本：
```
import fitz

doc = fitz.open("（中石油）200.pdf")
page = doc.loadPage(0)
print(page.getText("text"))
doc.close()
```
效果不理想，比如，本应连续出现的“开票日期：2019 年 03 月 03 日”却分隔为“开票日期”、“2019  03  03”、“年月日”，且散落在不同地方，这类非结构化文本，程序很难处理。所以，提取 PDF 文本的功能，我不得不用前面的 xpdf 套件中的 pdftotext 命令来实现。

pdftotext 在 linux 下运行效果还不错，win 下不知道怎么样，试试看。到 https://www.xpdfreader.com/download.html 下载 win 版：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/win 版 pdftotext.png" alt=""/><br>
</div>
运行看看：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/pdftotext 无法写入中文文件名.png" alt=""/><br>
</div>
报错“无法打开文件”，怀疑 pdftotext 无法写入中文文件名，变通下，用 - 替换文件名，不输出至文件而是直接显示：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/缺少语言支持包.png" alt=""/><br>
</div>
新问题又来了，从描述来看，好像缺少中文语言支持，找帮助文档看看：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/xpdf 文档.png" alt=""/><br>
</div>
xpdfrc.txt 是配置说明、sample-xpdfrc 是配置样例，按指导，在桌面新建文件夹 xpdf-utils/，xpdf-utils/ 中新建文本 xpdfrc，内容如下：
```
#----- display fonts

# These map the Base-14 fonts to the Type 1 fonts that ship with
# ghostscript.  You'll almost certainly want to use something like
# this, but you'll need to adjust this to point to wherever
# ghostscript is installed on your system.  (But if the fonts are
# installed in a "standard" location, xpdf will find them
# automatically.)

fontFile Symbol			.\\ps-fonts\s050000l.pfb
fontFile ZapfDingbats		.\\ps-fonts\d050000l.pfb

# If you need to display PDF files that refer to non-embedded fonts,
# you should add one or more fontDir options to point to the
# directories containing the font files.  Xpdf will only look at .pfa,
# .pfb, .ttf, and .ttc files in those directories (other files will
# simply be ignored).

fontDir		.\\non-embedded-font

#----- text output control

# Choose a text encoding for copy-and-paste and for pdftotext output.
# The Latin1, ASCII7, and UTF-8 encodings are built into Xpdf.  Other
# encodings are available in the language support packages.

textEncoding		GBK

#----- misc settings

# Enable FreeType, and anti-aliased text.

enableFreeType		yes
antialias		yes
vectorAntialias		yes

#----- Chinese Simplified support package (2011-sep-02)

cidToUnicode	Adobe-GB1	.\\chinese-simplified\Adobe-GB1.cidToUnicode
unicodeMap	ISO-2022-CN	.\\chinese-simplified\ISO-2022-CN.unicodeMap
unicodeMap	EUC-CN		.\\chinese-simplified\EUC-CN.unicodeMap
unicodeMap	GBK		.\\chinese-simplified\GBK.unicodeMap
cMapDir		Adobe-GB1	.\\chinese-simplified\CMap
toUnicodeDir			.\\chinese-simplified\CMap
```

配置项 fontFile 用于指定 PS 字体路径。PS 字体是按 PostScript 页面描述语言（PDL）规则定义的字体，属于矢量字体，常用的 Symbol 和 ZapfDingbats 两种 PS 字体可在页面下载：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/PS 向量字体.png" alt=""/><br>
</div>
在 xpdf-utils/ 中新建文件夹 ps-fonts/，将下载回来的 Symbol 和 ZapfDingbats 两种 PS 字体放入其中。

配置项 fontDir 用于指定非内嵌字体（non-embedded）。除了矢量字体，PDF 还会用到像素字体（比如系统自带的宋体），由于像素字体体积较大，PDF 文档并未将其嵌入文档内，需要单独提供。在 xpdf-utils/ 中新建文件夹 non-embedded-font/，将 C:\Windows\Fonts 中任一简中字体（如 Microsoft YaHei Light.ttc）拷贝至 non-embedded-font/，运行 xpdf 套件中的任何工具时，只要出现类似如下报错：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/缺少外部字体.png" alt=""/><br>
</div>
在 non-embedded-font/ 中，将 Microsoft YaHei Light.ttc 字体拷贝两份，分别重命名为 AdobeKaitiStd-Regular.ttc 和 STSong-Light-UniGB-UCS2-H.ttc，类似，若有报错无法找到 foo 字体，拷贝Microsoft YaHei Light.ttc 并重命名 foo.ttc 即可。

Chinese Simplified support package 中的配置项，用于设置简体中文支持包的路径。中文支持包下载：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/中文支持包.png" alt=""/><br>
</div>
解压后，将文件夹 xpdf-chinese-simplified/ 重命名为 chinese-simplified/，再移至 xpdf-utils/ 中，将 pdftotext.exe 和 pdftopng.exe 也复制至 xpdf-utils/ 中。

xpdf-utils/ 完整目录结构如下：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/xpdf-utils 目录结构.png" alt=""/><br>
</div>
运行试试，一切正常：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/pdftotext 运行正常.png" alt=""/><br>
</div>

用 python 简单封装如下：
```python
def convertPdf2Txt(pdf_path: str) -> str:
    # 执行外部命令 pdftotxt，提取 PDF 中的文本
    if platform.system() == 'Linux':
        return(subprocess.check_output(F'pdftotext {pdf_path} -', shell=True).decode('utf-8'))
    elif platform.system() == 'Windows':
        return(subprocess.check_output(F'pdftotext.exe -q "{pdf_path}" -', shell=True, cwd='pdf2txt').decode('gbk'))
    else:
        raise(Exception('ERROR! unkown OS.')
```

关键点三，提取开票日期中的数字部分。信息 "开票日期: 2019 年02 月27 日" 中的年月日，我以非数字作为分隔符，即可提取数字部分：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/XX.png" alt=""/><br>
</div>
其中，正则的 [^0-9] 等同于 '\D'。

关键点四，判断日期是否为工作日。前面是通过百度查询，我倒是可以用 requests 自动查询，但程序又得依赖互联网，最好有个离线版的。workalendar 库（https://github.com/peopledoc/workalendar ）挺强大的，可处理大部份国家、2099 年前的节假日，但它只识别假日的第一天、无法识别结束日期：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/XX.png" alt=""/><br>
</div>
你看，五一劳动节节，5.1 正确识别出不是工作日，但 5.2 就错了；另一个库 chinese-calendar（https://github.com/LKI/chinese-calendar ），可以很好地支撑我的需求，唯一问题是它每年需要手工更新：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/XX.png" alt=""/><br>
</div>
2019 年的五一假期调整至四号，chinese-calendar 识别效果理想。综合考虑，选用 chinese-calendar。

关键点五，PDF 转图片、图片叠加、图片添加文字、图片转 PDF、PDF 合并。

PyMuPDF 库可以轻松实现 PDF 转图片：
```python
import fitz

doc = fitz.open("（中石油）200.pdf")
matrix = fitz.Matrix(1.47, 1.47)  # 缩放比例
pixs = doc[0].getPixmap(matrix=matrix, alpha=False)  # 获取 PDF 第一页的所有像素
pixs.writePNG("（中石油）200.png")  # 将所有像素写入图片文件
doc.close()
```

借助 pillow 进行图片叠加，模拟将电子发票图片至粘贴底单上的效果：
```python
from PIL import Image

with Image.open('（中石油）200.png') as invoice_img, Image.open('bottom_sheet.jpg') as bottom_sheet_img:
    bottom_sheet_img.paste(invoice_img, (52, 99))
    bottom_sheet_img.save('expenses.png')
```

图片添加文字，再另存为 PDF：
```python
from PIL import Image, ImageFont, ImageDraw

font = ImageFont.truetype('/data/computer/practice/make_life_easier/invoice_helper/res/liguofu.ttf', 32)
with Image.open('/data/computer/practice/make_life_easier/invoice_helper/res/bottom_sheet.jpg') as img:
    ImageDraw.Draw(img).text((980, 555), '刘德华', font=font, fill=(0, 0, 0))
    img.save('mysmile.pdf', 'PDF', resolution=100)
```

PDF 合并：
```python
import fitz

all_in_one = fitz.open()
all_in_one.insertPDF(fitz.open("1.pdf"))
all_in_one.insertPDF(fitz.open("2.pdf"))
all_in_one.insertPDF(fitz.open("3.pdf"))
all_in_one.save('all_in_one.pdf', pretty=True)
all_in_one.close()
```

关键点六，win 下程序分发。图形界面和开箱即用是 win 用户的最大诉求。

发票助手是个简单应用，无需复杂的图像界面，所以我优选 python 自带 GUI 库 tkinter 来实现。十来行代码，效果如下：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/win 下图形界面效果.png" alt=""/><br>
</div>
注意，invoice_helper_gui.exe 所在路径不能出现中文。

另外，发票助手及其三方库，我得打包进单个的可执行程序，这样才能满足开箱即用。我通过pyinstaller（https://github.com/pyinstaller/pyinstaller ）将 *.py 打包为 *.exe：
```python
# 按单个 exe 分发
pyinstaller --noconsole --onefile invoice_helper_gui.py
# 按单个目录分发
pyinstaller --noconsole --onedir invoice_helper_gui.py
```
最终目录结构如下：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/win 应用分发目录结构.png" alt=""/><br>
</div>

### make life easier

以后，单位再让我贴油票，只需运行发票助手脚本 invoice_helper.py：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/操作 CLI 版.gif" alt=""/><br>
</div>
或者，运行 GUI 版的：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/操作 GUI 版.gif" alt=""/><br>
</div>

自动生成最终报销单文件，直接打印即可：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/最终报销单.gif" alt=""/><br>
</div>

这下，世界清净了。

