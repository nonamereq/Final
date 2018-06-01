'''
    CFG producer for python code
    requriements: 
        -   must be a python file without a error
        -   must have a compatible white space(you can't use tabs and 
            spaces at the same time)
        - can't print the content at this time
'''
import re
from io import StringIO
from stack import Stack

''' node_type 0 for root
                    1 for function
                    2 for if
                    3 for elif
                    4 for else
                    5 for while
                    6 for for
'''
class Node:
    def __init__(self, number, parent, edges=[], indentSize=0, node_type=2):
        self.setNumber(number)
        self.setParent(parent)
        self.indent_size = indentSize
        self.edges = [i for i in edges]
        self.visited = False
        self.type = node_type

    def setNumber(self, number):
        self.__number = number

    def getNumber(self):
        return self.__number

    def setParent(self, parent):
        self.__parent = parent

    def getParent(self):
        return self.__parent

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

    def __iter__(self):
        return self.edges

    def __eq__(self, other):
        return self.getNumber() == other.getNumber()

    def addEdge(self, edge):
        self.edges.append(edge)

    def isRoot(self):
        return self.__parent == None

class Graph:
    def __init__(self, root):
        self.__root = root
        self.__nodes = {root.getNumber(): root}
        self.__last = 0
        self.iter = None

    def __iter__(self):
        return iter(self.__nodes)

    def addNode(self, node, parent, indentSize=0, node_type=2):
        n = Node(node, parent, indentSize=indentSize, node_type=node_type)
        self.__nodes[n.getNumber()] = n
        self.__nodes[parent.getNumber()].addEdge(n.getNumber())
        return n

    def addEdge(self, node, to=None):
        if to == None:
           to = self.__last
        self.__nodes[to].addEdge(node)

    def dfs(self, root=None):
        pass

class Parser:
    ROOT = Node(1, None, node_type=0)
    def __init__(self, file):
        self.__file = open(file, "r")
        self.__functions = {}
        self.__graph = Graph(Parser.ROOT)
        self.__stack_frame = Stack()
        self.__stack_frame.push(Parser.ROOT)
        # self.__current_class = None
        self.__current_line = 0

    def parse(self):
        for i in self.__file:
            self.__current_line += 1
            self.handleLine(i)

    def handleLine(self, i):
        block = Parser.identifyBlock(i)
        if block == 1:
            self.parseFunction(i)
        elif block == 2 or block == 3 or block == 4:
            Parser.parseIf(i, self.__current_line, self.__stack_frame, self.__graph, Parser.ROOT)
        # elif block == 5 or block == 6:
        #     self.parseLoop(i)

    @staticmethod
    def identifyBlock(line, inLoop=False):
        ''' returns 1 for function
                    2 for if
                    3 for elif
                    4 for else
                    5 for while
                    6 for for
                    7 for break
                    8 for continue

        '''
        regexr = r'[^\S]?((def)|(if)|(elif)|(while)|(for))[\s]|(else[\s]*:)'

        match = re.search(regexr, line)
        if not match:
            pass
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
        if inLoop:
            regexr = r'[^\S]?((break)|(continue))[\s]*'
            match = re.search(regexr, line)

            if not match:
                pass
            elif match.group(2):
                return 7
            elif match.group(3):
                return 8

        return None

    @staticmethod
    def parseIf(line, lineNumber, stack_frame, graph, root):
        match = re.search(r'[^\S]?if[\s]', line)
        if match != None:
            pos = match.span()[0]
            Parser.getRoot(pos, root, stack_frame)
            thisNode = graph.addNode(lineNumber, stack_frame.top(), pos, node_type=2)
            stack_frame.push(thisNode)

        match = re.search(r'[^\S]?(else|elif)([\s]|:)', line)
        if match != None:
            pos = match.span()[0]
            Parser.getRoot(pos, root, stack_frame)
            ntype = 4
            if match.group(0) == 'elif':
                ntype = 3
            thisNode = graph.addNode(lineNumber, stack_frame.top(), pos, node_type=ntype)
            stack_frame.push(thisNode)
        return True

    @staticmethod
    def getRoot(pos, root, stack_frame):
        while stack_frame.top().indent_size > pos or (stack_frame.top().getNumber() != root.getNumber() and pos == stack_frame.top().indent_size):
                stack_frame.pop()

    @staticmethod 
    def indentSize(line):
        return len(re.search(r'(\s*)', line).group(0))

    def parseLoop(self, line):
        stack_frame = Stack()
        indent_size = Parser.indentSize(line)
        function_root = Node(self.__current_line, None)
        graph = Graph(function_root)
        stack_frame.push(function_root)

        for i in self.__file:
            self.__current_line += 1
            block = Parser.identifyBlock(i, True)
            if indent_size > Parser.indentSize(i):
                self.handleLine(i)
            elif block == 2 or block == 3 or block == 4:
                Parser.parseIf(i, self.__current_line, stack_frame, graph, function_root)
            elif block == 5 or block == 6:
                self.parseLoop(i)
            elif block == 7 or block == 8:
                pos = indent_size(line)
                graph.addNode(self.__current_line, self.__stack_frame.top(), indentSize=pos, node_type=block)



    def parseFunction(self, line):
        stack_frame = Stack()
        indent_size = Parser.indentSize(line)
        function_name = re.search(r'[^\S]?def ([a-zA-Z_][a-zA-Z0-9_]*)\(', line).group(1)
        function_root = Node(self.__current_line, None, node_type=1)
        graph = Graph(function_root)
        self.__functions[function_name] = graph
        stack_frame.push(function_root)

        for i in self.__file:
            self.__current_line += 1
            block = Parser.identifyBlock(i)
            if indent_size >= Parser.indentSize(i):
                self.handleLine(i)
            elif block == 2 or block == 3 or block == 4:
                Parser.parseIf(i, self.__current_line, stack_frame, graph, function_root)

    def printAll(self):
        self.__graph.dfs()
        for i in self.__functions:
            self.__functions[i].dfs()

parser = Parser("test_simple.py")
parser.parse()

parser.printAll()

print()
