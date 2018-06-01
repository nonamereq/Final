class Node:
    def __init__(self, item = None, nextNode=None):
        self.item = item
        self.next = nextNode

class Stack:
    def __init__(self):
        self.__first = Node()
        self.__size = 0

    def push(self, item):
        oldfirst = self.__first
        self.__first = Node(item, oldfirst)
        self.__size += 1

    def pop(self):
        item = self.__first.item
        self.__first = self.__first.next
        self.__size -= 1
        return item

    def isEmpty(self):
        return self.__size == 0

    def size(self):
        return self.__size
    
    def top(self):
        if self.__first:
            return self.__first.item
        return None

class Queue:
    def __init__(self):
        self.__first = None
        self.__last = None
        self.__size = 0

    def isEmpty(self):
        return self.__size == 0

    def size(self):
        return self.__size

    def enqueue(self, item):
        oldlast = self.__last
        self.__last = Node(item, None)
        if self.isEmpty():
            self.__first = self.__last
        else:
            oldlast.next = self.__last
        self.__size += 1

    def dequeue(self):
        item = self.__first.item
        self.__first = self.__first.next
        if self.isEmpty():
            self.__last = None
        self.__size -= 1
        return item

    def top(self):
        if self.__first:
            return self.__first.item
        return None
