import tkinter as tk
from tkinter.filedialog import askopenfilename
from . import interactive
from . import const
# import bcrypt
import hashlib

class ControlForm(tk.Frame):
    '''
    操作区域
    '''
    def __init__(self,parent,root):
        super().__init__(parent)
        self.frames = {}

        for F in (Authentication,Logs,Update):
            frame = F(self,root)
            self.frames[F] = frame
            frame.place(relwidth=1.0,relheight=1.0)
        self.show_frame(Authentication)

    def show_frame(self,cont):
        if cont==Logs:
            self.frames[cont].refresh()
        self.frames[cont].tkraise()

class Authentication(tk.Frame):
    '''
    用户认证
    '''
    def __init__(self,parent,root):
        super().__init__(parent)
        self.fileNameEntry = tk.Entry(self,textvariable="")
        self.fileNameEntry.pack()
        tk.Button(self,text="打开文件",command=self.selectFile).pack()
        tk.Button(self,text="认证指纹",command= lambda: self.authentication(123456,root)).pack()
        
    def selectFile(self):
        fileName = askopenfilename(filetypes=[("TIF",".tif")])
        self.fileNameEntry.delete(0,'end')
        self.fileNameEntry.insert(0,fileName)
    def authentication(self,seed,root):
        filename = self.fileNameEntry.get()
        result = interactive.ExtractOne(seed,filename)
        if result== const.CONST.FileInvalid:
            tk.messagebox.showinfo("提示","指纹无效")
        else:
            result = interactive.Authenticat(root.username,result)
            if result== const.CONST.AuthenticationField:
                tk.messagebox.showinfo("提示","认证失败")
            else:
                root.token=result
                tk.messagebox.showinfo("提示","认证成功")

class Logs(tk.Frame):
    '''
    用户日志
    '''
    def __init__(self,parent,root):
        super().__init__(parent)
        self.root=root
        self.page = 1
        self.text = tk.Text(self,width=60,height=21)
        #self.text['state'] = 'disabled'
        self.text.bind("<Key>", lambda a: "break")
        self.text.pack()
        pageUp = tk.Button(self,text="上一页",command=lambda: self.getContent(self.page-1))
        pageUp.pack(side='left')
        pageDown = tk.Button(self,text="下一页",command=lambda: self.getContent(self.page+1))
        pageDown.pack(side='right')
        refreshButton = tk.Button(self,text="刷新",command=self.refresh)
        refreshButton.pack(side='bottom')
    def refresh(self):
        self.getContent(1)
    def getContent(self,page):
        if page<=0:
            tk.messagebox.showinfo("提示","已经是第一页了")
            return
        root = self.root


        if root.token=="":
            tk.messagebox.showinfo("提示","请先身份验证")
        result = interactive.GetLog(root.token,page-1)
        if result==const.CONST.LogField:
            tk.messagebox.showinfo("提示","获取失败")
        elif result==const.CONST.NoMore:
            tk.messagebox.showinfo("提示","没有更多了")
        else:
            self.page = page
            self.text.delete('1.0','end')
            count = 1
            for i in result:
                content = "%02d"%count + " "*10 + i['CreateTime'] + " "*10 + i['Content']+'\n'
                self.text.insert('end',content)
                count += 1

        

class Update(tk.Frame):
    '''
    指纹更新
    '''
    def __init__(self,parent,root):
        super().__init__(parent)
        self.fileNameEntry = tk.Entry(self,textvariable="")
        self.fileNameEntry.pack()
        tk.Button(self,text="打开文件",command=self.selectFile).pack()
        self.password = tk.Entry(self,bd=5)
        self.password.pack()
        tk.Button(self,text="更新指纹",command= lambda: self.update(123456,root)).pack()
        
    def selectFile(self):
        fileName = askopenfilename(filetypes=[("TIF",".tif")])
        self.fileNameEntry.delete(0,'end')
        self.fileNameEntry.insert(0,fileName)

    def update(self,seed,root):
        fileName = self.fileNameEntry.get()
        username = root.username
        password = self.password.get()
        password = password.encode("utf-8")
        h = hashlib.sha256()
        h.update(password)
        password = h.hexdigest()
        # salt = bcrypt.gensalt()
        # hashed = bcrypt.hashpw(password,salt)
        result = interactive.ExtractOne(seed,fileName)
        if result == const.CONST.FileInvalid:
            tk.messagebox.showinfo("提示","指纹无效")
        else:
            print(username,password,result)
            result = interactive.UpdateFinger(username,password,result)
            if result == const.CONST.UpdateField:
                tk.messagebox.showinfo("提示","更新失败")
            elif result == const.CONST.Ok:
                tk.messagebox.showinfo("提示","更新成功")
        
        