import paramiko
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox

global cli,sshcmdline, cmd, sshcmd, channel,output


def ssh_login():
    global cli,channel
    #ssh서버에 접속하기(로그인) 위한 함수
    try:
        # paramiko에서 SSHClient 객체를 cli에 생성
        cli = paramiko.SSHClient()
        cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        print(IP.get(), Port.get(), ID.get(), PW.get())
        cli.connect(IP.get(), port=Port.get(), username=ID.get(), password=PW.get())
        channel = cli.invoke_shell()
        print("ssh connect")
        ssh_cmdwin()

    except Exception as err:
        print(err)


def ssh_command():
    global sshcmdline, cmd, sshcmd, channel,output

    sshcmds = cmd.get() + "\n"
    # 명령 송신
    channel.send(sshcmds)
    time.sleep(0.5)
    # 결과 수신
    ssh_print()

def ssh_print():
    global output,sshcmdline, cmd, sshcmd, channel
    output = channel.recv(65535).decode("utf-8")
    sshcmdline.insert('end', output)
    sshcmd.delete("0", "end")
    sshcmdline.see('end')
    print(output)

def ssh_cmdwin():
    global cmd, sshcmdline, sshcmd

    ssh = tk.Toplevel(win)
    ssh.geometry("540x400")

    # 스크롤바
    scroll = tk.Scrollbar(ssh)
    scroll.pack(side='right', fill='y')

    sshcmdline = tk.Text(ssh, height=29, yscrollcommand=scroll.set)
    sshcmdline.pack()

    scroll["command"] = sshcmdline.yview

    cmd = tk.StringVar()
    sshcmd = ttk.Entry(ssh, textvariable=cmd)
    sshcmd.pack(side='bottom', fill='x')
    sshcmd.bind("<Return>", lambda event: ssh_command())
    ssh_print()

def files_upload():
    #파일을 선택하고 ssh서버에 업로드하는 함수
    global cli, ID
    
    trans = str.maketrans('/', '\\')
    dirt = tk.Tk()
    dirt.withdraw()
    file_path = filedialog.askopenfilename(parent=dirt,
                                           initialdir="/",
                                           title='Please select a directory')
    local_path = file_path.translate(trans)
    alist = list(file_path.split('/'))
    file_name = alist[-1]

    try:
        files = cli.open_sftp()
        files.put(local_path, "/home/" + ID.get() + "/" + file_name)
    except Exception as err:
        print(err)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        try:
            cli.close()
        except:
            pass
        win.destroy()

win = tk.Tk()
ssh_frame = ttk.LabelFrame(win, text='SSH Server')
ssh_frame.grid(row=0, column=0, padx=8, pady=4)

ttk.Label(ssh_frame, text="IP :").grid(row=1, column=0, sticky=tk.W)

IP = tk.StringVar()
IP_entry = ttk.Entry(ssh_frame, textvariable=IP)
IP_entry.grid(row=1, column=1, columnspan=2, sticky=tk.W)

ttk.Label(ssh_frame, text="Port :").grid(row=2, column=0, sticky=tk.W)

Port = tk.StringVar()
Port_entry = ttk.Entry(ssh_frame, textvariable=Port)
Port_entry.grid(row=2, column=2, sticky=tk.W)

user_frame = ttk.LabelFrame(win, text='User ID/PW')
user_frame.grid(row=3, column=0, padx=8, pady=4)

ttk.Label(user_frame, text="ID :").grid(row=4, column=0, sticky=tk.W)

ID = tk.StringVar()
ID_entry = ttk.Entry(user_frame, textvariable=ID)
ID_entry.grid(row=4, column=1, columnspan=2, sticky=tk.W)

ttk.Label(user_frame, text="PW :").grid(row=5, column=0, sticky=tk.W)

PW = tk.StringVar()
PW_entry = ttk.Entry(user_frame, textvariable=PW,show='*')
PW_entry.grid(row=5, column=2, sticky=tk.W)

ttk.Button(win, text='Connect', command=ssh_login).grid(row=6, column=0, sticky=tk.E)

win.protocol("WM_DELETE_WINDOW", on_closing)
win.mainloop()

