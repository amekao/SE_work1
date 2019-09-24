简单的文本统计软件    
--------------
诚挚欢迎您使用本软件！
程序需要通过cmd控制台以输入如下命令的方式来运行
“wc.exe [parameter] [file_name]”
------------
**[parameter]** 是控制参数，有如下几种控制参数：  
  _普通参数：_ -c -w -l -b -a 五种可随意组合叠加使用，顺序不限
   1. -c  返回文件字符数
   2. -w  返回文件词数
   3. -l  返回文件行数
   4. -b  返回文件详细字符数（数字/字母/空格/换行符/制表符/标点）
   5. -a  返回文件详细行数（代码行/空行/注释行） 
        注释行仅支持.c和.cpp格式，且不支持/**/类注释

  _特殊参数：_-s -x
   1. -s  寻找指定路径下所有符合通配符的文件并计算
   2. -x  弹出文件选择窗口，-c -w -l -b -a五种统计信息全显示
    
**[file_name]** 是文件信息，包括文件路径和文件名
   路径支持相对路径和绝对路径
   值得一提的是：
   1. 使用-s参数时可以对指定的目录递归遍历，
   文件后缀支持用*,?通配符输入
   2. 使用-x参数时文件由弹出对话框选择，因此不用输入此项,
   且默认五种计算模式都打开

**用法示例：**
   1. wc.exe -w -b -a file.py  
      返回文件file.py的词数，详细字符数，详细行数（代码行和空行）   
   2. wc.exe -x -abcdefg  
      -x优先级比较高，有-x在其他参数均会无视。弹出窗口进行选择
   3. wc.exe -s -a E:/code/  
      遍历E盘code文件夹下文件，不输入文件后缀默认为.c文件，输出详细行数
   4. wc.exe -s -b -w ../*.cpp  
      遍历当前文件上级目录中后缀为.cpp的文件，返回其详细字数和单词数
---
程序制作者：吴子昊 3117004671  
软件代码：https://github.com/amekao/SE_work1  
有任何bug和建议可以联系：peterwu7@qq.com