from typing import Any, Optional, Iterator


class DoubleLinkedList:
    """Двусвязный список"""
    class Node:
        """Элемент списка"""
        def __init__(self, value: Any) -> None:
            self.value = value
            self.prev = None
            self.next = None

    def __init__(self) -> None:
        self._head = None
        self._counter = 0

    def _create_node(self, value: Any) -> Optional[Node]:
        node = self.Node(value)
        if self._head is None:
            self._head = node
            return
        return node

    def _get_first_or_last_node(self, is_first: bool = True) -> Optional[Node]:
        """Получение первого или последнего элемента"""
        attr_name = "prev" if is_first else "next"

        if self._head:
            current = self._head
            while getattr(current, attr_name, None):
                current = getattr(current, attr_name)
            return current
        return

    def _get_first_node(self) -> Optional[Node]:
        """Получение первого элемента"""
        return self._get_first_or_last_node(is_first=True)
    
    def _get_last_node(self) -> Optional[Node]:
        """Получение последнего элемента"""
        return self._get_first_or_last_node(is_first=False)

    def append(self, value: Any) -> None:
        """Добавление элемента в конец списка"""
        node = self._create_node(value)
        if not node:
            return
        
        last_node = self._get_last_node()
        node.prev = last_node
        last_node.next = node
    
    def prepend(self, value: Any) -> None:
        """Добавление элемента в начало списка"""
        node = self._create_node(value)
        if not node:
            return
        
        first_node = self._get_first_node()
        node.next = first_node
        first_node.prev = node
    
    def insert(self, index: int, value: Any) -> None:
        """Добавление элемента по индексу"""
        node = self._create_node(value)
        if not node:
            return
        
        if index < 0:
            index += len(self) + 1

        counter = 0
        prev_ = None
        current = self._get_first_node()

        while counter < index and current:
            counter += 1
            prev_ = current
            current = current.next
        
        if not prev_:
            node.next = current
            current.prev = node
        elif prev_ and current:
            node.prev = prev_
            node.next = current
            prev_.next = node
            current.prev = node
        else:
            node.prev = prev_
            prev_.next = node
        
    def delete(self, value: Any) -> None:
        """Удаление элемента по значению"""
        current = self._get_first_node()
        if not current:
            return

        while current:
            if current.value != value:
                current = current.next
                continue
            
            if not current.next and not current.prev:
                self._head = None
                break

            if current.prev:
                current.prev.next = current.next
            if current.next:
                current.next.prev = current.prev
            
            break
    
    def find(self, value: Any) -> int:
        """
        Поиск элемента по значению. Возвращает индекс
        """
        index = 0
        current = self._get_first_node()
        if not current:
            return -1

        while current:
            if current.value != value:
                index += 1
                current = current.next
                continue

            return index
        return -1
    
    def __len__(self) -> int:
        """Возвращает длину списка"""
        len_ = 0
        current = self._get_first_node()
        if not current:
            return len_
        
        while current:
            len_ += 1
            current = current.next
        return len_
    
    def __iter__(self) -> Iterator:
        """Возвращает итератор"""
        self._counter = 0
        return self
    
    def __next__(self):
        """Возвращает следующий элемент"""
        index = 0
        value = self._get_first_node()
        
        while index < self._counter and value:
            index += 1
            value = value.next
        
        if value:
            self._counter += 1
            return value
        
        raise StopIteration


if __name__ == "__main__":
    double_ll = DoubleLinkedList()
    double_ll.append(10)
    double_ll.prepend(0)
    double_ll.insert(-2, -10)
    double_ll.delete(10)
    print("index:", double_ll.find(-10))
    print("len:", len(double_ll))

    for node in double_ll:
        print(node.value)
