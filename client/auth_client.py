import httplib2
import urllib3
import json
import codecs
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto import Random
# import tkinter
import tkinter           # 导入 Tkinter 库

# username = input('please input username:\n')
# passcode = input('please input passcode:\n')
# rand1 = input('please input rand1:\n')
# if not rand1:
#     rndfile = Random.new()
#     rand1 = rndfile.read(16).hex()
# print("rand1", rand1)
# h1 = SHA256.new()
# h1.update((username+passcode).encode('utf-8'))
# hash1 = h1.digest().hex()

# h2 = SHA256.new()
# h2.update((hash1+rand1).encode('utf-8'))
# hash2 = h2.digest().hex()

# data = {"username": username, "hash2": hash2, "rand1":rand1}
# encoded_data = json.dumps(data).encode('utf-8')

# http = urllib3.PoolManager()
# r = http.request('POST', 'http://127.0.0.1:3001/data', body=encoded_data, headers={'Content-Type': 'application/json'})
# ret_data = json.loads(r.data)
# print(ret_data)

#pkcs7
BS = AES.block_size
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]

# if ret_data['status'] == 'success':
#     print('----------server responds success----------')
#     iv =  ret_data['iv']
#     iv = codecs.decode(iv, 'hex_codec')
    
#     rand2_encrypted = ret_data['rand2_encrypted']
#     rand2_encrypted = codecs.decode(rand2_encrypted, 'hex_codec')
#     print('encrypted', rand2_encrypted.hex())

#     key = h1.digest().hex()[:32]
#     key = codecs.decode(key, 'hex_codec')
#     print('key', key.hex())

#     aes_cipher = AES.new(key, AES.MODE_CBC, iv)
#     plain_text = aes_cipher.decrypt(rand2_encrypted)
#     plain_text = unpad(plain_text.decode('utf-8'))
#     print('decrypted', plain_text)
#     fileHandle = open ( 'test.txt', 'w' )
#     fileHandle.write(plain_text)
# else:
#     print('authentication failed!')


class Auth(object):
    def __init__(self):
        # 生产者
        # self.q = queue.Queue()
        # self.emptyQ = threading.Event()
        # 创建主窗口,用于容纳其它组件
        self.root = tkinter.Tk()
        # 给主窗口设置标题内容
        self.root.title("Port-Scanner")

        # ip范围和端口范围，和需使用的线程数，显示结果
        self.username_prompt = tkinter.Label(self.root,compound = 'left', fg = 'red',bg = '#FF00FF',text = 'username')
        username_init = tkinter.StringVar()
        username_init.set("sky")
        self.username_input = tkinter.Entry(self.root, textvariable=username_init)

        self.passcode_prompt = tkinter.Label(self.root,compound = 'left', fg = 'red',bg = '#FF00FF',text = 'passcode')
        passcode_init = tkinter.StringVar()
        passcode_init.set("pass01")
        self.passcode_input = tkinter.Entry(self.root, textvariable=passcode_init)

        self.rand1_prompt = tkinter.Label(self.root,compound = 'left', fg = 'red',bg = '#FF00FF',text = 'rand1')
        self.rand1_input = tkinter.Entry(self.root)
        
        self.text_result = tkinter.Text(self.root)

        # 创建一个查询结果的按钮
        self.result_button = tkinter.Button(self.root, command = self.scan, text = "LogIn")

    # 完成布局
    def gui_arrang(self):
        self.username_prompt.grid(row=0,sticky=tkinter.E+tkinter.W)
        self.username_input.grid(row=0,column=1, sticky=tkinter.E+tkinter.W)
        self.passcode_prompt.grid(row=1,sticky=tkinter.E+tkinter.W)
        self.passcode_input.grid(row=1,column=1, sticky=tkinter.E+tkinter.W)
        self.rand1_prompt.grid(row=2,sticky=tkinter.E+tkinter.W)
        self.rand1_input.grid(row=2,column=1, sticky=tkinter.E+tkinter.W)
        # self.display_info.grid(columnspan=2, sticky=tkinter.E+tkinter.W+tkinter.N+tkinter.S)
        self.text_result.grid(row=3, columnspan=2, sticky=tkinter.E+tkinter.W)

        self.result_button.grid(columnspan=2)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=3)
        self.root.rowconfigure(3, weight=1)

    def scan(self):
        # self.check()
        # self.display_info.delete(0, tkinter.END);
        self.text_result.delete(0.0, tkinter.END)
        username = self.username_input.get()
        passcode = self.passcode_input.get()
        rand1 = self.rand1_input.get()
        if not rand1:
            rndfile = Random.new()
            rand1 = rndfile.read(16).hex()

        h1 = SHA256.new()
        h1.update((username+passcode).encode('utf-8'))
        hash1 = h1.digest().hex()
        print('hash1', hash1)

        h2 = SHA256.new()
        h2.update((hash1+rand1).encode('utf-8'))
        hash2 = h2.digest().hex()

        data = {"username": username, "hash2": hash2, "rand1":rand1}
        print(data)
        encoded_data = json.dumps(data).encode('utf-8')

        http = urllib3.PoolManager()
        r = http.request('POST', 'http://127.0.0.1:3001/data', body=encoded_data, headers={'Content-Type': 'application/json'})
        ret_data = json.loads(r.data)
        print(ret_data)
        self.text_result.insert(tkinter.END, str(ret_data)+'\n')
        if ret_data['status'] == 'success':
            print('----------server responds success----------')
            iv =  ret_data['iv']
            iv = codecs.decode(iv, 'hex_codec')
            
            rand2_encrypted = ret_data['rand2_encrypted']
            rand2_encrypted = codecs.decode(rand2_encrypted, 'hex_codec')
            print('encrypted:', rand2_encrypted.hex())
            self.text_result.insert(tkinter.END, 'encrypted: ' + rand2_encrypted.hex()+"\n")

            key = h1.digest().hex()
            key = codecs.decode(key, 'hex_codec')
            print('key', key.hex())
            self.text_result.insert(tkinter.END, 'key: ' + key.hex()+"\n")
            

            aes_cipher = AES.new(key, AES.MODE_CBC, iv)
            plain_text = aes_cipher.decrypt(rand2_encrypted)
            plain_text = unpad(plain_text.decode('utf-8'))
            print('decrypted', plain_text)
            self.text_result.insert(tkinter.END, 'decrypted: ' + plain_text+"\n")
            fileHandle = open ( 'test.txt', 'w' )
            fileHandle.write(plain_text+"\n")
        else:
            print('authentication failed!')
            self.text_result.insert(tkinter.END, 'authentication failed!+"\n')


def main():
    # 初始化对象
    FL = Auth()
    FL.gui_arrang()

    # 主程序执行
    FL.root.mainloop()

if __name__ == "__main__":
    main()
