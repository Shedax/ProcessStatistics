import subprocess, psutil
import datetime, time
from subprocess import Popen, PIPE
import os.path

def get_path():
    while True:
        cpath = input('Введите путь к файлу, который необходимо запустить:\n')
        if os.path.exists(cpath):
            return cpath
        else:
            print('Указан неверный путь файла.')

def get_timer():
    while True:
        timer = input('Введите интервал сбора статистики в секундах:\n')
        if timer.isdigit():
            return timer
        else:
            print('Недопустимый формат ввода времени.')

path = get_path()
timer = get_timer()
proc = Popen(
    r"" + path,
    shell=True,
    stdout=PIPE, stderr=PIPE
)
time.sleep(5)
RUN = True
PROCNAME = path.split('\\')[len(path.split('\\')) - 1]
with open(PROCNAME.split('.')[0] + "_data.txt", "r+") as f:
    text = f.read()
    if len(text) == 0:
        f.write('Загрузка CPU\t\tWorking Set\t\tPrivate Bytes\t\tHandle Count\t\tВремя')
nid = 0
while RUN:
    if nid != 0 and not psutil.pid_exists(nid):
        RUN = False
    else:
        for proc in psutil.process_iter():
            if proc.name().lower() == PROCNAME.lower():
                Data = subprocess.check_output(['wmic', 'process', 'list', 'brief'])
                data = str(Data)
                p = psutil.Process(proc.pid)
                nid = proc.pid
                for i in range(len(data)):
                    if PROCNAME.lower() in data.split("\\r\\r\\n")[i].lower():
                        handles = str(data.split("\\r\\r\\n")[i].split(' ')[0])
                        break
                now = datetime.datetime.now()
                current_time = str(now.strftime("%d-%m-%Y %H:%M:%S"))
                cpu = str(p.cpu_percent(interval=1)) + '%'
                wset = str(p.memory_info().wset / 1024)
                private_byte = str(p.memory_info().pagefile / 1024)
                with open(PROCNAME.split('.')[0] + "_data.txt", "a+") as f:
                    f.write('\n' + cpu + '\t\t\t' + wset + '\t\t\t' + private_byte + '\t\t\t' + handles + '\t\t\t' + current_time)



