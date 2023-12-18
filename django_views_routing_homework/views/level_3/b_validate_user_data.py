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


import json
from typing import Mapping
from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseBadRequest


def check_json_structure(user_data: Mapping[str, str]) -> bool:
    check_keys_set = {'full_name', 'email', 'registered_from', 'age'}
    user_keys_set = set(user_data.keys())
    return user_keys_set <= check_keys_set and check_keys_set - user_keys_set in [set(), {'age'}]


def check_full_name(user_data: Mapping[str, str]) -> bool:
    user_full_name = str(user_data.get('full_name', ''))
    return 5 <= len(user_full_name) <= 256


def check_email(user_data: Mapping[str, str]) -> bool:
    user_email = str(user_data.get('email', ''))
    at_sign_check = user_email.count('@') == 1 and user_email.find('@') >= 0
    dot_check = user_email.count('.')
    return all([at_sign_check, dot_check])


def check_registered_from(user_data: Mapping[str, str]) -> bool:
    user_registered_from = str(user_data.get('registered_from', ''))
    return user_registered_from in ['website', 'mobile_app']


def check_age(user_data: Mapping[str, str]) -> bool:
    user_age_raw = user_data.get('age', None)
    return True if user_age_raw is None else str(user_age_raw).isdigit()


def validate_user_data_view(request: HttpRequest) -> HttpResponse:
    try:
        user_data_json = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        user_data_json = {}
    if not check_json_structure(user_data_json):
        return HttpResponseBadRequest('Bad data structure found')
    is_user_data_valid = all([
        check_full_name(user_data_json),
        check_email(user_data_json),
        check_registered_from(user_data_json),
        check_age(user_data_json),
    ])
    return JsonResponse({'is_valid': is_user_data_valid})
