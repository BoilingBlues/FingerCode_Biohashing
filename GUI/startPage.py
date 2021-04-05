import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
from . import interactive
from . import const

class StartPage(tk.Frame):
    '''
    主页
    '''
    def __init__(self,parent,root):
        super().__init__(parent)
        label = tk.Label(self,text = "这里是主页")
        label.pack()
        self.entry = tk.Entry(self,bd=5)
        self.entry.pack()
        button = ttk.Button(self, text="登入", command=lambda: self.login(root))
        button.pack()
        button1 = ttk.Button(self, text="注册", command=lambda: root.show_frame(2))
        button1.pack()

    def login(self,root):
        username = self.entry.get()
        result = interactive.Login(username)
        if result == const.CONST.Ok:
            root.username=username
            root.show_frame(1)
        elif result == const.CONST.TimeOutError:
            tk.messagebox.showinfo("错误","网络异常")
        elif result == const.CONST.NoUser:
            tk.messagebox.showinfo("提示","用户名不存在")
        elif result == const.CONST.UnKnown:
            tk.messagebox.showinfo("错误","未知异常")