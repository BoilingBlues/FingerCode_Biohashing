import tkinter as tk
from tkinter.filedialog import askopenfilename
from . import interactive
from . import const
# import bcrypt
import hashlib
import tkinter.font as tkFont
import _thread as thread

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
        titleFont = tkFont.Font(family='Fixdsys',size=20,weight=tkFont.BOLD)
        titleLabel = tk.Label(self,text="用户认证",font=titleFont)
        titleLabel.place(relheight=0.2,relwidth=0.5,relx=0.25,rely=0)
        self.seedEntry = tk.Entry(self)
        self.seedEntry.place(relheight=0.1,relwidth=0.5,relx=0.25,rely=0.4)
        seedLabel = tk.Label(self,text="请输入口令")
        seedLabel.place(relheight=0.05,relwidth=0.5,relx=0.25,rely=0.5)
        self.button = tk.Button(self,text="认证指纹",command= lambda: self.botton(root))
        self.button.place(relheight=0.1,relwidth = 0.5,relx=0.25,rely=0.7)


    def botton(self,root):
        self.button['text'] = "请录入指纹"
        thread.start_new_thread(self.authentication,(root,))


    def authentication(self,root):
        seed = self.seedEntry.get()
        if not seedLigit(seed):
            tk.messagebox.showinfo("提示","口令为6位数字")
            return
        seed = int(seed)
        img = interactive.GetIMG()
        if isinstance(img,int) and img == const.CONST.DeviceError:
            tk.messagebox.showinfo("错误","设备连接错误，请安装驱动或检查设备连接")
            return
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
        self.button['text'] = "认证指纹"



class Logs(tk.Frame):
    '''
    用户日志
    '''
    def __init__(self,parent,root):
        super().__init__(parent)
        self.root=root
        self.page = 1
        self.parent = parent
        titleFont = tkFont.Font(family='Fixdsys',size=20,weight=tkFont.BOLD)
        titleLabel = tk.Label(self,text="用户认证",font=titleFont)
        titleLabel.place(relheight=0.2,relwidth=0.5,relx=0.25,rely=0)
        self.text = tk.Text(self,width=60,height=21)
        #self.text['state'] = 'disabled'
        self.text.bind("<Key>", lambda a: "break")
        self.text.place(relheight=0.55,relwidth=0.6,relx=0.2,rely=0.2)
        pageUp = tk.Button(self,text="上一页",command=lambda: self.getContent(self.page-1))
        pageUp.place(relheight = 0.1,relwidth=0.2,relx=0.2,rely=0.8)
        self.pageLabel = tk.Label(self,text=str(self.page))
        self.pageLabel.place(relheight=0.1,relwidth=0.2,relx=0.4,rely = 0.8)
        pageDown = tk.Button(self,text="下一页",command=lambda: self.getContent(self.page+1))
        pageDown.place(relheight = 0.1,relwidth=0.2,relx=0.6,rely=0.8)

    def refresh(self):
        self.getContent(self.page)
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
                pre = i['CreateTime']
                time = pre[0:10]+" " + pre[11:19] + " " + pre[20:]
                content = " "*3 + "%02d"%count + " "*10 + time + " "*10 + i['Content']+'\n'
                self.text.insert('end',content)
                count += 1
        self.pageLabel['text'] = str(self.page)
        

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
        self.updateButton = tk.Button(self,text="更新指纹",command= lambda: self.botton(root))
        self.updateButton.place(relheight=0.1,relwidth=0.2,relx=0.4,rely=0.8)
        
    # def selectFile(self):
    #     fileName = askopenfilename(filetypes=[("TIF",".tif")])
    #     self.fileNameEntry.delete(0,'end')
    #     self.fileNameEntry.insert(0,fileName)
    
    def botton(self,root):
        self.updateButton['text'] = "请录入指纹"
        thread.start_new_thread(self.update,(root,))

    def update(self,root):
        #fileName = self.fileNameEntry.get()
        seed = self.seed.get()
        if not seedLigit(seed):
            tk.messagebox.showinfo("提示","口令为6位数字")
            return
        seed = int(seed)
        img = interactive.GetIMG()
        if isinstance(img,int) and img == const.CONST.DeviceError:
            tk.messagebox.showinfo("错误","设备连接错误，请安装驱动或检查设备连接")
            return
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
        
        self.updateButton['text'] = "更新指纹"

def seedLigit(seed):
    if len(seed)!=6 or not all(48<ord(c) and ord(c) <57 for c in seed):
        return False
    return True





