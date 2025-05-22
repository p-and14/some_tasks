import pytest

from typing import Iterator

from main import MyDict


keys = ["1", 10, (1, 2)]
values = [1, "1", None]
items = list(zip(keys, values))

@pytest.fixture
def my_dict() -> MyDict:
    my_dict = MyDict()
    for key, value in items:
        my_dict[key] = value
    return my_dict

class TestMyDict:
    def test_set_get_item(self, my_dict):
        assert len(my_dict) == len(items)
        for item in items:
            assert my_dict[item[0]] == item[1]
        
        my_dict[10] = "15"
        assert my_dict[10] == "15"
    
    def test_get(self, my_dict):
        default = "abc"
        for key, value in items:
            assert my_dict.get(key, default="abc") == value
        assert my_dict.get("Non-existing key", default) == default
    
    def test_delitem(self, my_dict):
        del my_dict[items[0][0]]
        del my_dict[items[-1][0]]

        with pytest.raises(KeyError):
            del my_dict["abc"]
        assert len(my_dict) != len(items)
        with pytest.raises(KeyError):
            my_dict[items[0][0]]
    
    def test_contains(self, my_dict):
        for item in items:
            assert (item[0] in my_dict) is True
        assert ("abc" in my_dict) is False
    
    def test_iter(self, my_dict):
        assert isinstance(iter(my_dict), Iterator) is True

        for index, key in enumerate(my_dict):
            assert key == keys[index]
        
        for index, key in enumerate(my_dict.keys()):
            assert key == keys[index]
        
        for index, value in enumerate(my_dict.values()):
            assert value == values[index]
        
        for dict_item, list_item in zip(my_dict.items(), items):
            assert dict_item == list_item
    
    def test_size(self, my_dict):
        assert my_dict._MyDict__size == 8

        new_items = [
            ("5", 5),
            ("6", 6),
            ("7", 7),
        ]
        for key, value in new_items:
            my_dict[key] = value

        assert my_dict._MyDict__size == 16
        del my_dict[new_items[0][0]]
        assert my_dict._MyDict__size == 8
        