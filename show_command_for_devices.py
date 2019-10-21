# -*- coding: utf-8 -*-
'''
 подключается по SSH к одному устройству и выполняет указанную команду.
* device - словарь с параметрами подключения к устройству
* command - команда, которую надо выполнить

Возвращает строку с выводом команды.
'''


import yaml
from netmiko import ConnectHandler


def send_show_command(device, command):
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        result = ssh.send_command(command)
    return(result)

if __name__ == '__main__':
    command = 'sh ip int br'
    with open('devices.yaml') as f:     #Параметры подключения к устройствам находятся в файле devices.yaml(несколько устройств)
        devices_dict = yaml.safe_load(f)
    for element in devices_dict:    # Так как устройств несколько, то применяется цикл for, который поочередно на каждом устройства выполняет функцию send_show_command
        show_command = send_show_command(element, command)
        print(show_command)