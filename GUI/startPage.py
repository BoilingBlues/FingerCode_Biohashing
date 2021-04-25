import tkinter as tk
import tkinter.font as tkFont
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
        titleFont = tkFont.Font(family='Fixdsys',size=40,weight=tkFont.BOLD)
        #buttonFont = tkFont.Font(family='Fixdsys',size=10,weight=tkFont.BOLD)

        label = tk.Label(self,text = "指 纹 认 证 系 统",font = titleFont)
        label.place(relheight=0.4,relwidth=0.8,relx=0.1,rely=0 )
        self.entry = tk.Entry(self,bd=2)
        self.entry.place(relheight = 0.1,relwidth = 0.4,relx = 0.3,rely = 0.5)
        label2 = tk.Label(self,text = "请在此键入您的用户名")
        label2.place(relheight=0.05,relwidth = 0.6,relx=0.2,rely=0.6)
        button = ttk.Button(self, text="登入", command=lambda: self.login(root))
        button.place(relheight = 0.1,relwidth = 0.4,relx = 0.3,rely = 0.7)
        button1 = ttk.Button(self, text="注册", command=lambda: root.show_frame(2))
        button1.place(relheight = 0.1,relwidth = 0.4,relx = 0.3,rely = 0.85)

    def login(self,root):
        username = self.entry.get()
        if len(username)<6 or len(username)>20 or not all(ord(c) <128 for c in username):
            tk.messagebox.showinfo("提示","用户名错误")
            return
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