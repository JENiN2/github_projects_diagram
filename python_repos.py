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

# Анализ первого репозитория.
repo_dict = repo_dicts[0]
print('\nKeys:', len(repo_dict))
for key in sorted(repo_dict.keys()):
    print(key)