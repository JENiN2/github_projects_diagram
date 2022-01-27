import operator

import requests
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

# Создание вызова API и сохранение ответа.
url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)
print('Status code:', r.status_code)

# Обработка информации о каждой строке.
submission_ids = r.json()
submission_dicts, names = [], []
for submission_id in submission_ids[:30]:
    # Создание отдельного вызова API для каждой статьи.
    url = f'https://hacker-news.firebaseio.com/v0/item/{str(submission_id)}.json'
    submission_r = requests.get(url)
    print(submission_r.status_code)
    response_dict = submission_r.json()
    names.append(response_dict['by'])
    submission_dict = {
        'value': response_dict.get('descendants', 0),
        'label': response_dict['title'],
        'xlink': response_dict['url']
    }
    submission_dicts.append(submission_dict)
submission_dicts.sort(key=operator.itemgetter('value'), reverse=True)

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
chart.title = 'The Most Active Discussions on Hacker News'
chart.x_labels = names
chart.add('', submission_dicts)
chart.render_to_file('hn_submissions.svg')
