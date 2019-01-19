from daos import dog_dao


class TestGetDogByName:
    def test_get_dog_name_happy_path(self):
        result = dog_dao.get_dog_by_name('french bulldog')
        assert result['name'].lower() == 'french bulldog'
