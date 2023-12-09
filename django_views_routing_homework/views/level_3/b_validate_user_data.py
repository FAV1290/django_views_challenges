"""
В этом задании вам нужно реализовать вьюху, которая валидирует данные о пользователе.

- получите json из тела запроса
- проверьте, что данные удовлетворяют нужным требованиям
- если удовлетворяют, то верните ответ со статусом 200 и телом `{"is_valid": true}`
- если нет, то верните ответ со статусом 200 и телом `{"is_valid": false}`
- если в теле запроса невалидный json, вернуть bad request

Условия, которым должны удовлетворять данные:
- есть поле full_name, в нём хранится строка от 5 до 256 символов
- есть поле email, в нём хранится строка, похожая на емейл
- есть поле registered_from, в нём одно из двух значений: website или mobile_app
- поле age необязательное: может быть, а может не быть. Если есть, то в нём хранится целое число
- других полей нет

Для тестирования рекомендую использовать Postman.
Когда будете писать код, не забывайте о читаемости, поддерживаемости и модульности.
"""

from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseBadRequest
from typing import Mapping


def check_data_structure(user_data: Mapping[str, str]) -> bool:
    check_set = {'full_name', 'email', 'registered_from', 'age'}
    keys_set = set(user_data.keys())
    return keys_set <= check_set and check_set - keys_set in [set(), {'age'}]


def check_full_name(user_data: Mapping[str, str]) -> bool:
    user_full_name = user_data.get('full_name', '')
    return 5 <= len(user_full_name) <= 256


def check_email(user_data: Mapping[str, str]) -> bool:
    user_email = user_data.get('email', '')
    at_sign_check = user_email.count('@') == 1 and user_email.find('@') >= 0
    dot_check = user_email.count('.')
    return all([at_sign_check, dot_check])


def check_registered_from(user_data: Mapping[str, str]) -> bool:
    user_registered_from = user_data.get('registered_from', '')
    return user_registered_from in ['website', 'mobile_app']


def check_age(user_data: Mapping[str, str]) -> bool:
    user_age = user_data.get('age', None)
    if user_age is None:
        return len(user_data) == 3
    else:
        return user_age.isdigit()


def validate_user_data_view(request: HttpRequest) -> HttpResponse:
    user_data = request.POST
    if not check_data_structure(user_data):
        return HttpResponseBadRequest('Bad data structure found')
    is_user_data_valid = all([
        check_full_name(user_data),
        check_email(user_data),
        check_registered_from(user_data),
        check_age(user_data),
    ])
    return JsonResponse({'is_valid': is_user_data_valid})
