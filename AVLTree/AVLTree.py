#id1:
#name1:
#username1:
#id2:345778039
#name2:Aaron Tawil
#username2:aarondavidt


"""A class represnting a node in an AVL tree"""

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
		return search_from(self.root, key)

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
		node , edges_down = search_from(curr, key)
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
		parent, edges = self.insert_position(key)
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

		# case A: parent is not a leaf - valid AVL tree
		if parent.height == 1:
			return new_node, edges, 0
		# case B: parent is a leaf
		promotes = 0

		# rebalancing logic
		curr = parent
		bf = balance_factor(curr)# must be 1 or -1 the first time
		while bf==1 or bf==-1: # if bf==0 we are done (since curr is for sure grater than the unchanged child but bf=0 -> childs same height less than parent)
			# case 1 - promote
			promote_height(curr)
			promotes += 1
			curr = curr.parent
			bf = balance_factor(curr) # notice if curr is none bf will be 0


		# case 2 - rotate if needed once
		if bf >1 or bf<-1:
				rebalance(curr)
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
		return None, -1, -1


	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	"""
	def delete(self, node):
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
	def insert_position(self, key):
		_, edges, parent = search_from(self.root, key)
		return parent, edges




# stand-alone helper functions
def balance_factor(node):
	if not node or not node.is_real_node():
		return 0
	return node.left.height - node.right.height

def promote_height(node):
	if not node or not node.is_real_node():
		return
	node.height = 1 + max(node.left.height, node.right.height)

def rebalance(curr):


	pass


"""
search the key from node subtree. used in search and search finger and insert to reduce duplicate code

	@type node: AVLNode
	@param node: the node to start the search from
	@param key: key of item that is to be inserted to self
	@rtype: (AVLNode,int,AVLNode)
	@returns: a 3-tuple (node,edges,parent) where node is the searched node,
	edges is the number of edges on the path between the starting node and new node before rebalancing,
	parent is the parent of the searched node. used in insert
	"""
#
def search_from(node, key):
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
