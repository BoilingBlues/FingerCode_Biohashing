import tkinter as tk
from tkinter import ttk
import hashlib
from . import interactive
from . import const
class RegistPage(tk.Frame):
    '''
    注册页
    '''
    def __init__(self,parent,root):
        super().__init__(parent)
        label = tk.Label(self,text = "注册")
        self.userName = tk.Entry(self,bd=5)
        self.password = tk.Entry(self,bd=5)
        registBotton = ttk.Button(self,text="注册",command=lambda: self.regist()) 
        button = ttk.Button(self, text="返回主页", command=lambda: root.show_frame(0))
        label.pack()
        self.userName.pack()
        self.password.pack()
        registBotton.pack()
        button.pack()

    def regist(self):
        #用户名小于20个字符
        userName = self.userName.get()
        password = self.password.get()
        password = password.encode('utf-8')
        h = hashlib.sha256()
        h.update(password)
        password = h.hexdigest()
        result = interactive.Regist(userName,password)
        if result == const.CONST.Ok:
            tk.messagebox.showinfo("提示","注册成功")
        elif result == const.CONST.UserRepeat:
            tk.messagebox.showinfo("提示","用户名重复")
        elif result == const.CONST.TimeOutError:
            tk.messagebox.showinfo("警告","网络错误")
        elif result == const.CONST.TimeOutError:
            tk.messagebox.showinfo("警告","未知错误")