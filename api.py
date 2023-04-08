import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json

class PetFriends:
    """Создаем API библиотеку к веб приложению Pet Friends согласно документации"""

    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru'

    def get_api_key(self, email, password):
        """С помощью этого метода согласно документации отправляем запрос к API сервера и возвращаем статус запроса
        и результат в формате JSON с уникальным ключом зарегистрированного пользователя"""

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url+'/api/key', headers=headers)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key, filter):
        """С помощью этого метода отправляем запрос к API сервера и возвращаем статус запроса и результат в формате JSON
                со списком найденных по фильтру питомцев. Если фильтр имеет пустое значение, получаем список всех питомцев.
                Если хотим получить список собственных питомцев, указываем в значении фильтра 'my_pets'"""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+'/api/pets', headers=headers, params=filter)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        """С помощью этого метода добавляем на сервер карточку с данными нового питомца и возвращаем статус запроса
            на сервер и результат в формате JSON с данными добавленного питомца"""

        data = MultipartEncoder(
        fields={
            'name': name,
            'animal_type': animal_type,
            'age': age,
            'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
        })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url+'/api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """С помощью этого метода отправляем на сервер запрос на удаление питомца с указанным ID и возвращаем
                статус запроса и результат в формате JSON."""

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url+'/api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: int) -> json:
        """С помощью этого метода отправляем на сервер запрос об обновлении данных питомца по указанному ID и
        возвращаем статус запроса и результат в формате JSON с обновлёнными данными питомца"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = requests.put(self.base_url+'/api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet_simple(self, auth_key: json, name: str, animal_type: str,
                           age: str) -> json:
        """С помощью этого метода добавляем на сервер карточку с данными нового питомца без фотографии и возвращаем
        статус запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url+'/api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def add_pet_photo(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """С помощью этого метода добавляем на сервер фотографию питомца по указанному ID
        и возвращаем статус запроса и result в формате JSON с обновлёнными данными питомца"""

        data = MultipartEncoder(
            fields={'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')})
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + '/api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result
