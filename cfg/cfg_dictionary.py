import re
from io import StringIO
from stack import Stack

'''
Only supports if statments
'''

''' node_type 0 for root
                    1 for function
                    2 for if
                    3 for elif
                    4 for else
                    5 for while
                    6 for for
'''
class Node:
    def __init__(self, number, indentSize=0, node_type=2):
        self.setNumber(number)
        self.indent_size = indentSize
        self.visited = False
        self.type = node_type

    def setNumber(self, number):
        self.__number = number

    def getNumber(self):
        return self.__number

    def getType(self):
        if self.type == 0:
            return "root"
        elif self.type == 1:
            return "function"
        elif self.type == 2:
            return "if"
        elif self.type == 3:
            return "elif"
        elif self.type == 4:
            return "else"
        elif self.type == 5:
            return "while"
        elif self.type == 6:
            return "for"

    def __eq__(self, other):
        return self.getNumber() == other.getNumber()

class Graph:
    def __init__(self, indentSize):
        self.indent_size = indentSize
        self.dict = {}

class Parser:
    def __init__(self, file):
        self.__file = open(file, "r")
        self.__graph = Graph(0)
        self.__stack_frame = Stack()
        self.__stack_frame.push(self.__graph)
        # self.__current_class = None
        self.__current_line = 0

    def parse(self):
        for i in self.__file:
            self.__current_line += 1
            self.handleLine(i)

    def handleLine(self, i):
        block = Parser.identifyBlock(i)
        if block == 2 or block == 3 or block == 4:
            Parser.parseIf(i, self.__current_line, self.__stack_frame, self.__graph)

    @staticmethod
    def identifyBlock(line, inLoop=False):
        ''' returns 1 for function
                    2 for if
                    3 for elif
                    4 for else
                    5 for while
                    6 for for
        '''
        regexr = r'[^\S]?((def)|(if)|(elif)|(while)|(for))[\s]|(else[\s]*:)'

        match = re.search(regexr, line)
        if not match:
            return None
        elif match.group(2):
            return 1
        elif match.group(3):
            return 2
        elif match.group(4):
            return 3
        elif match.group(7):
            return 4
        elif match.group(5):
            return 5
        elif match.group(6):
            return 6
        else:
            return None

    @staticmethod
    def parseIf(line, current_line, stack_frame, graph):
        match = re.search(r'[^\S]?if[\s]', line)
        if match != None:
            pos = match.span()[0]
            Parser.getRoot(pos, stack_frame)
            thisNode = Node(current_line, pos)
            thisGraph = Graph(pos)
            thisGraph.dict[current_line] = thisNode
            (stack_frame.top()).dict[current_line] = thisGraph
            stack_frame.push(thisGraph)

        match = re.search(r'[^\S]?(else|elif)([\s]|:)', line)
        if match != None:
            pos = match.span()[0]
            Parser.getRoot(pos, stack_frame)
            thisNode = Node(current_line, pos)
            (stack_frame.top()).dict[current_line]=thisNode

    @staticmethod
    def getRoot(pos, stack_frame):
        while stack_frame.top().indent_size > pos:
            if stack_frame.size() == 1:
                break
            stack_frame.pop()

parser = Parser("test_nested.py")
parser.parse()


print()
