"""
В этом задании вам нужно научиться генерировать текст заданной длинны и возвращать его в ответе в виде файла.

- ручка должна получать длину генерируемого текста из get-параметра length;
- дальше вы должны сгенерировать случайный текст заданной длины. Это можно сделать и руками
  и с помощью сторонних библиотек, например, faker или lorem;
- дальше вы должны вернуть этот текст, но не в ответе, а в виде файла;
- если параметр length не указан или слишком большой, верните пустой ответ со статусом 403

Вот пример ручки, которая возвращает csv-файл: https://docs.djangoproject.com/en/4.2/howto/outputting-csv/
С текстовым всё похоже.

Для проверки используйте браузер: когда ручка правильно работает, при попытке зайти на неё, браузер должен
скачивать сгенерированный файл.
"""
import string
import random
from faker import Faker
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden


def generate_text_handler(length: int) -> str:
    fake = Faker('la')
    fake_text: str = fake.text(max_nb_chars=length) if length > 5 else ''

    missing_length = length - len(fake_text)
    missing_chars = random.choices((string.ascii_lowercase + ' '), k=missing_length)
    missing_chars[0], missing_chars[-1] = random.choices(string.ascii_lowercase, k=2)
    fake_text += ''.join(missing_chars)

    return fake_text


def generate_file_with_text_view(request: HttpRequest) -> HttpResponse:
    target_length_str = request.GET.get('length', '0')
    if target_length_str.isdigit() and 0 < int(target_length_str) <= 1000000:
        file_content = generate_text_handler(int(target_length_str))
        response = HttpResponse(file_content, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={"lorem.txt"}'
        return response
    else:
        return HttpResponseForbidden('length param is incorrect or missing')
