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
from typing import Mapping, Any
from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseBadRequest


def check_keys_structure(user_keys_set: set[str]) -> bool:
    check_keys_set = {'full_name', 'email', 'registered_from', 'age'}
    return user_keys_set <= check_keys_set and check_keys_set - user_keys_set in [set(), {'age'}]


def check_json_values_types(user_data_json: Mapping[str, Any]) -> bool:
    try:
        for key in ['full_name', 'email', 'registered_from']:
            assert isinstance(user_data_json[key], str)
        age = user_data_json.get('age')
        assert age is None or isinstance(age, int)
        return True
    except AssertionError:
        return False


def check_full_name(full_name_str: str) -> bool:
    return 5 <= len(full_name_str) <= 256


def check_email(email_str: str) -> bool:
    at_sign_check = email_str.count('@') == 1 and 1 <= email_str.find('@') < (len(email_str) - 1)
    dot_check = email_str.count('.') and 1 <= email_str.find('.') < (len(email_str) - 1)
    return all([at_sign_check, dot_check])


def check_registered_from(registered_from_str: str) -> bool:
    return registered_from_str in ['website', 'mobile_app']


def check_age(age: int) -> bool:
    return age > 0


def validate_user_data_view(request: HttpRequest) -> HttpResponse:
    try:
        user_data_json = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        user_data_json = {}

    if not check_keys_structure(set(user_data_json.keys())):
        return HttpResponseBadRequest('Bad data structure found')

    if not check_json_values_types(user_data_json):
        is_user_data_valid = False
    else:
        is_user_data_valid = all([
            check_full_name(user_data_json['full_name']),
            check_email(user_data_json['email']),
            check_registered_from(user_data_json['registered_from']),
            check_age(user_data_json.get('age', True)),
        ])
    return JsonResponse({'is_valid': is_user_data_valid})
