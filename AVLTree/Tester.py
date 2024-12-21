from AVLTree import AVLNode, AVLTree, EXTERNAL_LEAF

if __name__ == '__main__':
    # Test cases for finger_search
    def test_finger_search():
        # Create a simple AVL tree
        tree = AVLTree()

        tree.root = AVLNode(10, "root")
        root = tree.root
        left = AVLNode(5, "left", parent=root, left= EXTERNAL_LEAF, right= EXTERNAL_LEAF)
        right = AVLNode(15, "right", parent=root,left= EXTERNAL_LEAF, right= EXTERNAL_LEAF)
        root.left = left
        root.right = right

        tree.max = right

        # Test 1: Search for existing keys
        assert tree.finger_search(15) == (right, 1)  # Directly at max
        assert tree.finger_search(10) == (root, 2)  # Going up then down
        assert tree.finger_search(5) == (left, 3)  # Traversing full path


        # Test 2: Search for a non-existent key
        print(tree.finger_search(7))
        assert tree.finger_search(7) == (None, 3)  # Stops at left child

        # Test 3: Search for key in a single-node tree
        tree.root = AVLNode(20, "single", left= EXTERNAL_LEAF, right= EXTERNAL_LEAF)
        tree.max = tree.root
        assert tree.finger_search(20) == (tree.root, 1)  # Key found
        assert tree.finger_search(30) == (None, 1)  # Key not found

        print("All tests passed!")


    test_finger_search()
