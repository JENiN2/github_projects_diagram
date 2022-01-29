import argparse
import pathlib
from urllib.parse import urljoin

import requests
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS


class GitHubAPIClient:
    BASE_URL = 'https://api.github.com/'

    def send_request(self, url, method='GET'):
        full_url = urljoin(self.BASE_URL, url)
        response = requests.request(url=full_url, method=method)
        response.raise_for_status()
        return response.json()

    def get_repos(self, language):
        return self.send_request(f'search/repositories?q=language:{language}&sort=stars')


class Chart:
    def __init__(self):
        # Построение визуализации.
        self.pygal_style = LS('#333366', base_style=LCS)
        self.pygal_config = pygal.Config(
            x_label_rotation=45,
            show_legend=False,
            title_font_size=24,
            label_font_size=14,
            major_label_font_size=18,
            truncate_label=15,
            show_y_guides=False,
            width=1000
        )

    def render(self, title, names, data):
        chart = pygal.Bar(self.pygal_config, style=self.pygal_style)
        # chart.title =
        chart.title = title
        chart.x_labels = names
        chart.add('', data)
        chart.render_to_file(f'{language.lower()}_repos.svg')


def prepare_data(data):
    # Обрабатывает данные для отрисвки.
    repo_dicts = data.get('items')
    print("Repositories returned:", len(repo_dicts))
    names, plot_dicts = [], []
    for repo_dict in repo_dicts:
        names.append(repo_dict['name'])
        plot_dict = {
            'value': repo_dict['stargazers_count'],
            'label': repo_dict['description'],
            'xlink': repo_dict['html_url']
        }
        plot_dicts.append(plot_dict)
    return names, plot_dicts


parser = argparse.ArgumentParser(description='Creating a diagram of popular projects on github.')
parser.add_argument(
    '--language', type=str,
    choices=['Python', 'JavaScript', 'Ruby', 'C', 'Java', 'Perl', 'Haskell', 'Go'],
    required=True, help='Specify the language in which you want to get the data.'
)

parser.add_argument(
    '--output', type=pathlib.Path, default='.',
    help='Where to create an svg chart'
)

args = parser.parse_args()
language = args.language
print(f'You choose {language} language.')
print(f'Dir for SVG chart: {args.output}')

github_client = GitHubAPIClient()
repos = github_client.get_repos(language)
chart_names, chart_data = prepare_data(repos)
chart = Chart()
chart.render(title=f'Most-Starred {language} Projects on GitHub', names=chart_names, data=chart_data)
