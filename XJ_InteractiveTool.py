import XJ_Recorder
import traceback#Python 输出详细的异常信息(traceback)方式：https://cloud.tencent.com/developer/article/1731086

class XJ_InteractiveTool:#单线程工具，多线程下使用时容易翻车请注意。直接原因是XJ_Recorder的启动和关闭，根本原因是公共资源，对公共资源的解决办法是加锁(死锁警告！)
    def __init__(self,varDict=dict()):#记得传入变量字典，环境卫生从我做起
        self.__text=""#待输入的字符串
        self.__holdOn=False#判断是否多行输入
        self.__varDict=varDict

    def HoldOn(self):#获取当前的输入状态(如果是处于多行输入的状态那么该值为真
        return self.__holdOn
        
    def ReadOrder(self,text:str):#传入文本(包括空文本)，然后执行结果
        emptyInput=len(text)==0#判断传入的文本是否为空
        holdOn=self.__holdOn
        locals=self.__varDict
        text=self.__text+text+'\n'

        oldRecord=XJ_Recorder.GetRecord()#保存旧记录
        XJ_Recorder.ClearRecord()#暂时清空记录
        status=XJ_Recorder.IsRunning()#记录运行状态
        XJ_Recorder.Start()#开始记录
        
        if(holdOn==False and emptyInput==False):#如果当前是第一行输入，并且当前输入不为空
            try:
                code=compile(text,'','eval')#尝试作为eval进行编译
                rst=eval(code,locals)#执行代码
                if(type(rst)!=type(None)):#如果结果不空那就输出结果
                    print(rst)
            except:
                try:
                    code=compile(text,'','exec')#尝试作为exec进行编译【进行语法检查】
                    exec(code,locals)#执行代码
                except Exception as err:
                    if(str(err).find("EOF")!=-1):#如果只是EOF错误那么说明是多行输入，置holdOn为真
                        holdOn=True
                    else:
                        self.__PrintTrackBack()#输出异常
        elif(holdOn==True):#如果当前并不是第一行输入
            if(emptyInput):#如果当前输入为空
                holdOn=False
            try:
                code=compile(text,'','exec')#尝试作为exec进行编译【进行语法检查】
                if(holdOn==False):#如果holdOn假，说明代码已经输入完毕
                    exec(code,locals)#执行代码
            except Exception as err:
                if(str(err).find("EOF")==-1 or holdOn==False):#如果不是EOF错误，或者虽然是EOF错误但是holdOn为假的话那就输出错误
                    self.__PrintTrackBack()#输出异常
                    holdOn=False
        self.__text=text if holdOn else ""#如果执行完上面的if-else代码段后holdOn为假那么就清空text
        self.__holdOn=holdOn
        
        if(status==False):#之前若不处于运行状态的话那就关闭记录
            XJ_Recorder.Stop()#停止记录
        newRecord=XJ_Recorder.GetRecord()#获取新记录
        XJ_Recorder.SetRecord(oldRecord)#恢复旧记录
 
        return newRecord
        
    def VarDict(self):#获取self.__varDict
        return self.__varDict
        
    def __PrintTrackBack(self):#打印异常
        err=traceback.format_exc()
        if(err.count('Traceback')>1):
            err=err[err.find('\nTraceback'):]#清掉第一份错误，那个没啥用
        else:
            err='\n'+err#加上一个回车
        err=err[err.find('<module>')+8:]#去除多余内容
        err=err.replace('\n','\n* ')#每行前面添加一点符号
        err=err[1:]#去掉第一个回车
        err='_'*100+'\n'+err+'\n'+'￣'*50#整两条横线围一下
        print(err)

if __name__=='__main__':
    IT=XJ_InteractiveTool(globals())

    while(True):
        print(''.join(IT.ReadOrder(input("..."if IT.HoldOn() else ">>>"))),end='')
        








        

        
        