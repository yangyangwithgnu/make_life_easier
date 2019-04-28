<h1 align="center">油票助手</h1>


的确，我一直缺个秘书！

### 事情缘起

每个季度单位允许我们定额报销一次交通费，只要把加油发票按要求粘贴到报销底单就行。我大概要作几步操作：检查电子发票有效性、调整 PDF 版电子发票尺寸、已调好尺寸的电子发票转为 PNG 版、打印 PNG 版电子发票、打印报销底单、将 PNG 电子发票粘贴至报销底单的合适区域、填写底单信息，这样七步也仅仅完成一张发票的处理，我有 15 张发票，生活艰辛！

我举几个例子，你随便感受下。

比如，检查电子发票有效性。在这个环保时代，油发票肯定是电子档 PDF 的，大概长这样子：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/电子发票.png" alt=""/><br>
</div>
有四条件必须满足要求才能报销：一是，开票日期必须是当年的工作日，不能是周末、不能是节假日；二是，购买方名称必须是本单位，"中国xx集团四川有限公司"；三是，销售方必须为成都市的加油站；四是，发票金额不能超过 ￥1000。二三四点倒容易，眼睛扫下就能判断，第一点的工作日判断就麻烦了，开票时间既不是周末、也不是假期，系统上的日期工具可以查看是否为周末但看不到节假日信息，所以我只能问百度，手工查看 20190124 是否为工作日：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/百度节假日查询.png" alt=""/><br>
</div>
你建议我只在工作日加油（我工作日都很加油：），那样开票时间就不会有问题了。是的，你很贤慧，但平时我很少开车，发票基本靠三朋四友捐赠的（鸣谢两位票友：文武兼备的勇哥、美丽与智慧并存的静静），既然是帮忙，又怎么好过多要求别人呢。

又如，调整电子发票尺寸。底单大概如下模样：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/票据粘贴底单.png" alt=""/><br>
</div>
油发票应该粘贴至高亮区域。底单为 A4 大小，电子发票默认打印出来也是 A4 尺寸，直接粘贴肯定会覆盖掉底单上部和右部的信息，所以，我先得把 PDF 版电子发票按 60% 显示，再按此比例截图成 PNG 版电子发票，然后打印粘贴。

再如，填报底单信息。内容及用途要填写"车辆运行费"，普通发票张数填写"1"，普通发票金额按实填报，经办人写本人"南门张学友"，15 张底单啊，把我累得不行了。

### 命令辅助

我琢磨这些繁琐操作或许能让计算机代劳。试试看。

第一步，提取电子发票中的文字信息。所幸原始电子发票是文本版 PDF，而非扫描版，让我可以选择一款钟意的工具，轻松提取文字版 PDF 中的文字信息，poppler-utils（https://poppler.freedesktop.org/ ）就很不错，基于老牌开源库 xpdf 开发的一款 PDF 处理套件，ubuntu 安装：
sudo apt install poppler-utils poppler-data -y
之后系统上就有了多个独立工具，比如，将 PDF 转换为文本的工具 pdftotext、转换为图片的 pdftoppm，将多个 PDF 合并成单个的 pdfunite、反之单个拆分成多个的 pdfseparate，提取 PDF 元数据的 pdfinfo、提取内嵌文件的 pdfdetach，总之，装上就赚到。

执行如下命令：
pdftotext （未知加油站）160.pdf
将电子发票中的文本信息提取到同目录下的 （未知加油站）160.txt 中：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/提取电子发票中的文本信息.png" alt=""/><br>
</div>

第二步，校验发票是否满足报销要求。虽然从 PDF 提取出的文本信息不那么工整，但报销要求相关的几个要素能以结构化的形式出现。开票日期，提取 "开票日期: 2019 年02 月27 日"，查询百度，确认是否为工作日；购买方名称，全文搜索确认是否存在关键字 "中国xx集团四川有限公司"；发票金额，提取关键字 "(小写)" 随后的数字，确认是否不大于 1000。如果三个条件均为真，那么该张发票可报销。

第三步，PDF 版发票转换为 PNG 版。为了便于后续操作，先生成图片版电子发票，前面提过的 pdftoppm 派上用场了：
pdftoppm -png -scale-to 900 （未知加油站）160.pdf > （未知加油站）160.png
其中，-scale-to 选项设定 PDF 文档的水平边和垂直边较长者的像素，如，电子发票通常是横向排版，
水平边较长，那么，-scale-to 900 就设定转换的图片水平为 900 像素、垂直边长自适应。

第四步，将电子发票图片覆盖至粘贴底单上。ImageMagick，我的老朋友了，两三年前它用魔图漏洞给我带来了无数个肉鸡：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/ImageMagick 漏洞列表.png" alt=""/><br>
</div>
扯远了，ImageMagick 是 web 系统广泛使用的图片处理套件，包含叠加图片的 composite、加工图片的 convert，以及其他命令。<br />

要达到粘贴的效果，也就要进行图片叠加操作，composite 很适合：
composite -geometry +60+120 （未知加油站）160.png bottom_sheet.bmp expenses0.png
其中，-geometry 设定发票图片相较左上角的偏移位置。效果如下：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/已贴票的报销单.png" alt=""/><br>
</div>

第五步，模拟手工笔迹填写底单信息。填写信息，实际上就是在图片指定位置上添加文字，字体是手写体就行。

网上找了一圈，李国夫手写体和我的笔迹挺像的：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/李国夫手写体.png" alt=""/><br>
</div>
下载安装好这款字体之后，找到它的安装路径：
yangyang@gnu:~$ fc-list | grep -i liguofu
/home/yangyang/.local/share/fonts/liguofu.ttf: liguofu:style=Regular

要想在"内容及用途"模拟手工签写"车辆运行费"，只需用 convert 在图片上适当位置用手写体输出文本即可。填写内容及用途：
convert -font '/home/yangyang/.local/share/fonts/liguofu.ttf' -pointsize 26 -annotate +968+96 '车辆运行费' expenses0.png expenses1.png
其中，-annotate 指定输出文本的坐标位置。效果如下：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/已写内容及用途的报销单.png" alt=""/><br>
</div>

填写普通发票张数1：
convert -font '/home/yangyang/.local/share/fonts/liguofu.ttf' -pointsize 35 -annotate +983+228 '1' expenses1.png expenses2.png
填写普通发票金额 160：
convert -font '/home/yangyang/.local/share/fonts/liguofu.ttf' -pointsize 27 -annotate +978+256 '160' expenses2.png expenses3.png
填写经办人南门张学友：
convert -font '/home/yangyang/.local/share/fonts/liguofu.ttf' -pointsize 39 -annotate +990+580 '南门张学友' expenses3.png expense.png
整体效果：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/报销单.png" alt=""/><br>
</div>

这样就完成了一张发票的处理，生成报销单图片。重复一至五步，处理完所有发票，生成多张报销单图片。

第六步，将多张报销单图片转换为 PDF 并合并为单个文件，以便一次性打印：
convert /path/to/expenses_img/*.png -quality 100 final.pdf
其中，-quality 指定转换质量为 100% 保真。 

### 脚本自动化

虽然前面有命令辅助处理发票，但仍需我的指导和看管，这不是我的预期，计算机就应该替我做完绝大部分事，我，最多打开、打印一个 PDF。嗯，得用代码把各个独立的命令串联起来，最好的命令粘合剂的语言理当 python，对标前面命令辅助实现的各步骤，看看 python 如何帮我实现自动化。

说个题外话，刚开始，从编译项目分发、性能提升考虑，我趋向用纯 python 来操纵 PDF 而非第三方命令，当前在维的、功能完善的 PDF 开源库有两个 PyPDF2（https://github.com/mstamy2/PyPDF2/ ）、pdfrw（https://github.com/pmaupin/pdfrw ），经过实际考察，若是英文 PDF，处理效果不错，但中文就无解了，所以，退而其次，任采用调用三方命令，python 作粘合剂。其中几个关键点，简单聊下。

提取开票日期中的数字部分。信息 "开票日期: 2019 年02 月27 日" 中的年月日，我以非数字作为分隔符，即可提取数字部分：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/提取日期数字.png" alt=""/><br>
</div>
其中，正则的 [^0-9] 等同于 '\D'。

判断日期是否为工作日。前面是通过百度查询，我倒是可以用 requests 自动查询，但程序又得依赖互联网，最好有个离线版的。库 workalendar（https://github.com/peopledoc/workalendar ）挺强大的，可处理大部份国家、2099 年前的节假日，但它只识别假日的第一天、无法识别结束日期：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/workalendar 无法识别节假日结束日期.png" alt=""/><br>
</div>
你看，五一劳动节节，5.1 正确识别出不是工作日，但 5.2 就错了；另一个库 chinese-calendar（https://github.com/LKI/chinese-calendar ），可以很好地支撑我的需求，唯一问题是它每年需要手工更新：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/chinese_calendar 正确识别工作日.png" alt=""/><br>
</div>
19 年的五一假期调整至四号，chinese-calendar 识别效果理想。综合考虑，选用 chinese-calendar。

python 启用外部命令的方式很多，个人偏好 subprocess.check_call()，它能关注到命令输出结果以及退出状态：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/用 subprocess.check_call() 启动外部命令.png" alt=""/><br>
</div>

全自动化生成最终报销单文件：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/操作.gif" alt=""/><br>
</div>
报销单文件效果：
<div align="center">
<img src="https://github.com/yangyangwithgnu/make_life_easier/blob/master/invoice_helper/img/最终报销单.gif" alt=""/><br>
</div>

后续有两个小问题找时间优化：
1）细化销售方是否为成都市内加油站的判断规则；
2）增加校验是否为正规发票。

生活理应美好，make life easier :-)

