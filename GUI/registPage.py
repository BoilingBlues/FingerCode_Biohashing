import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import hashlib
from . import interactive
from . import const
class RegistPage(tk.Frame):
    '''
    注册页
    '''
    def __init__(self,parent,root):
        super().__init__(parent)
        self.root = root

        titleFont = tkFont.Font(family='Fixdsys',size=20,weight=tkFont.BOLD)
        titleLabel = tk.Label(self,text = "注册新用户",font=titleFont)
        self.userName = tk.Entry(self,bd=2)
        usernameLabel = tk.Label(self,text = "请输入您的用户名")
        passwordLabel = tk.Label(self,text = "请输入您的密码")
        repasswordLabel = tk.Label(self,text = "请再次输入您的用户名")
        self.password = tk.Entry(self,show="*",bd=2)
        self.repassword = tk.Entry(self,show="*",bd=2)
        registBotton = ttk.Button(self,text="注册",command=lambda: self.regist()) 
        button = ttk.Button(self, text="返回主页", command=lambda: root.show_frame(0))
        titleLabel.place(relheight=0.3,relwidth=0.4,relx=0.3,rely=0)
        self.userName.place(relheight=0.1,relwidth=0.4,relx=0.3,rely=0.3)
        usernameLabel.place(relheight=0.05,relwidth=0.4,relx=0.3,rely=0.4)
        self.password.place(relheight=0.1,relwidth=0.4,relx=0.3,rely=0.475)
        passwordLabel.place(relheight=0.05,relwidth=0.4,relx=0.3,rely=0.575)
        self.repassword.place(relheight=0.1,relwidth=0.4,relx=0.3,rely=0.65)
        repasswordLabel.place(relheight=0.05,relwidth=0.4,relx=0.3,rely=0.75)
        registBotton.place(relheight=0.1,relwidth=0.4,relx=0.3,rely=0.85)
        button.place(relheight=0.1,relwidth=0.15,relx=0.8,rely=0.85)

    def regist(self):
        #用户名小于20个字符
        userName = self.userName.get()
        password = self.password.get()
        repassword = self.repassword.get()
        if len(userName)<6 or len(userName)>20 or not all(ord(c) <128 for c in userName):
            tk.messagebox.showinfo("提示","用户名必须为6到20位的ascii码")
            return
        if len(password)<6:
            tk.messagebox.showinfo("提示","密码位数不得少于6位")
            return
        if password!=repassword:
            tk.messagebox.showinfo("提示","两次输入的密码不一致")
            return
        password = password.encode('utf-8')
        h = hashlib.sha256()
        h.update(password)
        password = h.hexdigest()
        result = interactive.Regist(userName,password)
        if result == const.CONST.Ok:
            tk.messagebox.showinfo("提示","注册成功")
            self.root.show_frame(0)
        elif result == const.CONST.UserRepeat:
            tk.messagebox.showinfo("提示","用户名重复")
        elif result == const.CONST.TimeOutError:
            tk.messagebox.showinfo("警告","网络错误")
        elif result == const.CONST.TimeOutError:
            tk.messagebox.showinfo("警告","未知错误")