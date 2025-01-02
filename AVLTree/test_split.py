from AVLTree import AVLTree


def test_split():
    def verify_split(tree, split_key):
        node = tree.search(split_key)[0]
        left, right = tree.split(node)

        def verify_left(node):
            if not node or not node.is_real_node():
                return True
            return (node.key < split_key and
                    verify_left(node.left) and
                    verify_left(node.right))

        def verify_right(node):
            if not node or not node.is_real_node():
                return True
            return (node.key > split_key and
                    verify_right(node.left) and
                    verify_right(node.right))

        def verify_avl(node):
            if not node or not node.is_real_node():
                return True, -1
            left_valid, left_height = verify_avl(node.left)
            right_valid, right_height = verify_avl(node.right)
            balance = left_height - right_height
            height = max(left_height, right_height) + 1
            return (left_valid and right_valid and
                    abs(balance) <= 1 and
                    height == node.height), height

        assert verify_left(left.root), "Left tree contains keys >= split_key"
        assert verify_right(right.root), "Right tree contains keys <= split_key"
        left_valid, _ = verify_avl(left.root)
        right_valid, _ = verify_avl(right.root)
        assert left_valid, "Left tree violates AVL properties"
        assert right_valid, "Right tree violates AVL properties"

        print(f"Split at {split_key} passed all verifications")
        return left, right

    test_cases = [
        ([1, 2, 3, 4, 5], 3),
        ([5, 3, 7, 2, 4, 6, 8], 5),
        ([10], 10),
        ([5, 3, 7, 2, 4, 6, 8, 1, 9], 2),
        ([15, 10, 20, 5, 12, 17, 25], 12),
    ]

    for keys, split_key in test_cases:
        print(f"\nTesting split with keys {keys} at {split_key}")
        tree = AVLTree()
        for k in keys:
            tree.insert(k, f"value{k}")
        try:
            left, right = verify_split(tree, split_key)
        except AssertionError as e:
            print(f"Test failed: {e}")


if __name__ == "__main__":
    test_split()