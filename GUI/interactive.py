import requests
import json
from . import const
import sys
sys.path.append("..")
from fingercode import fingercode
from biohashing import BioCode
import ctypes
import datetime
import numpy as np
from cv2 import cv2 as cv

root_path = "http://47.102.198.54:8080"
regist_path = root_path + "/regist"
login_path = root_path + "/login"
changePassword_path = root_path + "/changePassword"
update_path = root_path + "/api/update"
authentication_path = root_path + "/api/authentication"
logs_path = root_path + "/api/logs"

headers = {'Content-Type':'application/json'}

def timeout(func):
    def tryTimeOut(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except requests.exceptions.RequestException:
            return const.CONST.TimeOutError
        except:
            return const.CONST.UnKnown
    return tryTimeOut

@timeout
def Regist(username,password):
    data = {
        'username':username,
        'password':password
    }
    response = requests.post(url=regist_path,headers=headers,data=json.dumps(data),timeout=(5,10))
    if response.status_code==200:
        return const.CONST.Ok
    else:
        return const.CONST.UserRepeat


@timeout
def Login(username):
    data = {
        'username':username
    }
    response = requests.post(url=login_path,headers=headers,data=json.dumps(data),timeout=(5,10))
    if response.status_code!=200:
        return const.CONST.NoUser
    return const.CONST.Ok

@timeout
def Authenticat(username,biocode):
    data = {
        'username':username,
        'biocode':biocode
    }
    response = requests.post(url=authentication_path,headers=headers,data=json.dumps(data),timeout=(5,10))
    if response.status_code!=200:
        return const.CONST.AuthenticationField
    else:
        token = json.loads(response.content)["token"]
        return token

@timeout
def UpdateFinger(username,password,biocode):
    data = {
        'username':username,
        'password':password,
        'biocode':biocode
    }
    response = requests.post(url=update_path,headers=headers,data=json.dumps(data),timeout=(5,10))
    if response.status_code!=200:
        return const.CONST.UpdateField
    else:
        return const.CONST.Ok

@timeout
def GetLog(token,page):
    data = {
        'token':token,
        'page':page
        }
    response = requests.post(url=logs_path,headers=headers,data=json.dumps(data),timeout=(5,10))
    if response.status_code!=200:
        return const.CONST.LogField
    else:
        result = json.loads(response.content)
        if len(result["list"])==0:
            return const.CONST.NoMore
        else:
            return result["list"]


def ExtractOne(seed,img):
    try:
        preTime = datetime.datetime.now()
        finger = fingercode.fingercode(img)
        print(datetime.datetime.now()-preTime,"总计")
        preTime = datetime.datetime.now()
        finger = BioCode.BioCode(seed,finger)
        print(datetime.datetime.now()-preTime,"特征加密")
        result = ""
        for i in finger:
            result += str(i)
        print(result)
        return result
    except:
        return const.CONST.FileInvalid


def GetIMG():
    buffer = np.zeros([300*400],dtype=np.uint8)
    dll = ctypes.cdll.LoadLibrary('./GUI/dll/finger_image_DLL.dll')
    dll.GetIMG.restype = ctypes.c_int
    dll.GetIMG.argtypes = [np.ctypeslib.ndpointer(dtype=np.uint8,ndim=1,flags="C_CONTIGUOUS")]
    ret = dll.GetIMG(buffer)
    if ret != 0:
        return const.CONST.DeviceError
    img = buffer.reshape((400,300))
    return img

