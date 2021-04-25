import requests
import json
from . import const
import sys
sys.path.append("..")
from fingercode import fingercode
from biohashing import BioCode
import ctypes
import numpy as np
from cv2 import cv2 as cv

root_path = "http://172.20.48.1:8080"
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
        finger = fingercode.fingercode(img)
        finger = BioCode.BioCode(seed,finger)
        result = ""
        for i in finger:
            for j in i:
                result += str(j)
        return result
    except:
        return const.CONST.FileInvalid


def GetIMG():
    buffer = np.zeros([300*400],dtype=np.uint8)
    dll = ctypes.cdll.LoadLibrary('./GUI/dll/finger_image_DLL.dll')
    dll.GetIMG.argtypes = [np.ctypeslib.ndpointer(dtype=np.uint8,ndim=1,flags="C_CONTIGUOUS")]
    dll.GetIMG(buffer)
    img = buffer.reshape((400,300))
    return img

if __name__ == "__main__":
    print(Authenticat("12341","0001000110100011100100000101111111101011000010000011101010101011110110111100000000011100101000111100000011011111001111111010010001011100101000010111101111001010010111010011111010001000110101000001010111000011010011000100000000110010110110100101110100011110100010101001010000001101011100110100110101000000001110101001101001001101011111001100101010011100001011110111101101000100010010101011100000011110010010011110000001011010110111010010001001111111111100000000111010111000000111000100100111100001010110101101100110100110001111011011100100011001101110010001010000011001101000011101000000011001101001110000110110111001100010011111100010010111"))