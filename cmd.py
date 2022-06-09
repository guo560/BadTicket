import os


def run(path, port):
    os.system(f"cd {path}")
    os.system(f"start chrome.exe --remote-debugging-port={port} --new-window http://pecg.hust.edu.cn/wescms/")


if __name__ == '__main__':
    run("C:/Program Files/Google/Chrome/Application", 9527)