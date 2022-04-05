


class XJ_ListAccessor:#列表访问器，利用该类对列表进行受限式修改
    def __init__(self,lst:list,size=0):#size用于约束容量(该值不大于0时不生效)
        self.__curr=-1 if len(lst)==0 else 0
        self.__size=size
        self.__list=lst
        
    def IterSet(self,curr):#设置位置
        self.__curr=min(max(0,curr),len(self.__list)-1)
    def IterNext(self):#下一个元素
        self.IterSet(self.__curr+1)
    def IterBack(self):#上一个元素
        self.IterSet(self.__curr-1)
    def IterPos(self):#获取self.__curr的值（如果该值为-1说明列表是空的
        return self.__curr
    def IterValid(self):#self.__curr的值超出范围时访问器暂时无效（self.__curr为-1时访问器仍能正常使用
        return self.__curr<len(self.__list)
        
    def GetList(self):
        return self.__list
    def GetValue(self):#获取元素
        curr=self.__curr
        if(self.IterValid()==False or curr==-1):
            return None
        return self.__list[curr]
    def SetValue(self,obj):#设置元素
        if(self.IterValid()==False or curr==-1):
            return False
        self.__list[self.__curr]=obj
    def Insert(self,obj):#插入数据，当超出容量上限时将插入失败
        curr=self.__curr
        if((self.__size>0 and self.__size<=len(self.__list)) or self.IterValid()==False):
            return False
        if(curr==-1):
            curr=0
            self.__curr=0
        self.__list.insert(curr,obj)
        return True
    def ForceInsert(self,obj):#强制插入数据，如果超出容量则将距离当前位置最远的元素删除
        curr=self.__curr
        if(self.IterValid()==False):
            return False
        if(curr==-1):
            curr=0
            self.__curr=0
        self.__list.insert(curr,obj)
        if(self.__size>0 and self.__size<len(self.__list)):#超出容量，删除最远元素
            boundary=int((self.__size+1)/2)#分界
            self.__list.pop(0 if self.__curr>boundary else len(self.__list)-1)
        return True
    def Delete(self):#删除数据
        curr=self.__curr
        if(self.IterValid()==False or curr==-1):
            return False
        self.__list.pop(curr)
        
if __name__=='__main__':
    lst=[1,2,3,4,5]
    acr=XJ_ListAccessor(lst,5)
    acr.Delete()
    acr.IterNext()
    acr.ForceInsert(10)
    acr.Insert(20)
    print(lst)
    
    
    
    