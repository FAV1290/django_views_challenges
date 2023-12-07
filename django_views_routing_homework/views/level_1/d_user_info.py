from django.http import JsonResponse, HttpRequest, HttpResponse


"""
Вьюха get_user_info_view возвращает информацию о юзере по его айдишнику.
Если айдишника нет - возвращает собщение об ошибке

Задания:
    1. Добавьте путь в файле urls.py, чтобы при открытии http://127.0.0.1:8000/user-info/тут айдишник юзера/
       вызывалась вьюха get_user_info_view. Например http://127.0.0.1:8000/user-info/55/
    2. Проверьте созданный вами путь с существуюшим айдишником.
    3. Проверьте созданный вами путь с несуществуюшим айдишником.
"""
USER_ID_TO_USER_INFO_MAPPER = {
    1: {'username': 'red_dev', 'age': 34},
    2: {'username': 'green_bear', 'age': 43},
    3: {'username': 'monster', 'age': 17},
}


def get_user_info_view(request: HttpRequest, user_id: int) -> HttpResponse:
    if user_id in USER_ID_TO_USER_INFO_MAPPER:
        return JsonResponse(data=USER_ID_TO_USER_INFO_MAPPER[user_id])
    else:
        return JsonResponse(data={'error': 'There is no user info'}, status=404)
