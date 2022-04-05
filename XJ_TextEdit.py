import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QTextCursor,QFont,QTextOption
from PyQt5.QtCore import Qt,pyqtSignal

class XJ_TextEdit(QTextEdit):
    textSent=pyqtSignal(str)#槽信号，当发送文本时发送信号
    #textChanged，为自带的槽信号，文本内容更改时触发
    def __init__(self,parent=None):
        super(XJ_TextEdit, self).__init__(parent)
        self.__oneLineMode=False
        self.__sendMsgMode=True
        self.setFont(QFont(self.font().family(),12))#简单设置下字体，初始字体的字号太小了
    def OneLineMode(self,flag:bool):#单行模式，文本内容将只保留最后一行字串，并且窗口大小修改为单行大小，按回车将不会换行
        self.__oneLineMode=flag
        if(flag):#如果为单行模式，对文本内容进行修改
            text=self.toPlainText()#文本内容
            sep=text.find('\n')+1#寻找回车符的后一个字符
            if(sep):
                while(sep):
                    self.textSent.emit(text[:sep])#连同回车符也一并发送
                    text=text[sep:]#新行内容
                    sep=text.find('\n')+1#寻找回车符的后一个字符
                self.setText(text)
        #对组件的模式策略进行设置
        height=self.fontMetrics().lineSpacing()+10#获取单行字串的最低高度（10是魔法数字，非常恶意，是一点一点试出来的结果
        if(flag):#如果为单行模式，取消“自动换行”，并且把滚动条全隐藏
            self.setWordWrapMode(QTextOption.NoWrap)#设置换行模式为“不自动换行”
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)#隐藏行滚动条
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)#隐藏纵滚动条
            self.setMinimumHeight(height)
            self.setMaximumHeight(height)
        else:#多行模式则把“自动换行”恢复，并且显示滚动条
            self.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)#设置换行模式为默认的“智能换行”
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)#显示行滚动条
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)#显示纵滚动条
            self.setMinimumHeight(height)
            self.setMaximumHeight(QApplication.desktop().screenGeometry().height())

    def SendMsgMode(self,flag:bool):#文本发送模式，如果为真那么按下回车键(多行模式还得同时按下Ctrl)时将会清除文本内容并且触发textSent信号
        self.__sendMsgMode=flag
    def keyPressEvent(self, event):#键盘某个键被按下时调用
        enter=(event.key()==Qt.Key_Return or event.key()==Qt.Key_Enter)#回车键
        ctrl=event.modifiers()==Qt.ControlModifier#ctrl键
        text=self.toPlainText()#文本内容
        
        if(enter):#按下回车键
            if(self.__oneLineMode or ctrl):#单行模式按回车触发，多行模式按回车+ctrl触发
                if(self.__sendMsgMode):#如果设置了信息发送模式
                    self.textSent.emit(text)#触发信号
                    self.setText("")#清除文本
                return
        super().keyPressEvent(event)#没有触发文本发送时该干啥干啥
    def Search(self,keyword):#搜索关键词，搜索成功将会高亮文本，并且返回True，否则返回False
        cursor = self.textCursor()#光标
        text=self.toPlainText()#文本内容
        L=text.find(keyword,cursor.position())#在光标位置作为起点开始寻找
        if(L==-1):
            L=text.find(keyword)#从头开始寻找
            if(L==-1):
                return False
        R=L+len(keyword)
        cursor.setPosition(L,QTextCursor.MoveAnchor)#移动光标
        cursor.setPosition(R,QTextCursor.KeepAnchor)#拖动光标
        self.setTextCursor(cursor)
        


if __name__ == '__main__':
    app = QApplication(sys.argv)


    te=XJ_TextEdit()
    te.textSent.connect(lambda s:print("【OneLine】\n",s))
    te.setText("123456789\nABCDEFGHI\n123456789")
    te.append('<font color="red"> sss </font>')
    te.Search("456")
    te.setFont(QFont('楷体',20))
#    te.OneLineMode(True)
    te.show()
    sys.exit(app.exec())




    

















