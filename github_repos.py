import argparse
from urllib.parse import urljoin

import requests
import pygal
from pygal.style import LightColorizedStyle, LightenStyle


class GitHubAPIClient:
    """Класс, для обработки запросов к API GitHub"""
    BASE_URL = 'https://api.github.com/'

    def send_request(self, url, method='GET'):
        # Формирует URL адрес.
        full_url = urljoin(self.BASE_URL, url)
        response = requests.request(url=full_url, method=method)
        print(f'Status code: {response.status_code}')
        response.raise_for_status()
        return response.json()

    def get_repos(self, language):
        return self.send_request(f'search/repositories?q=language:{language}&sort=stars')


class Chart:
    """Класс, для построения визуализации"""
    def __init__(self):
        self.pygal_style = LightenStyle('#333366', base_style=LightColorizedStyle)
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
        # Принимает обработанные данные, рисует на их основе диаграмму.
        chart_prep = pygal.Bar(self.pygal_config, style=self.pygal_style)
        chart_prep.title = title
        chart_prep.x_labels = names
        chart_prep.add('', data)
        chart_prep.render_to_file(f'{selected_language.lower()}_repos.svg')


def get_language():
    # Принимает название языка и путь для сохранения диаграмы.
    parser = argparse.ArgumentParser(description='Creating a diagram of popular projects on github.')
    parser.add_argument(
        '--language', type=str,
        choices=['Python', 'JavaScript', 'Ruby', 'C', 'Java', 'Perl', 'Haskell', 'Go'],
        required=True, help='Specify the language in which you want to get the data.'
    )

    args = parser.parse_args()
    lang = args.language
    print(f'You choose {lang} language.')
    return lang


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


if __name__ == '__main__':
    selected_language = get_language()
    github_client = GitHubAPIClient()
    repos = github_client.get_repos(selected_language)
    chart_names, chart_data = prepare_data(repos)
    chart = Chart()
    chart.render(title=f'Most-Starred {selected_language} Projects on GitHub', names=chart_names, data=chart_data)
