'''
Параметры функции:
* template - путь к файлу с шаблоном ("templates/for.txt")
* data_dict - словарь со значениями, которые надо подставить в шаблон (data/for.yml.)
'''

import yaml
import os
import sys
from jinja2 import Environment, FileSystemLoader


def generate_config(template, data_dict):
    template_dir, template_file = os.path.split(template)
    env = Environment(loader=FileSystemLoader(template_dir),
                      trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(template_file)
    result = template.render(data_dict)
    return str(result)



if __name__ == "__main__":
    with open('data_files/for.yml') as f:
        data = yaml.safe_load(f)
    print(generate_config('templates/for.txt', data))