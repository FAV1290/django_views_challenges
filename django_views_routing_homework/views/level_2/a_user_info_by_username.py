from django.http import JsonResponse, HttpResponse, HttpRequest


"""
Вьюха get_user_info_by_username_view возвращает информацию о юзере по его юзернейму.
Если айдишника нет - возвращает собщение об ошибке

Задания:
    1. Откройте страницу http://127.0.0.1:8000/user-info-by-username/red_dev/
       Вы получаете ошибку, несмотря на то что путь есть в urls.py
       и юзер с таким юзернэймом есть в словаре USERNAME_TO_USER_INFO_MAPPER.
    2. Откройте urls.py и найдите путь, который обрабатывает вьюху get_user_info_by_username_view.
    3. Подумйте, почему Django не может открыть страницу из первого пункта и исправьте ошибку.
       Подсказка тут https://docs.djangoproject.com/en/4.2/topics/http/urls/#path-converters
"""
USERNAME_TO_USER_INFO_MAPPER = {
    'red_dev': {'id': 1, 'age': 34},
    'green_bear': {'id': '2', 'age': 43},
    'monster': {'id': '3', 'age': 17},
}


def get_user_info_by_username_view(request: HttpRequest, username: str) -> HttpResponse:
    if username in USERNAME_TO_USER_INFO_MAPPER:
        return JsonResponse(data=USERNAME_TO_USER_INFO_MAPPER[username])
    else:
        return JsonResponse(data={'error': 'There is no user info'}, status=404)
