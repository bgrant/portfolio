#!/usr/bin/env python
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

class TreeNode:
    def __init__(self, parent=None, left=None, right=None, value=0):
        self.parent = parent
        self.left = left
        self.right = right
        self.value = value

class BST:
    def __init__(self, root):
        self.root = root 

    def insert(self, node = None, subroot = None ):

        if subroot == None:
            subroot = self.root

        if (node == None) or (node.value == subroot.value): 
            return

        elif node.value < subroot.value:  # goes in left subtree
            if subroot.left != None:      # not at a leaf yet
                self.insert(node, subroot.left)
            else:                         # we're at a leaf, so insert  
                subroot.left = node
                node.parent = subroot
                return

        elif node.value > subroot.value:  # goes in right subtree
            if subroot.right != None:     # not at a leaf yet
                self.insert(node, subroot.right)
            else:                         # we're at a leaf, so insert  
                subroot.right = node
                node.parent = subroot
                return

    def print_me(self, subroot = None, traversal_type = 'inorder'):
        if subroot == None:
            return
        
        if traversal_type == 'preorder':
            print subroot.value,
            self.print_me(subroot.left, traversal_type = 'preorder')
            self.print_me(subroot.right, traversal_type = 'preorder')

        elif traversal_type == 'inorder':
            self.print_me(subroot.left, traversal_type = 'inorder')
            print subroot.value,
            self.print_me(subroot.right, traversal_type = 'inorder')

        elif traversal_type == 'postorder':
            self.print_me(subroot.left, traversal_type = 'postorder')
            self.print_me(subroot.right, traversal_type = 'postorder')
            print subroot.value,

        elif traversal_type == 'nr-preorder':
            stack = []

            while 1:
                if subroot == None:
                    if stack == []:
                        return
                    else:
                        subroot = stack.pop()
                        subroot = subroot.right
                else:
                    print subroot.value,
                    stack.append(subroot)
                    subroot = subroot.left


        elif traversal_type == 'nr-inorder':
            stack = []

            while 1:
                if subroot == None:
                    if stack == []:
                        return
                    else:
                        subroot = stack.pop()
                        print subroot.value,
                        subroot = subroot.right
                else:
                    stack.append(subroot)
                    subroot = subroot.left


if __name__ == '__main__':
    root_node = TreeNode(value = 5)
    tree = BST(root_node)

    print "Root =", 
    tree.print_me(tree.root, 'inorder')
    print "\n"

    mylist = [ 5, 1, 2, 3, 9, 22, 100, 4, 8, 6, 58 ]
    #for x in range(10):
    for x in mylist:
        node = TreeNode(value = x)
        tree.insert(node)

    print 'Preorder =\t[',
    tree.print_me(tree.root, traversal_type = 'preorder')
    print ']'

    print 'NR-Preorder =\t[',
    tree.print_me(tree.root, traversal_type = 'nr-preorder')
    print ']'

    print ''

    print 'Inorder =\t[',
    tree.print_me(tree.root, traversal_type = 'inorder')
    print ']'

    print 'NR-Inorder =\t[',
    tree.print_me(tree.root, traversal_type = 'nr-inorder')
    print ']'

    print ''

    print 'Postorder =\t[',
    tree.print_me(tree.root, traversal_type = 'postorder')
    print ']'
