# PyQt_InteractiveTerminal

```diff
! 运行脚本【Main.py】
```

<br>该项目的本意是为了给理想的“帮助手册”打下基础。目前来说这个项目用起来也没什么问题于是就先上传了
<br>运行效果就是强化过的伪终端（见下面运行截图）
<br>基于PyQt，核心的变量/函数/引用为：exec、eval、compile、sys.stdout

<br>
<br>文件说明：
<br>【XJ_InteractiveTool.py】为伪终端(命令行形式)，用起来和系统自带终端基本没区别(不排除是我测试做得少，没试出问题)。
<br>【XJ_InteractiveTerminal.py】为伪终端(PyQt界面)，除了界面不一样外和命令行形式的伪终端没区别。
<br>【XJ_Main.py】在这里定义额外的功能(函数+自定义指令)并对XJ_InteractiveTerminal进行一些设置(见下面的图6图7)，所以才说是“强化过的伪终端”(因为能完成更多功能)
<br>【XJ_TextEdit.py】个人认为算是封装得不错的QT组件，既可单行又能多行，附加了“回车发送信息”的行为(不需要的话可以关闭)以及“文本搜索”功能，算是一只小麻雀了(功能不多但实用)
<br>【XJ_ListAccessor.py】受限型列表访问器，用于实现历史输入的，个人认为这个类算是设计得比较规范的一个(因为没有简单地把list塞进类里头而是采用“访问器”的形式)
<br>【XJ_Recorder.py】这个的话，额，算是最妖魔最邪道的一个文件/模块了(本人盛产奇怪代码)，看看这个文件的内容就知道我为啥这么形容它(因为它，这，反正就是不合常理但就是能跑)



<br>
<br>
<br>




# 【运行效果】
![1](https://github.com/Ls-Jan/PyQt_InteractiveTerminal/blob/main/RunningResult%5BPNG%5D/1.png)
![2](https://github.com/Ls-Jan/PyQt_InteractiveTerminal/blob/main/RunningResult%5BPNG%5D/2.png)
![3](https://github.com/Ls-Jan/PyQt_InteractiveTerminal/blob/main/RunningResult%5BPNG%5D/3.png)
![4](https://github.com/Ls-Jan/PyQt_InteractiveTerminal/blob/main/RunningResult%5BPNG%5D/4.png)
![5](https://github.com/Ls-Jan/PyQt_InteractiveTerminal/blob/main/RunningResult%5BPNG%5D/5.png)
![6](https://github.com/Ls-Jan/PyQt_InteractiveTerminal/blob/main/RunningResult%5BPNG%5D/6.png)
![7](https://github.com/Ls-Jan/PyQt_InteractiveTerminal/blob/main/RunningResult%5BPNG%5D/7.png)

