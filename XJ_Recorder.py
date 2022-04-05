#记录器。
#最开始的时候是设计为类的，但发现禁用不了生成对象，不能像C++一样整个私有构造把对象生成操作给封杀，而且py也没有“静态类”的说法
#后来想着python不是自带模块化的方式吗import本文件时文件内定义变量都是唯一的，那不刚好符合我这情况？于是“大道至简”，回到“普真”

exec('import '+__name__)#以歪门邪道的方式引入“<class module "XJ_Recorder">”，要说合不合理那自然很不合理的了这做法，只能说“这邪道别用太多”，万一哪天报错查不到或者修改代价太大呢？
import sys


__record=[]
__stdout=sys.stdout


def write(s):#这函数是给系统调用的
    __record.append(str(s))

def flush():#这函数是给系统调用的。在需要和外设交互时这函数才有它的实际意义，如输出到显示屏、输出到文本文件。在这里并不需要这么做，所以直接pass
    pass

def GetRecord():
    return __record

def SetRecord(record:list):#用来恢复记录
    __record=record

def ClearRecord():
    global __record
    __record=[]#不调用clear()函数是因为想保留旧记录

def Start():
    exec('sys.stdout='+__name__,globals())#只能说，exec太香了
    
def Stop():
    sys.stdout=__stdout
    
def IsRunning():#判断是否处于运行状态
    return sys.stdout!=__stdout



if __name__=='__main__':
    exec('XJ_Recorder='+__name__)#歪门邪道遍地走。该句的实际作用是为了获取引用。本模块内获取本模块的引用实在是难，或者说不合常理，因为正常情况下并不需要这么做
    XJ_Recorder.Start()
    help(list)
    XJ_Recorder.Stop()
    print(XJ_Recorder.GetRecord())
    print(''.join(XJ_Recorder.GetRecord()))
    print(XJ_Recorder)
    
    
    #外界使用的话很省事，就是一句import XJ_Recorder
    #然后该怎么用就怎么用就是了
    
    
    