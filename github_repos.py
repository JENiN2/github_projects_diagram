import requests
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

# Выбор языка программирования.
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

language = input('Enter the programming language number: ')

if language == '1':
    language = 'Python'
elif language == '2':
    language = 'JavaScript'
elif language == '3':
    language = 'Ruby'
elif language == '4':
    language = 'C'
elif language == '5':
    language = 'Java'
elif language == '6':
    language = 'Perl'
elif language == '7':
    language = 'Haskell'
elif language == '8':
    language = 'Go'

# Создание вызова API и сохранение ответа.
url = f'https://api.github.com/search/repositories?q=language:{language}&sort=stars'
r = requests.get(url)
print(f'Status code: {r.status_code}')

# Сохранение ответа API в пересенной.
response_dict = r.json()

# Обработка результатов.
print('Total Repositories', response_dict['total_count'])

# Анализ информации о репозиториях.
repo_dicts = response_dict['items']
names, plot_dicts = [], []
for repo_dict in repo_dicts:
    names.append(repo_dict['name'])
    plot_dict = {
        'value': repo_dict['stargazers_count'],
        'label': repo_dict['description'],
        'xlink': repo_dict['html_url']
    }
    plot_dicts.append(plot_dict)

# Построение визуализации.
my_style = LS('#333366', base_style=LCS)
my_config = pygal.Config()
my_config.x_label_rotation = 45
my_config.show_legend = False
my_config.title_font_size = 24
my_config.label_font_size = 14
my_config.major_label_font_size = 18
my_config.truncate_label = 15
my_config.show_y_guides = False
my_config.width = 1000

chart = pygal.Bar(my_config, style=my_style)
chart.title = f'Most-Starred {language} Projects on GitHub'
chart.x_labels = names
chart.add('', plot_dicts)
chart.render_to_file(f'{language}_repos.svg')
