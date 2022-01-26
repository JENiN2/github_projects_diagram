import requests

# Создание вызова API и сохранение ответа.
url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
r = requests.get(url)
print(f'Status code: {r.status_code}')

# Сохранение ответа API в пересенной.
response_dict = r.json()

# Обработка результатов.
print('Total Repositories', response_dict['total_count'])

# Анализ информации о репозиториях.
repo_dicts = response_dict['items']
print('Repositories Returned:', len(repo_dicts))
print('\nSelected information about each repository:')
for repo_dict in repo_dicts:
    print('\nName:', repo_dict['name'])
    print('Owner:', repo_dict['owner']['login'])
    print('Stars:', repo_dict['stargazers_count'])
    print('Repository:', repo_dict['html_url'])
    print('Description:', repo_dict['description'])
