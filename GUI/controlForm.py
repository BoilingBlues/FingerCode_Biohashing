import tkinter as tk
from tkinter.filedialog import askopenfilename
from . import interactive
from . import const
# import bcrypt
import hashlib
import tkinter.font as tkFont

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
        self.frames[cont].tkraise()
        if cont==Logs:
            self.frames[cont].refresh()

class Authentication(tk.Frame):
    '''
    用户认证
    '''
    def __init__(self,parent,root):
        super().__init__(parent)
        self.seedEntry = tk.Entry(self)
        self.seedEntry.pack()
        tk.Button(self,text="认证指纹",command= lambda: self.authentication(root)).pack()
        
    def authentication(self,root):
        seed = self.seedEntry.get()
        seed = int(seed)
        img = interactive.GetIMG()
        result = interactive.ExtractOne(seed,img)
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
        self.parent = parent
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
            self.parent.show_frame(Authentication)
            return
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
        titleFont = tkFont.Font(family='Fixdsys',size=20,weight=tkFont.BOLD)
        titleLabel = tk.Label(self,text="指纹更新",font=titleFont)
        titleLabel.place(relheight=0.2,relwidth=0.5,relx=0.25,rely=0)
        #self.fileNameEntry = tk.Entry(self,textvariable="")
        #self.fileNameEntry.place(relheight=0.1,relwidth=0.5,relx=0.25,rely=0.2)
        #selectFileButton = tk.Button(self,text="选择文件",command=self.selectFile)
        #selectFileButton.place(relheight=0.1,relwidth=0.2,relx=0.75,rely=0.2)
        self.seed = tk.Entry(self,bd=2)
        self.seed.place(relheight=0.1,relwidth=0.5,relx=0.25,rely=0.4)
        seedLabel = tk.Label(self,text="请输入口令")
        seedLabel.place(relheight=0.05,relwidth=0.5,relx=0.25,rely=0.5)
        self.password = tk.Entry(self,bd=2,show="*")
        self.password.place(relheight=0.1,relwidth=0.5,relx=0.25,rely=0.6)
        passwordLabel = tk.Label(self,text="请输入用户密码")
        passwordLabel.place(relheight=0.05,relwidth=0.5,relx=0.25,rely=0.7)
        updateButton = tk.Button(self,text="更新指纹",command= lambda: self.update(root))
        updateButton.place(relheight=0.1,relwidth=0.2,relx=0.4,rely=0.8)
        
    # def selectFile(self):
    #     fileName = askopenfilename(filetypes=[("TIF",".tif")])
    #     self.fileNameEntry.delete(0,'end')
    #     self.fileNameEntry.insert(0,fileName)

    def update(self,root):
        #fileName = self.fileNameEntry.get()
        seed = self.seed.get()
        seed = int(seed)
        img = interactive.GetIMG()
        username = root.username
        password = self.password.get()
        password = password.encode("utf-8")
        h = hashlib.sha256()
        h.update(password)
        password = h.hexdigest()
        # salt = bcrypt.gensalt()
        # hashed = bcrypt.hashpw(password,salt)
        result = interactive.ExtractOne(seed,img)
        if result == const.CONST.FileInvalid:
            tk.messagebox.showinfo("提示","指纹无效")
        else:
            print(username,password,result)
            result = interactive.UpdateFinger(username,password,result)
            if result == const.CONST.UpdateField:
                tk.messagebox.showinfo("提示","更新失败")
            elif result == const.CONST.Ok:
                tk.messagebox.showinfo("提示","更新成功")
        
        