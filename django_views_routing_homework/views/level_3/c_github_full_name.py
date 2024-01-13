"""
В этом задании вам нужно реализовать ручку, которая принимает на вход ник пользователя на Github,
а возвращает полное имя этого пользователя.

- имя пользователя вы узнаёте из урла
- используя АПИ Гитхаба, получите информацию об этом пользователе
  (это можно сделать тут: https://api.github.com/users/USERNAME)
- из ответа Гитхаба извлеките имя и верните его в теле ответа: `{"name": "Ilya Lebedev"}`
- если пользователя на Гитхабе нет, верните ответ с пустым телом и статусом 404
- если пользователь на Гитхабе есть, но имя у него не указано, верните None вместо имени
"""
import requests
from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseNotFound


def fetch_github_user_info_handler(
    github_login: str,
) -> dict[str, str | int | float | bool | None] | None:
    github_response = requests.get(f'https://api.github.com/users/{github_login}')
    if github_response.ok:
        github_response_json: dict[str, str | int | float | bool | None] = github_response.json()
        return github_response_json
    else:
        return None


def fetch_name_from_github_view(request: HttpRequest, github_username: str) -> HttpResponse:
    user_info = fetch_github_user_info_handler(github_username)
    if user_info is None:
        return HttpResponseNotFound()
    elif user_info['name'] is None:  # To prevent None transformation to null (in order to satisfy line 9 condition)
        return JsonResponse({'name': 'None'})
    else:
        return JsonResponse({'name': user_info['name']})
