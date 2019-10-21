'''
Отправляет команду show или config на разные устройства в параллельных потоках, а затем записывает вывод в файл.
Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* show - команда show, которую нужно отправить (по умолчанию, значение None)
* config - команды конфигурационного режима, которые нужно отправить (по умолчанию, значение None)
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)
'''

import yaml
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from netmiko import ConnectHandler


def send_show_command(device, command):     ###Используется для комманд show
   with ConnectHandler(**device) as ssh:
       ssh.enable()
       result = ssh.find_prompt() + ssh.send_command(command, strip_command=False) + '/n'
   return(result)

def send_conf_command(device, command):     ###Используется для комманд конфигурационного режима
   with ConnectHandler(**device) as ssh:
       ssh.enable()
       result = ssh.find_prompt() + ssh.send_config_set(command, strip_command=False) + '/n'
   return(result)


def send_commands_to_devices(devices, show = None, config = None, filename = None, limit=3):
    data = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        future_ssh = []
        for device in devices:
            address = device['ip']
            if show:
                future_ssh.append(executor.submit(send_show_command, device, show))
            elif config:
                future_ssh.append(executor.submit(send_conf_command, device, config))
        for f in as_completed(future_ssh):
            result = f.result()
            data.append(result)
    with open(filename, 'w') as file:
        file.writelines(data)

if __name__ == "__main__":
    with open('devices.yaml') as f:
        devices = yaml.load(f)
    send_commands_to_devices(devices, show = 'show clock', filename = 'result.txt')