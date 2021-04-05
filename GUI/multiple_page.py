import tkinter as tk
from tkinter import ttk
from . import startPage
from . import appPage
from . import registPage
class Application(tk.Tk):
    '''
    多页面测试程序
        界面于逻辑分离
    '''
    def __init__(self):
        #super函数用于调用父类的一个方法
        super().__init__()
        self.wm_title("多页面切换程序")
        self.wm_geometry('800x500')
        self.username = ""
        self.token = ""
        self.frames = {}
        index = 0
        for F in (startPage.StartPage,appPage.AppPage,registPage.RegistPage):
            frame = F(self,self)
            self.frames[index] = frame
            index += 1
            frame.place(relheight=1.0,relwidth=1.0)
        self.show_frame(0)

    def show_frame(self,cont):
        frame = self.frames[cont]
        # 切换，将指定画布对象移动到显示列表的顶部
        frame.tkraise()


if __name__=='__main__':
    app = Application()
    app.mainloop()