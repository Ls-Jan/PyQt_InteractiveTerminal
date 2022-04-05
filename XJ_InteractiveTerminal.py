import XJ_Recorder
from XJ_TextEdit import *
from XJ_ListAccessor import *
from XJ_InteractiveTool import *
from PyQt5.QtGui import QTextCharFormat,QColor

class XJ_InteractiveTerminal(QWidget):#XJ的交互式窗口
    def __init__(self,varDict=dict(),parent=None):#记得传入变量字典，环境卫生从我做起
        super(XJ_InteractiveTerminal, self).__init__(parent)

        input=XJ_TextEdit()#命令输入端
        input.SendMsgMode(True)#开启“发送信息功能"
        input.OneLineMode(True)#设置为单行模式
        input.textSent.connect(self.SendText)#绑定事件

        output=XJ_TextEdit()#命令显示端
        output.SendMsgMode(False)#关闭“发送信息功能”
        output.setReadOnly(True)#设置为只读


        box=QVBoxLayout()
        box.addWidget(output)
        box.addWidget(input)
        box.setStretchFactor(output,1)
        self.setLayout(box)

        self.__input=input
        self.__output=output
        self.__IT=XJ_InteractiveTool(varDict)

        self.__fmtNormal=QTextCharFormat()
        self.__fmtNormal.setFont(output.font())
        self.__fmtNormal.setForeground(Qt.black)
        self.__fmtHint=QTextCharFormat()
        self.__fmtHint.setFont(output.font())
        self.__fmtHint.setForeground(Qt.blue)

        self.setStyleSheet("background-color: transparent;")
        output.verticalScrollBar().setStyleSheet("background-color:rgb(128,172,224);")
        input.setStyleSheet("color:rgb(255,255,255)")
        self.setWindowOpacity(0.80)#设置透明度
        self.__history=['']#输入的历史记录
        self.__inputAsr=XJ_ListAccessor(self.__history,1000)#容量为1000

        self.__AddText("")
        input.setFocus()#设置焦点

    def SendText(self,text):
        self.__inputAsr.ForceInsert(text)
        text=self.TextPreprocess(text)
        self.__inputAsr.IterNext()
        rst=self.__IT.ReadOrder(text)
        outputText=text+"\n"+''.join(rst)
        self.__AddText(outputText)

    def TextPreprocess(self,text):#对文本进行预处理的函数
        return text

    def __AddText(self,text):#在文本框self.__output中添加内容
        output=self.__output
        cursor=output.textCursor()
        fmt=QTextCharFormat()

        fmt.setFont(output.font())
        cursor.movePosition(QTextCursor.End)#移至文末

        fmt.setForeground(QColor(255,255,0))
        cursor.setCharFormat(fmt)#设置一般文本格式
        cursor.insertText(text)#添加文本
        fmt.setForeground(QColor(128,192,255))
        cursor.setCharFormat(fmt)#设置提示符格式
        cursor.insertText("..."if self.__IT.HoldOn() else ">>>")#插入输入提示符
        output.setTextCursor(cursor)#移动文本光标

    def keyPressEvent(self, event):#键盘某个键被按下时调用。（我也不清楚为啥，但既然特殊按键可以监听到的话那我就还省了改写input.keyPressEvent函数的事
        alt=event.modifiers()==Qt.AltModifier
        ctrl=event.modifiers()==Qt.ControlModifier#ctrl键
        
        if(event.key()==Qt.Key_Up or event.key()==Qt.Key_Down):
            if(event.key()==Qt.Key_Up):
                self.__inputAsr.IterBack()
            else:
                self.__inputAsr.IterNext()
            tx=self.__inputAsr.GetValue()#从历史记录中获取字串
            self.__input.setText(tx if tx else '')
            cursor=self.__input.textCursor()#用来设置光标
            cursor.movePosition(QTextCursor.End)
            self.__input.setTextCursor(cursor)
        elif(event.key()==Qt.Key_Escape):
            self.__input.clear()
        
    def ClearScreen(self):#清除输出端文本内容
        self.__output.clear()
        self.__AddText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    context=dict()#环境卫生从我做起（可以选择性地将需要的东西传入环境中
    IT=XJ_InteractiveTerminal(context)#如果用了globals()的话IT将暴露在交互系统中，一旦对IT有任何的赋值操作或者其他特殊行为(如销毁窗口啥的)的话都会让程序崩溃
    IT.resize(1300,600)
    context['clear']=lambda:IT.ClearScreen()#预置函数，清空输出端文本内容
    IT.show()

    sys.exit(app.exec())



















