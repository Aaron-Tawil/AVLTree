from AVLTree import AVLTree
from anytree import Node, RenderTree


class AVLTreePrinter:

    def __init__(self, tree=None):
        self.tree = tree if tree else AVLTree()

    def build_anytree(self, node):
        if not node:
            return None
        # Create a root node with key and height
        root = Node(f"{node.key}(h={node.height})")
        # Recursively build left and right subtrees
        if node.left:
            root.left = self.build_anytree(node.left)
            root.children += (root.left,)
        if node.right:
            root.right = self.build_anytree(node.right)
            root.children += (root.right,)
        return root

    def display_tree(self):
        root = self.build_anytree(self.tree.root)
        if not root:
            print("Tree is empty")
            return
        for pre, fill, node in RenderTree(root):
            print(f"{pre}{node.name}")

    def insert_and_display(self, keys):
        for key in keys:
            self.tree.insert(key, f"value{key}")
        self.display_tree()

    @staticmethod
    def test_join():
        # Test cases for join

        # Case 1: Both trees are non-empty
        tree1 = AVLTree()
        tree2 = AVLTree()
        for i in range(1, 11):
            tree1.insert(i, f"value{i}")
        for i in range(20, 31):
            tree2.insert(i, f"value{i}")

        print("Tree 1:")
        AVLTreePrinter(tree1).display_tree()
        print("Tree 2:")
        AVLTreePrinter(tree2).display_tree()

        # Join trees
        tree1.join(tree2, 15, "value15")
        print("Joined Tree:")
        AVLTreePrinter(tree1).display_tree()

        # Case 2: First tree is empty
        empty_tree = AVLTree()
        print("Empty Tree:")
        AVLTreePrinter(empty_tree).display_tree()
        print("Tree 1 before join:")
        AVLTreePrinter(tree1).display_tree()
        empty_tree.join(tree1, 5, "value5")
        print("Joined Tree (Empty + Tree 1):")
        AVLTreePrinter(empty_tree).display_tree()

        # Case 3: Second tree is empty
        empty_tree2 = AVLTree()
        print("Tree 2 before join:")
        AVLTreePrinter(tree2).display_tree()
        tree2.join(empty_tree2, 50, "value50")
        print("Joined Tree (Tree 2 + Empty):")
        AVLTreePrinter(tree2).display_tree()

        # Case 4: Both trees are empty
        empty_tree1 = AVLTree()
        empty_tree3 = AVLTree()
        empty_tree1.join(empty_tree3, 100, "value100")
        print("Joined Empty Trees:")
        AVLTreePrinter(empty_tree1).display_tree()

    @staticmethod
    def test_split():
        print("\nTesting split function:")

        # Case 1: Split at root of a balanced tree
        tree = AVLTree()
        keys = [10, 5, 15, 3, 7, 12, 17]
        for key in keys:
            tree.insert(key, f"value{key}")
        print("\nOriginal balanced tree:")
        AVLTreePrinter(tree).display_tree()

        node = tree.search(10)[0]
        left, right = tree.split(node)
        print("\nAfter splitting at root (10):")
        print("Left tree:")
        AVLTreePrinter(left).display_tree()
        print("Right tree:")
        AVLTreePrinter(right).display_tree()

        # Case 2: Split at leaf node
        tree = AVLTree()
        keys = [10, 5, 15, 3, 7]
        for key in keys:
            tree.insert(key, f"value{key}")
        print("\nOriginal tree:")
        AVLTreePrinter(tree).display_tree()

        node = tree.search(3)[0]
        left, right = tree.split(node)
        print("\nAfter splitting at leaf (3):")
        print("Left tree:")
        AVLTreePrinter(left).display_tree()
        print("Right tree:")
        AVLTreePrinter(right).display_tree()

        # Case 3: Split at node with only one child
        tree = AVLTree()
        keys = [10, 5, 15, 7]
        for key in keys:
            tree.insert(key, f"value{key}")
        print("\nOriginal tree:")
        AVLTreePrinter(tree).display_tree()

        node = tree.search(5)[0]
        left, right = tree.split(node)
        print("\nAfter splitting at node with one child (5):")
        print("Left tree:")
        AVLTreePrinter(left).display_tree()
        print("Right tree:")
        AVLTreePrinter(right).display_tree()

        # Case 4: Split single node tree
        tree = AVLTree()
        tree.insert(1, "value1")
        print("\nSingle node tree:")
        AVLTreePrinter(tree).display_tree()

        node = tree.search(1)[0]
        left, right = tree.split(node)
        print("\nAfter splitting single node tree:")
        print("Left tree:")
        AVLTreePrinter(left).display_tree()
        print("Right tree:")
        AVLTreePrinter(right).display_tree()

        # Case 5: Split at node in a linear tree
        tree = AVLTree()
        keys = [10, 20, 30, 40, 50]
        for key in keys:
            tree.insert(key, f"value{key}")
        print("\nLinear tree:")
        AVLTreePrinter(tree).display_tree()

        node = tree.search(30)[0]
        left, right = tree.split(node)
        print("\nAfter splitting at middle node (30):")
        print("Left tree:")
        AVLTreePrinter(left).display_tree()
        print("Right tree:")
        AVLTreePrinter(right).display_tree()


if __name__ == '__main__':
    # AVLTreePrinter.test_join()
    AVLTreePrinter.test_split()