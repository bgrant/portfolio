"""
Playing with implementing data structures in python.

Done in 2007 while preparing for interviews.

:author: Robert David Grant <robert.david.grant@gmail.com>

:copyright: 
    Copyright 2011 Robert David Grant

    Licensed under the Apache License, Version 2.0 (the "License"); you
    may not use this file except in compliance with the License.  You
    may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
    implied.  See the License for the specific language governing
    permissions and limitations under the License.
"""


class Stack:
    '''Mimic a stack using a list.'''
    def __init__(self):
        self.d_data = []

    def push(self, x):
        self.d_data.append(x)

    def pop(self):
        return self.d_data.pop()

    def __repr__(self):
        return str(self.d_data)


class Queue:
    '''Mimic a queue using a list.''' 
    def __init__(self):
        self.d_data = []

    def enqueue(self,x):
        self.d_data.insert(0,x)

    def dequeue(self):
        return self.d_data.pop()

    def __repr__(self):
        return str(self.d_data)


class Tree:
    ''' Node in a tree'''
    def __init__(self,value):
        self.value = value
        self.left = None
        self.right = None

    def __repr__(self):
        return str(self.value)

def inorder_walk(root):
    '''Walk a binary tree in order'''
    if root is None:
        return
    else:
        inorder_walk(root.left)
        print root
        inorder_walk(root.right)

def preorder_walk(root):
    '''Walk a binary tree in preorder'''
    if root is None:
        return
    else:
        print root
        inorder_walk(root.left)
        inorder_walk(root.right)

def postorder_walk(root):
    '''Walk a binary tree in postorder'''
    if root is None:
        return
    else:
        inorder_walk(root.left)
        inorder_walk(root.right)
        print root

def make_lefttree(root, count):
    if count == 0:
        return
    else:
        root.left = TreeNode(count)
        make_lefttree(root.left, count-1)

def make_righttree(root, count):
    if count == 0:
        return
    else:
        root.right = TreeNode(count)
        make_righttree(root.right, count-1)


class BinaryTree(Tree):
    def __init__(self, root):
        Tree.__init__(self,root)

    def insert(self, x):
        if isinstance(x, int):
            x = BinaryTree(x)

        if x.value is None or x.value == self.value:
            return
        elif x.value < self.value:
            if self.left is None:
                self.left = x
            else:
                self.left.insert(x)
        elif x.value > self.value:
            if self.right is None:
                self.right = x
            else:
                self.right.insert(x)


class LinkedListNode():

    def __init__(self, value=None, next_node=None):
        self.value = value
        self.next_node = next_node

    def __repr__(self):
        return str(self.value)


class LinkedList():
    
    def __init__(self, head_value):
        self.head = LinkedListNode(value=head_value)
        self.tail = self.head
        self._length = 1

    def __repr__(self):
        return repr(self.to_list())

    def __len__(self):
        return self._length

    def to_list(self):
        value_list = []
        current_node = self.head
        while current_node is not None:
            value_list.append(current_node.value)
            current_node = current_node.next_node
        return value_list

    def append(self, value):
        current_node = self.tail
        current_node.next_node = LinkedListNode(value=value)
        self.tail = current_node.next_node
        self._length += 1


def test_linked_list():
    ll = LinkedList(0)
    for x in range(1,10):
        ll.append(x)
    assert(len(ll) == 10)

    node = ll.head
    for x in range(len(ll)):
        assert(node.value == x)
        node = node.next_node
            
    assert(ll.to_list() == range(10))

    ll.append('foo')
    assert(len(ll) == 11)
    assert(ll.tail.value == 'foo')

    ll.append(None)
    ll.append({'foo': 55})
    assert(len(ll) == 13)
    assert(ll.tail.value['foo'] == 55)
