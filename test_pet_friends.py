from api import PetFriends
from settings import valid_email, valid_password
from settings import wrong_email, wrong_password
import os
pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверка запроса api-ключа валидными данными. """
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
    # Проверяем, что запрос возвращает статус 200, в результате содержится слово key.

def test_get_api_key_for_nonexistent_user(email=wrong_email, password=wrong_password):
    """ Проверка запроса api-ключа невалидными данными:
        пароль и е-майл незарегистрированного пользователя """
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'This user wasn&#x27;t found in database' in result
    # Проверяем, что запрос возвращает статус 403 и выводит сообщение, что такой пользователь не найден.

def test_get_api_key_for_nonexistent_user_wrong_password(email=valid_email, password=wrong_password):
    """ Проверка запроса api-ключа невалидными данными: неверный пароль """
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'This user wasn&#x27;t found in database' in result
    # Проверяем, что запрос возвращает статус 403 и выводит сообщение, что такой пользователь не найден.

def test_get_api_key_for_nonexistent_user_wrong_email(email=wrong_email, password=valid_password):
    """ Проверка запроса api-ключа невалидными данными: неверный email """
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'This user wasn&#x27;t found in database' in result
    # Проверяем, что запрос возвращает статус 403 и выводит сообщение, что такой пользователь не найден.

def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем, что запрос на получение списка питомцев возвращает непустой список. """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Получаем api-key c валидными данными, записываем ключ в переменную auth_key
    status, result = pf.get_list_of_pets(auth_key, filter)
    # С помощью переменной auth_key отправляем запрос на получение списка
    assert status == 200
    assert len(result['pets']) > 0
    # Проверяем, что запрос возвращает статус 200 и непустой список

def test_get_all_pets_with_wrong_key(filter=''):
    """ Проверка получения списка питомцев с данными незарегистрированного пользователя"""
    _, auth_key = pf.get_api_key(wrong_email, wrong_password)
    # Получаем api-key с данными незарегистрированного пользователя, записываем ключ в переменную auth_key.
    status, result = pf.get_list_of_pets(auth_key, filter)
    # С помощью переменной auth_key пробуем получить список всех питомцев
    assert status == 403
    assert 'This user wasn&#x27;t found in database' in result
    # Проверяем, что запрос возвращает статус 403 и выводит сообщение, что такой пользователь не найден.

def test_get_my_pets_with_valid_key(filter='my_pets'):
    """ Проверка, что запрос на получения списка всех питомцев пользователя возвращает непустой список. """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Получаем api-key c валидными данными, записываем ключ в переменную auth_key
    status, result = pf.get_list_of_pets(auth_key, filter)
    # С помощью переменной auth_key и фильтра my_pets отправляем запрос на получение списка питомцев пользователя.
    assert status == 200
    assert len(result['pets']) > 0
    # Проверяем, что запрос возвращает статус 200 и непустой список

def test_get_my_pets_with_wrong_key(filter='my_pets'):
    """ Проверка получения списка питомцев с фильтром my_pets и данными незарегистрированного пользователя. """
    _, auth_key = pf.get_api_key(wrong_email, wrong_password)
    # Получаем api-key c невалидными данными, записываем ключ в переменную auth_key
    status, result = pf.get_list_of_pets(auth_key, filter)
    # Отправляем запрос на получение списка питомцев.
    assert status == 403
    assert 'This user wasn&#x27;t found in database' in result
    # Проверяем, что запрос возвращает статус 403 и выводит сообщение, что такой пользователь не найден.

def test_add_new_pet_with_valid_data(name='Ушастый', animal_type='заяц',
                                     age='2', pet_photo='images/hare.jpg'):
    """ Проверка добавления нового питомца на сайт с валидными данными пользователя. """
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Для добавления фото с помощью библиотеки os и команды dirname определим директорию, из которой запущен тест,
    # сложим ее с адресом картинки, полученный результат сохраним в переменную pet_photo.
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name
    # Проверяем, что запрос возвращает статус 200 и имя добавленного питомца

def test_add_new_pet_with_wrong_auth_key(name='Ушастый', animal_type='заяц',
                                     age='2', pet_photo='images/hare.jpg'):
    """ Проверка добавления нового питомца на сайт с данными незарегистрированного пользователя """
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Для добавления фото с помощью библиотеки os и команды dirname определим директорию, из которой запущен тест,
    # сложим ее с адресом картинки, полученный результат сохраним в переменную pet_photo.
    _, auth_key = pf.get_api_key(wrong_email, wrong_password)
    # Получаем api-key c невалидными данными, записываем ключ в переменную auth_key
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 403
    assert 'This user wasn&#x27;t found in database' in result
    # Проверяем, что запрос возвращает статус 403 и выводит сообщение, что такой пользователь не найден.

def test_successful_delete_pet_from_database():
    """Проверка успешного удаления карточки питомца зарегистрированного пользователя"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Получаем api-key c валидными данными, записываем ключ в переменную auth_key
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Получаем список питомцев, записываем его в переменную my_pets
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Васька", "кот", "3", "images/Kot1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Если список пустой, добавляем нового питомца и снова запрашиваем список.
    pet_id = my_pets['pets'][0]['id']
    # Записываем в переменную pet_id ай-ди первого питомца из полученного списка
    status, _ = pf.delete_pet(auth_key, pet_id)
    # Отправляем запрос на удаление первого питомца
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Cнова запрашиваем список.
    assert status == 200
    assert pet_id not in my_pets.values()
    # Проверяем, что запрос возвращает статус 200 и в списке нет id удалённого питомца.

def test_successful_update_information_about_pet(name='Длинноухий', animal_type='кролик', age=3):
    """Проверка успешной замены нескольких данных питомца по указанному ай-ди"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Получаем api-key c валидными данными, записываем ключ в переменную auth_key
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Получаем список питомцев, записываем его в переменную my_pets
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
    # Если список питомцев не пустой, отправляем запрос на смену данных первого питомца в списке.
        assert status == 200
        assert result['name'] == name
    # Проверяем, что запрос возвращает статус 200 и обновленное имя питомца
    else:
         raise Exception("There is no my pets")
    # если список пустой, выводим исключение "мои питомцы отсутствуют""

def test_successful_update_only_name_of_pet(name='Серый', animal_type='кролик', age=3):
    """Проверка успешной замены только имени питомца по указанному ай-ди"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Получаем api-key c валидными данными, записываем ключ в переменную auth_key
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Получаем список питомцев, записываем его в переменную my_pets
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
    # Если список питомцев не пустой, отправляем запрос на смену имени первого питомца в списке.
        assert status == 200
        assert result['name'] == name
    # Проверяем, что запрос возвращает статус 200 и обновленное имя питомца
    else:
         raise Exception("There is no my pets")
    # если список пустой, выводим исключение "мои питомцы отсутствуют""

def test_successful_update_pet_whith_unvalid_date(name=2, animal_type=2, age="один"):
    """Проверка запроса на замену данных питомца с неверным форматом ввода данных. """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Получаем api-key c валидными данными, записываем ключ в переменную auth_key
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Получаем список питомцев, записываем его в переменную my_pets
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
    # Если список питомцев непустой, отправляем запрос на замену данных первого питомца в списке.
        assert status == 400
        assert 'that provided data is incorrect' in result
    # Проверяем, что запрос возвращает статус 400 и сообщение о неверно введенных данных.
    else:
         raise Exception("There is no my pets")
    # если список пустой, выводим исключение "мои питомцы отсутствуют""

def test_add_new_pet_simple_with_valid_data(name='Барсик', animal_type='котанчик', age='10'):
    """Проверка запроса на добавление нового питомца без фото"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_add_pet_photo_with_valid_data(pet_photo='images/kot1.jpg'):
    """Проверка добавления фото к уже имеющейся карточке питомца"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
    else:
        raise Exception("There is no my pets")
