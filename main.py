import os
import sys
import subprocess
from dotenv import load_dotenv
import tkinter as tk
from tkinter import messagebox

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Load .env
dotenv_path = get_resource_path(".env")
load_dotenv(dotenv_path)
global_password = os.getenv("PASSWORD", "default_password")

CLIENT_CONF_PATH = "./client.conf"

def run_command_with_sudo(command, password):
    try:
        process = subprocess.Popen(
            f'echo {password} | sudo -S {command}',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output, error = process.communicate()
        return output.decode().strip(), error.decode().strip(), process.returncode
    except Exception as e:
        messagebox.showerror("오류", f"명령 실행 중 오류 발생:\n{e}")
        return "", str(e), 1

def connect_vpn():
    command = f"wg-quick up {CLIENT_CONF_PATH}"
    output, error, returncode = run_command_with_sudo(command, global_password)
    show_result("VPN 연결", output, error, returncode)
    update_status()

def disconnect_vpn():
    command = f"wg-quick down {CLIENT_CONF_PATH}"
    output, error, returncode = run_command_with_sudo(command, global_password)
    show_result("VPN 연결 종료", output, error, returncode)
    update_status()

def check_vpn_status():
    command = "wg show"
    output, error, returncode = run_command_with_sudo(command, global_password)
    if returncode == 0 and "interface:" in output:
        return "VPN 상태: 연결됨"
    else:
        return "VPN 상태: 연결되지 않음"

def update_status():
    status = check_vpn_status()
    status_label.config(text=status)

def show_result(title, output, error, returncode):
    if returncode == 0:
        messagebox.showinfo(title, output or "성공적으로 실행되었습니다.")
    else:
        messagebox.showerror(title, error or "오류가 발생했습니다.")

def run_gui():
    global status_label
    root = tk.Tk()
    root.title("WireGuard VPN 도구")
    root.resizable(False, False)

    # GUI 크기 및 위치
    width, height = 350, 200
    x = root.winfo_screenwidth() - width - 40
    y = 40
    root.geometry(f"{width}x{height}+{x}+{y}")

    # 프레임 구성
    frame = tk.Frame(root)
    frame.pack(pady=20, padx=20)

    # 버튼들
    connect_button = tk.Button(frame, text="VPN 연결", width=25, command=connect_vpn, bg="lightgreen")
    connect_button.pack(pady=5)

    disconnect_button = tk.Button(frame, text="VPN 연결 종료", width=25, command=disconnect_vpn, bg="tomato")
    disconnect_button.pack(pady=5)

    # 상태 표시 (가운데 정렬)
    status_label = tk.Label(
        root,
        text=check_vpn_status(),
        anchor='center',
        justify='center',
        bg='lightgrey',
        padx=10
    )
    status_label.pack(fill=tk.X, side=tk.BOTTOM, ipady=5)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
