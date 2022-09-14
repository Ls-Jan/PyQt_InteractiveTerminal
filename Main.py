import sys
import os
from PyQt5.QtWidgets import QApplication
from XJ_InteractiveTerminal import XJ_InteractiveTerminal
from types import MethodType
from pydoc import help

#打包exe后使用时经常会出现该问题：XXX.XXX未找到、XXX导入失败
#在这里简单说明一下原因(也可以顺道参考一下我写的博客：https://blog.csdn.net/weixin_44733774/article/details/126737346)：
#   模块在被用pyinstaller打包时，会把代码中的依赖模块也给打包进程序文件中。如果你导入的是包，那么包内的其他模块并不一定会被加进程序中(原因——优化)
#   然后在模块导入时，sys.meta_path[0](打包程序额外加了一个模块查找器)优先在程序内查找模块/包，
#   如果你导入的是包的话，会优先导入程序内的包，而这些包一般都是残的，也就是在特定场合使用时会发现这里缺那里缺(不能正常使用)
#   其实这本质就是同名模块的导入问题，解决办法有两个，一是在这个Main文件里把模块提前导进来，二是调整sys.meta_path并把缓存sys.modules清了然后再导入(新方法)



def ListPrint(lst,keyword=''):#将列表内容打印
    '''
        打印列表内容(其实只要是可迭代可字符串化的都能传入该函数，不仅限列表
        如果keyword不为空那么将返回有关键词的元素(不区分大小写
        列表打印的列数：ListPrint.cols（值默认为3
        列表打印的列宽：ListPrint.width（值默认为120

        用小数点可以快速调用该函数。小数点调用法：.[变量] (空格) [关键词]
        执行
           .[1,2,3]   3
           .   [1,2,3]    3
        与执行
           ListPrint([1,2,3],'3')
        等价
    '''
    #【关于python内open函数encoding编码问题】https://www.cnblogs.com/wangyi0419/p/11192593.html#:~:text=%E7%94%B3%E6%98%8Eopen%20%28%29%E5%87%BD%E6%95%B0%E7%9A%84%E7%BC%96%E7%A0%81%E6%96%B9%E5%BC%8F%E4%B8%BA%27utf-8%27%EF%BC%8C%E5%8D%B3encoding%3D%22utf-8%22.,%E5%9C%A8%E8%AF%BB%E5%8F%96%E6%96%87%E6%9C%AC%E6%96%87%E4%BB%B6%E7%9A%84%E6%97%B6%E5%80%99%EF%BC%8C%E5%A6%82%E6%9E%9Copen%20%28%29%E5%87%BD%E6%95%B0%E6%B2%A1%E6%9C%89%E5%A3%B0%E6%98%8E%E4%BB%96%E4%BB%AC%E5%A6%82%E4%BD%95%E7%BC%96%E7%A0%81%EF%BC%8Cpython3%E4%BC%9A%E9%80%89%E5%8F%96%E4%BB%A3%E7%A0%81%E6%89%80%E8%BF%90%E8%A1%8C%E7%9A%84%E8%AE%A1%E7%AE%97%E6%9C%BA%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F%E7%9A%84%E9%BB%98%E8%AE%A4%E7%BC%96%E7%A0%81%E4%BD%9C%E4%B8%BAopen%20%28%29%E5%87%BD%E6%95%B0%E7%9A%84%E7%BC%96%E7%A0%81%E6%96%B9%E5%BC%8F%E3%80%82
    #【urwid判断字符宽度】
    #https://blog.csdn.net/weixin_44733774/article/details/124079410
    if(hasattr(ListPrint,'cols')==False):
        ListPrint.cols=3
    if(hasattr(ListPrint,'width')==False):
        ListPrint.width=120
    keyword=str(keyword).lower()

    from urwid.str_util import get_width
    from math import ceil
    cols=ListPrint.cols
    colWidth=int(ListPrint.width/cols)
    print('_'*(colWidth*cols+cols+1))
    cnt=cols
    for i in lst:
        s=str(i)
        if(s.lower().find(keyword)==-1):
            continue
        cnt_ch=len(s)#字符个数
        len_ch=sum([get_width(ord(ch)) for ch in s])#字符实际长度
        ncol=ceil(len_ch/colWidth)#需要的列宽个数，向上取整
        if(ncol==0):#如果s是空字符串，那么ncol的值为0，所以需要人为给它设置1
            ncol=1
        if(ncol>cnt):#超过剩余的宽度
            if(cnt!=cols):#这不是新行
                print('|{:^{}}|'.format('',colWidth*cnt+cnt-1))
                cnt=cols
            ncol=min(cnt,ncol)
        cnt=cnt-ncol
        if(cols==1):
            print(s,end='')
        else:
            print('|{:^{}}'.format(s,colWidth*ncol-(len_ch-cnt_ch)+ncol-1),end='')
        if(cnt==0):
            cnt=cols
            print('|' if cols>1 else '')
    if(cnt!=cols):
        print('|{:^{}}|'.format('',colWidth*cnt+cnt-1))
    print('￣'*((colWidth*cols+cols+1)>>1))
    print()

def QuicklyInquiry(obj,keyword='',formatPrint=False):#XJ的快速查询小助手，如果格式化输出为真那么将执行print语句，否则将返回列表
    '''
        XJ的快速查询小助手，本质上是返回dir(obj)，关键字keyword用于筛选列表中的元素。
        如果formatPrint为真那么将打印结果，为假则返回列表。

        用小数点可以快速调用该函数。小数点调用法：..[变量] (逗号/空格) [关键字]
        执行
           ..list c
           ..list,c
           ..  list , c
        与执行
           QuicklyInquiry(list,'c',True)
        等价
    '''
    lst=list(filter(lambda s:s.lower().find(keyword.lower())!=-1,dir(obj)))
    if(formatPrint):
        ListPrint(lst)
    else:
        return lst

def ChangeDir(path=None):#修改当前路径。path为None或者为空时返回当前路径；path无效时提示路径不存在
    '''
        修改当前路径，并返回路径结果。
        path无效时不修改路径。

        用cd指令可以快速调用该函数： cd [路径]
    '''
    if(type(path)!=type(None)):
        if(type(path)!=str):
            print("参数错误，请传入字符串")
            return
        if(len(path)>0):
            if(os.path.isdir(path)==False):
                if(os.path.isfile(path)):
                    print("“{}”不是文件夹".format(path))
                else:
                    print("路径“{}”不存在".format(path))
                return
            else:
                os.chdir(path)
                sys.path[0]=os.path.abspath(os.curdir)#修改当前路径
    return os.path.abspath(os.curdir)#返回当前路径


def ListDir():#返回当前路径下的文件+文件夹（分成两个列表返回
    '''
        返回当前路径下的文件+文件夹（分成两个列表返回

        用ls指令可以快速调用该函数并且将结果以表格形式打印：ls
    '''
    import os#仅在域内生效，很方便
    file=[]
    folder=[]
    for p in os.listdir():
        if(os.path.isdir(p)):
            folder.append(p)
        else:
            file.append(p)
    return file,folder

# def Import(self,module:str):#新添的Import方式，以强制导入模块
    # 仔细分析后发现，重导模块的一个方法是，把sys.modules缓存清了。准备嘎嘎乱杀
    # 摸了，不乱杀了，有心情再说
    
def DeleteModule(module:str):#删掉模块(删的是模块缓存sys.modules)
    '''
        将模块/包的缓存删掉，用于模块/包的再导入
        主要应对于某些包的导入问题
        
        用--指令可以快速调用该函数：-- module
        (调用--指令会同时调用del module，可以当作快速del变量的方法
    '''
    # 大佬的文章就是详细，不愧大佬，不少地方都参考借鉴其内容：https://blog.csdn.net/jeffery0207/article/details/120612313
    if(module in sys.modules):
        sys.modules.pop(module)
    
def TextPreprocess(self,text):#文本预处理，与“XJ_InteractiveTerminal.TextPreprocess”绑定，用于执行额外的功能(例如清空输出端文本、设置函数的快速调用、过滤有害命令
    context=self.GetContext()#可能有别的用途呢？(可以通过修改该字典来修改环境变量)
    if(text.find('help()')!=-1):#有害指令
        return 'help'
    if(text.strip()=='ls'):#【打印当前路径下的文件+文件夹】
        return '[ListPrint(lst) for lst in ListDir()] and None'#为了不引入变量lst，使用这种奇怪的做法
    if(text.find('cd')==0):#【切换当前路径】
        return 'ChangeDir("{}")'.format(text[2:].strip())
    if(text.find('...')==0):#【清空输出端内容】
        self.ClearScreen()
        return ''
    if(text.find('..')==0):#【调用QuicklyInquiry】
        text=text[2:].strip()#吃掉首尾空白符
        if(len(text)==0):
            return 'help(QuicklyInquiry)'
        keyword=''
        sep=text.find(',')
        if(sep==-1):
            sep=text.find(' ')
        if(sep!=-1):
            keyword=''.join(list(filter(lambda ch:ch if ch!=' ' and ch!=',' else '',text[sep+1:])))#清除关键字中无用的逗号和空格
            text=text[:sep]
        return "QuicklyInquiry({},'{}',True)".format(text,keyword)
    if(text.find('.')==0):#【调用ListPrint】
        text=text[1:].strip()#吃掉首尾空白符
        if(len(text)==0):
            return 'help(ListPrint)'
#        text=''.join(text.split(','))
        text=text.split()
        return "ListPrint({},'{}')".format(text[0],text[1] if len(text)>1 else '')
    if(text.find('?')==0):#【调用help】
        text=text[1:].strip()#吃掉首尾空白符
        if(len(text)==0):
            return "help"
        return "help({})".format(text)
    if(text.find('--')==0):#【调用DeleteModule】(新增)
        text=text[2:].strip()#吃掉首尾空白符
        if(len(text)==0):
            return 'help(DeleteModule)'
        if(text in context):
            context.pop(text)
        return f"DeleteModule('{text}')"
    return text


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.path=[#人为修改路径，因为程序运行时的sys.path与脚本运行时的sys.path是不一致的，所以要强制修改。在默认交互端(即传统黑窗口输入py进入py交互)中获取以下绝对路径
        os.path.abspath(os.curdir),
        r'C:\Users\Administrator\AppData\Local\Programs\Python\Python37\python37.zip',
        r'C:\Users\Administrator\AppData\Local\Programs\Python\Python37\DLLs',
        r'C:\Users\Administrator\AppData\Local\Programs\Python\Python37\lib',
        r'C:\Users\Administrator\AppData\Local\Programs\Python\Python37',
        r'C:\Users\Administrator\AppData\Roaming\Python\Python37\site-packages',
        r'C:\Users\Administrator\AppData\Local\Programs\Python\Python37\lib\site-packages',
        r'C:\Users\Administrator\AppData\Local\Programs\Python\Python37\lib\site-packages\win32',
        r'C:\Users\Administrator\AppData\Local\Programs\Python\Python37\lib\site-packages\win32\lib',
        r'C:\Users\Administrator\AppData\Local\Programs\Python\Python37\lib\site-packages\Pythonwin',
        r'C:\Users\Administrator\AppData\Local\Programs\Python\Python37\Lib',
        r'C:\Users\Administrator\AppData\Local\Programs\Python\Python37\Lib\site-packages',
        os.path.abspath(os.curdir),
    ]#反斜杠，如果不需要转义则要在字串前添加r前缀
    sys.meta_path.insert(0,sys.meta_path.pop())#参考文章可以知道这meta_path控制导入时的优先级：https://blog.csdn.net/jeffery0207/article/details/120612313
    #其中meta_path[-1]是根据sys.path搜寻模块的(这是模块导入的默认最终手段)，把这玩意儿调到最前的主要目的是让模块导入能优先根据sys.path导入
    
    context=dict()#环境卫生从我做起（选择性地将需要的东西传入命名空间中
    context['ListPrint']=ListPrint
    context['ListDir']=ListDir
    context['ChangeDir']=ChangeDir
    context['QuicklyInquiry']=QuicklyInquiry
    context['DeleteModule']=DeleteModule
    context['help']=help#加入“help”命令

    IT=XJ_InteractiveTerminal(context.copy())#若传入globals()则会有大量的程序无关变量加入到环境中(如变量IT)，增大脚本崩溃风险(如对IT赋值)。可以在程序中执行".globals()"以查看命名空间。
    IT.TextPreprocess=MethodType(TextPreprocess,IT)#设置文本的预处理
    IT.resize(1300,600)
    IT.show()

    sys.exit(app.exec())







