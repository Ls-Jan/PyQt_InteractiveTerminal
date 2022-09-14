
# 【更新】
解决了部分模块导入问题，例如导入import alphalens时会提示与ctypes有关的模块导入错误，那么需要执行```“-- ctypes”(新添的功能)```将ctypes从模块缓存sys.modules中删除，然后再次导入alphalens即可

遗留问题(摸了，有空一定修)：
<br>①、执行语句时的报错内容有时输出不理想
<br>②、没新增“强制导入”功能。“强制导入”也就是导入失败提示某个模块有问题的话(例如上面导入alphalens的例子)那么就将问题模块的缓存清除然后再次执行模块导入操作直至导入成功或者出现其他导入问题
<br>③、如果复制多行文本粘贴到输入框的话会有多余的回车没删干净
<br>④、输入框的字体样式会因为粘贴的文本而发生变动
<br>⑤、Releases我就不去更新了，需要的话就把项目下载下来然后手动打包吧(—,— )
<br>(遗留问题不止这么点，只是想到啥写啥而已)

```diff
! 运行脚本【Main.py】
```

# 【项目一般说明】
该项目的本意是为了给理想的“帮助手册”打下基础。目前来说这个项目用起来也没什么问题于是就先上传了。
<br>因为我这个项目是基于解释器函数“exec”、“eval”、“compile”的，所以，怎么说呢，个人认为比较稳不会翻车，所以在了解到“PDB”（Python调试器）后我并不怎么想改动项目。
<br>运行效果就是强化过的伪终端（见下面运行截图）
<br>基于PyQt，核心的变量/函数/引用有：exec、eval、compile、sys.stdout、sys.path



# 【预置指令】
给了这个伪终端设置了许多预置指令：
```diff
+ [cd] 指令改变当前目录
+ [ls] 指令查看目录下文件
+ [?] 指令快速调用help
+ [.] 指令将列表内容以表格形式显示出来(并且支持关键词筛选)
+ [..] 指令将变量的属性名以表格形式显示出来(并且支持关键词筛选)
+ [...] 指令用于清空输出窗口
```
更多的预置指令可以在【Main.py】中尽情地设置，
<br>当然，在这个文件中可以完成更多函数以实现更多功能（或者可以写在其他py脚本中然后执行from XXX import * 语句将脚本内的环境变量全导入到交互端中


# 【其他操作】
在输入框中按着Ctrl/Alt键的同时按↑/↓键即可返回历史输入
<br>



# 【文件说明】
【XJ_InteractiveTool.py】为伪终端(命令行形式)，用起来和系统自带终端基本没区别(不排除是我测试做得少，没试出问题)。
<br>【XJ_InteractiveTerminal.py】为伪终端(PyQt界面)，除了界面不一样外和命令行形式的伪终端没区别。
<br>【XJ_Main.py】在这里定义额外的功能(函数+自定义指令)并对XJ_InteractiveTerminal进行一些设置(见下面的图6图7)，所以才说是“强化过的伪终端”(因为能完成更多功能)
<br>【XJ_TextEdit.py】个人认为算是封装得不错的QT组件，既可单行又能多行，附加了“回车发送信息”的行为(不需要的话可以关闭)以及“文本搜索”功能，算是一只小麻雀了(功能不多但实用)
<br>【XJ_ListAccessor.py】受限型列表访问器，用于实现历史输入的，个人认为这个类算是设计得比较规范的一个(因为没有简单地把list塞进类里头而是采用“访问器”的形式)
<br>【XJ_Recorder.py】这个的话，额，算是最妖魔最邪道的一个文件/模块了(本人盛产奇怪代码)，看看这个文件的内容就知道我为啥这么形容它(因为它，这，反正就是不合常理但就是能跑)


<br>
<br>
<br>





# 【运行效果】
![2](https://github.com/Ls-Jan/PyQt_InteractiveTerminal/blob/main/RunningResult%5BPNG%5D/2.png)
![3](https://github.com/Ls-Jan/PyQt_InteractiveTerminal/blob/main/RunningResult%5BPNG%5D/3.png)
![4](https://github.com/Ls-Jan/PyQt_InteractiveTerminal/blob/main/RunningResult%5BPNG%5D/4.png)
![5](https://github.com/Ls-Jan/PyQt_InteractiveTerminal/blob/main/RunningResult%5BPNG%5D/5.png)
![6](https://github.com/Ls-Jan/PyQt_InteractiveTerminal/blob/main/RunningResult%5BPNG%5D/6.png)
![7](https://github.com/Ls-Jan/PyQt_InteractiveTerminal/blob/main/RunningResult%5BPNG%5D/7.png)
![8](https://github.com/Ls-Jan/PyQt_InteractiveTerminal/blob/main/RunningResult%5BPNG%5D/8.png)
![9](https://github.com/Ls-Jan/PyQt_InteractiveTerminal/blob/main/RunningResult%5BPNG%5D/9.png)
![10](https://github.com/Ls-Jan/PyQt_InteractiveTerminal/blob/main/RunningResult%5BPNG%5D/10.png)



