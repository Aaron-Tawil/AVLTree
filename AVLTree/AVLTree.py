#id1:
#name1:
#username1:
#id2:345778039
#name2:Aaron Tawil
#username2:aarondavidt


"""A class represnting a node in an AVL tree"""
from os.path import join
from unittest.mock import right


class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 
	
	@type key: int
	@param key: key of your node
	@type value: string
	@param value: data of your node
	"""
	def __init__(self, key, value, left=None, right=None, parent=None):
		self.key = key
		self.value = value
		self.left = left
		self.right = right
		self.parent = parent
		self.height = 0 if key is not None else -1


	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		return self.key is not None

# Define the external leaf as singleton object (all external will point to this)
EXTERNAL_LEAF = AVLNode(key=None, value=None)


"""
A class implementing an AVL tree.
"""
class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.
	"""
	def __init__(self):
		self.root = None
		self.size = 0  # Number of real nodes in the tree
		self.max = self.root # pointer to maximum node

	"""searches for a node in the dictionary corresponding to the key (starting at the root)
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def search(self, key):
		return _search_from(self.root, key)

	"""searches for a node in the dictionary corresponding to the key, starting at the max
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node- the maximum of tree and ending node+1.
	"""
	def finger_search(self, key):
		curr = self.max_node()
		edges = 0
		# go up until key is in subtree of current node
		while curr.is_real_node() and curr.parent and (curr.parent.key >= key):
			curr = curr.parent
			edges += 1
		# go down until key is found
		node , edges_down = _search_from(curr, key)
		edges += edges_down
		return node, edges


	"""inserts a new node into the dictionary with corresponding key and value (starting at the root)

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def insert(self, key, val):
		parent, edges = self._insert_position(key)
		if parent is None:
			self.root = AVLNode(key, val, parent=None, left=EXTERNAL_LEAF, right=EXTERNAL_LEAF)
			self.size += 1
			self.max = self.root
			return self.root, edges, 0
		new_node = AVLNode(key, val, parent=parent, left=EXTERNAL_LEAF, right=EXTERNAL_LEAF)
		if key > parent.key:
			parent.right = new_node
		else:
			parent.left = new_node
		self.size += 1
		# update max if needed
		if key > self.max.key:
			self.max = new_node

		# case A: parent is not a leaf - valid AVL tree
		if parent.height == 1:
			return new_node, edges, 0
		# case B: parent is a leaf
		promotes = 0

		# TODO: check if we can avoid duplicate code, join has same logic rebalancing logic
		curr = new_node
		# case 1 - promote
		while curr.height >= curr.parent.height:
			bf = _balance_factor(curr.parent)
			# notice bf ==0 is impossible here.
			if bf in [-1, 1]:  # case 1 - only promote
				_update_height(curr.parent)
				promotes += 1
				curr = curr.parent
			else:
				curr = _rebalance(curr.parent)
				break # we break since we now in this case we finish


		# check if root has changed due to rotations. in any rotation on the root it drops maximum by 1
		if self.root.parent is not None:
			self.root = self.root.parent

		return new_node, edges, promotes


	"""inserts a new node into the dictionary with corresponding key and value, starting at the max

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def finger_insert(self, key, val):
		# TODO: implement
		return None, -1, -1


	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	"""
	def delete(self, node):
		# TODO: implement
		return


	"""joins self with item and another AVLTree

	@type tree2: AVLTree 
	@param tree2: a dictionary to be joined with self
	@type key: int 
	@param key: the key separting self and tree2
	@type val: string
	@param val: the value corresponding to key
	@pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
	or the opposite way
	"""

	def join(self, tree2, key, val):
		# determine which tree is of greater keys
		right_tree = self if self.max_node().key > key else tree2
		left_tree = self if self.max_node().key < key else tree2

		if left_tree.root.height > right_tree.root.height + 1:
			return self._join_with_bigger_subtree(
				bigger_tree=left_tree,
				smaller_tree=right_tree,
				key=key,
				val=val,
				is_left_bigger=True
			)
		if right_tree.root.height > left_tree.root.height + 1:
			return self._join_with_bigger_subtree(
				bigger_tree=right_tree,
				smaller_tree=left_tree,
				key=key,
				val=val,
				is_left_bigger=False
			)

		# if trees differ by at most 1 in height
		new_root = AVLNode(key, val, left=left_tree.root, right=right_tree.root)
		left_tree.root.parent = new_root
		right_tree.root.parent = new_root
		self.root = new_root
		self.size += tree2.size + 1
		self.max = right_tree.max
		return

	def _join_with_bigger_subtree(self, bigger_tree, smaller_tree, key, val, is_left_bigger):
		"""Helper method to join trees when one subtree is significantly bigger"""
		# go down in bigger until we find a node with height of smaller.root.height
		curr = bigger_tree.root
		while curr.height > smaller_tree.root.height:
			curr = curr.right if is_left_bigger else curr.left

		# connect and cut what's needed
		if is_left_bigger:
			x_node = AVLNode(key, val, parent=curr.parent, left=curr, right=smaller_tree.root)
			curr.parent.right = x_node
		else:
			x_node = AVLNode(key, val, parent=curr.parent, left=smaller_tree.root, right=curr)
			curr.parent.left = x_node
		curr.parent = x_node
		smaller_tree.root.parent = x_node
		_update_height(x_node)

		# rebalance from x_node to root
		curr = x_node
		# rebalancing logic
		while curr.height >= curr.parent.height :
			bf = _balance_factor(curr.parent)
			# notice bf ==0 is impossible here.
			if bf in [-1, 1]:  # case 1 - only promote
				_update_height(curr.parent)
				curr = curr.parent
			else: # case 2 - rotate
				curr = _rebalance(curr.parent)

		# check if root has changed due to rotations. in any rotation on the root it drops maximum by 1
		if bigger_tree.root.parent is not None:
			bigger_tree.root = bigger_tree.root.parent

		self.max = smaller_tree.max if is_left_bigger else bigger_tree.max
		self.root = bigger_tree.root
		self.size = bigger_tree.size + smaller_tree.size + 1
		return

	#  בפונקציה ספליטה השתמשתי בפונקציה הזו גם עבור מקרה זבו אחד מהעצים הוא ריק, אז או לטפל בזה כאן או לטפל בזה במתודה split
	"""splits the dictionary at a given node

	@type node: AVLNode
	@pre: node is in self
	@param node: the node in the dictionary to be used for the split
	@rtype: (AVLTree, AVLTree)
	@returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
	dictionary larger than node.key.
	"""

	# TODO: Update this function to calculate size,root,max dynamically for each tree
	def split(self, node):
		# Initialize the subtrees based on the given node
		larger_than_node = node.right # Subtree with nodes larger than the current node's key
		smaller_than_node = node.left # Subtree with nodes smaller than the current node's key

		# Disconnect the given node from its left and right children
		node.left = None
		node.right = None

		# Traverse upwards from the given node to update the subtrees structure
		currNode = node
		while currNode.parent is not None:
			parent = currNode.parent

			if currNode.key > parent.key:# If the current node is in the right subtree of its parent
				tempTree = parent.left
				parent.left = None
				# Join the parent's left subtree with the smaller subtree
				smaller_than_node = tempTree.join(smaller_than_node, parent.key, parent.val)
			else: # If the current node is in the left subtree of its parent
				tempTree = parent.right
				parent.right = None
				# Join the parent's right subtree with the larger subtree
				larger_than_node = larger_than_node.join(tempTree, currNode.key, currNode.val)

			# Move up to the parent node for the next iteration
			currNode = parent

		# Return the two resulting subtrees
		return larger_than_node, smaller_than_node



	"""returns an s array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):
		curr_node = self.root
		if not curr_node.left and not curr_node.right:
			return [(curr_node.key, curr_node.value)]

		left_subtree = curr_node.left.avl_to_array() if curr_node.left else []
		right_subtree = curr_node.right.avl_to_array() if curr_node.right else []

		return left_subtree + [(curr_node.key, curr_node.value)] + right_subtree

	"""returns the node with the maximal key in the dictionary

	@rtype: AVLNode
	@returns: the maximal node, None if the dictionary is empty
	"""
	def max_node(self):
		return self.max

	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self):
		return self.size


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return self.root



	# returns the parent of the node that should be the parent of the new node
	# and the number of edges on the path from root to the new node
	def _insert_position(self, key):
		_, edges, parent = _search_from(self.root, key)
		return parent, edges




# stand-alone helper functions
def _balance_factor(node):
	if not node or not node.is_real_node():
		return 0
	return node.left.height - node.right.height

def _update_height(node):
	if not node or not node.is_real_node():
		return
	node.height = 1 + max(node.left.height, node.right.height)


#cheks what rotation is needed (should handle all cases possible) and calls the appropriate function finally returns the new root of the subtree
def _rebalance(curr):
	#TODO: implement rebalance
	return curr
# rotates and returns the new root of the subtree
def _rotate_left(node):
	#TODO: implement rotate_left
	return
# rotates and returns the new root of the subtree
def _rotate_right(node):
	#TODO: implement rotate_right
	return


"""
	@returns: a 3-tuple (node,edges,parent) where node is the searched node or none if not found,
	edges is the number of edges on the path between the starting node and new node ,
	parent is the parent of the searched node. used in insert
	"""
def _search_from(node, key):
	if not node or not node.is_real_node():
		return None, 0
	curr = node
	edges = 0
	while curr.is_real_node():
		if curr.key == key:
			return curr , edges+1, curr.parent
		elif curr.key < key:
			curr = curr.right
		else:
			curr = curr.left
		edges += 1
	return None, edges, curr.parent

