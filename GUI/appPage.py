import tkinter as tk
from tkinter import ttk
from . import controlForm 

class AppPage(tk.Frame):
    '''
    应用页面
    '''
    def __init__(self,parent,root):
        super().__init__(parent)
        self.frm2 = controlForm.ControlForm(self,root)
        self.frm1 = SelectForm(self,root)
        self.frm1.place(relheight=1.0,relwidth=0.1)
        self.frm2.place(relx=0.1,relwidth=0.9,relheight=1.0)
class SelectForm(tk.Frame):
    '''
    侧边选择栏
    '''
    def __init__(self,parent,root):
        super().__init__(parent,bg='gray')
        ttk.Button(self, text="用户认证", command=lambda: parent.frm2.show_frame(controlForm.Authentication)).place(relwidth=1.0,relheight=0.1)
        ttk.Button(self, text="认证日志", command=lambda: parent.frm2.show_frame(controlForm.Logs)).place(rely=0.1,relwidth=1.0,relheight=0.1)
        ttk.Button(self, text="指纹更新", command=lambda: parent.frm2.show_frame(controlForm.Update)).place(rely=0.2,relwidth=1.0,relheight=0.1)
        ttk.Button(self, text="去到主页", command=lambda: self.back(root)).place(rely=0.9,relwidth=1.0,relheight=0.1)
    def back(self,root):
        root.username=""
        root.token=""
        root.show_frame(0)
        

