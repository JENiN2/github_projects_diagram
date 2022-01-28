import os
import requests
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS
from constants import language_map

print('\nCreating a diagram of popular projects on github.\n'
      'Сhoose a programming language:\n'
      '1 - Python\n'
      '2 - JavaScript\n'
      '3 - Ruby\n'
      '4 - C\n'
      '5 - Java\n'
      '6 - Perl\n'
      '7 - Haskell\n'
      '8 - Go')

lang = int(input('Enter the programming language number: '))

try:
    language_name = language_map[lang]
    print(f'You choose {language_map[lang]}')
except KeyError:
    print('Wrong language')
    os.exit()

language = language_map[lang]


class APIResponse:
    def __init__(self):
        self.response_dict = {}
        self.names = ''
        self.plot_dicts = []

    def api_request(self):
        # Создание вызова API и сохранение ответа.
        url = f'https://api.github.com/search/repositories?q=language:{language}&sort=stars'
        r = requests.get(url)
        print(f'Status code: {r.status_code}')

        # Сохранение ответа API в переменной.
        self.response_dict = r.json()

        # Обработка результатов.
        print('Total Repositories', self.response_dict['total_count'])

    def analysis(self):
        # Анализ информации о репозиториях.
        repo_dicts = self.response_dict.get('items')
        print("Repositories returned:", len(repo_dicts))
        self.names, self.plot_dicts = [], []
        for repo_dict in repo_dicts:
            self.names.append(repo_dict['name'])
            plot_dict = {
                'value': repo_dict['stargazers_count'],
                'label': repo_dict['description'],
                'xlink': repo_dict['html_url']
            }
            self.plot_dicts.append(plot_dict)
        return self.names, self.plot_dicts


class Visual:
    def __init__(self):
        # Построение визуализации.
        self.my_style = LS('#333366', base_style=LCS)
        self.my_config = pygal.Config()
        self.my_config.x_label_rotation = 45
        self.my_config.show_legend = False
        self.my_config.title_font_size = 24
        self.my_config.label_font_size = 14
        self.my_config.major_label_font_size = 18
        self.my_config.truncate_label = 15
        self.my_config.show_y_guides = False
        self.my_config.width = 1000

    def render(self):
        chart = pygal.Bar(self.my_config, style=self.my_style)
        chart.title = f'Most-Starred {language} Projects on GitHub'
        chart.x_labels = names
        chart.add('', plot_dicts)
        chart.render_to_file(f'{language.lower()}_repos.svg')


api = APIResponse()
api.api_request()
names, plot_dicts = api.analysis()
vis = Visual()
vis.render()
