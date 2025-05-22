from typing import Any, Hashable, Iterator, Optional


class MyDictIterator:
    def __init__(self, data) -> None:
        self.data = data
        self._counter = 0
    
    def __iter__(self) -> Iterator:
        return self
    
    def __next__(self):
        if self._counter >= len(self.data):
            raise StopIteration
        
        self._counter += 1
        return self.data[self._counter - 1]
        

class MyDict:
    class Entrie:
        def __init__(self, key: Hashable, value: Any) -> None:
            self.key = key
            self.value = value
        
        def __str__(self) -> str:
            key = f"{self.key}" if isinstance(self.key, (int, float)) else f"'{self.key}'"
            return f"{key}: {self.value}"
    
    def __init__(self):
        self.__data = []
        self.__size = 8
        self.__indexes = [[-1] for _ in range(self.__size)]
        self.__load_factor = 0.0

    def __set_load_factor(self) -> None:
        self.__load_factor = len(self.__data) / self.__size

    def __check_size(self) -> None:
        self.__set_load_factor()
        if self.__load_factor >= 0.75:
            self.__size *= 2
        elif self.__size > 8:
            self.__size //= 2
        self.__resize()

    def __resize(self) -> None:
        self.__set_load_factor()
        self.__indexes = [[-1] for _ in range(self.__size)]

        for data_indx in range(len(self.__data)):
            index = abs(hash(self.__data[data_indx].key)) % self.__size
            if self.__indexes[index][0] == -1:
                self.__indexes[index] = [data_indx]
            else:
                self.__indexes[index].append(data_indx)
        
    def _create_entrie(self, key: Hashable, value: Any) -> Entrie:
        return self.Entrie(key, value)
    
    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = abs(hash(key)) % self.__size

        for entrie_indx in self.__indexes[index]:
            if entrie_indx == -1:
                break
            if self.__data[entrie_indx].key == key:
                self.__data[entrie_indx].value = value
                return
        
        new_entrie = self._create_entrie(key, value)
        if self.__indexes[index][0] == -1:
            self.__indexes[index] = [len(self.__data)]
        else:
            self.__indexes[index].append(len(self.__data))
        self.__data.append(new_entrie)
        self.__check_size()
        
    def __getitem__(self, key: Hashable) -> Any:
        index = abs(hash(key)) % self.__size
        
        for entrie_indx in self.__indexes[index]:
            if entrie_indx == -1:
                break
            if self.__data[entrie_indx].key == key:
                return self.__data[entrie_indx].value
        
        raise KeyError("Ключ не найден")
    
    def __delitem__(self, key: Hashable) -> None:
        index = abs(hash(key)) % self.__size
        entitie_indexes = self.__indexes[index]
        
        for indx in entitie_indexes:
            if indx == -1:
                break
            if self.__data[indx].key == key:
                del self.__data[indx]
                del indx
                if len(entitie_indexes) < 1:
                    entitie_indexes.append(-1)
                self.__check_size()
                return
        raise KeyError("Ключ не найден")
    
    def __contains__(self, key: Hashable) -> bool:
        index = abs(hash(key)) % self.__size

        for entrie_indx in self.__indexes[index]:
            if entrie_indx == -1:
                break
            if self.__data[entrie_indx].key == key:
                return True
        return False
    
    def __len__(self) -> int:
        return len(self.__data)
    
    def __str__(self) -> str:
        data = [str(val) for val in self.__data]
        return "{" + ", ".join(data) + "}"
    
    def __iter__(self) -> Iterator:
        return MyDictIterator([entrie.key for entrie in self.__data])
    
    def get(self, key: Hashable, default: Any = None) -> Optional[Any]:
        try:
            val = self.__getitem__(key)
            return val
        except KeyError:
            return default
    
    def keys(self) -> Iterator:
        return self.__iter__()
    
    def values(self) -> Iterator:
        return MyDictIterator([entrie.value for entrie in self.__data])
    
    def items(self) -> Iterator:
        return MyDictIterator([(entrie.key, entrie.value) for entrie in self.__data])


if __name__ == "__main__":
    my_dict = MyDict()
    my_dict["1"] = 1
    my_dict["2"] = 2
    my_dict["3"] = 3
    my_dict["6"] = 6
    my_dict["6"] = 16
    my_dict["7"] = 7
    del my_dict["7"]

    print(my_dict)

    for key in my_dict.items():
        print(key)
