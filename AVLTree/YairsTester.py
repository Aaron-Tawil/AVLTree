import AVLTree
import random
#from printree import *


#checking rotations and inserts
def test1():
    print("test1")
    T = AVLTree.AVLTree()
    T.finger_insert(3,"Homelander")
    T.finger_insert(1,"Starlight")
    T.finger_insert(2,"Black Noir")
    T.finger_insert(4,"Soldier boy")
    T.finger_insert(5,"William Butcher")
    T.finger_insert(6,"A-train")
    T.finger_insert(7,"The Peak")
    if (T.root.right.key != 6 and T.root.right.right.key != 7 and T.root.right.left.key != 6):
        print("Insert or Left rotation fail")
    T.finger_insert(9,"Tek Knight")
    T.finger_insert(8,"Web Weaver")
    if (T.root.right.right.key != 8 and T.root.right.right.right.key != 9 and T.root.right.right.left.key != 7):
        print("Insert or Left right rotation fail")
    T.finger_insert(6.5,"Frenchie")
    T.finger_insert(6.2,"Kimiko")
    T.finger_insert(6.1,"Mother's Milk")
    if (T.root.right.left.key != 6.2 and T.root.right.left.right.key != 6.5 and T.root.right.left.left.key != 6.2):
        print("Insert or right rotation fail")
    T.finger_insert(4.5,"Nadia")
    T.finger_insert(4.7,"Edgar")
    if (T.root.left.right.key != 4.7 and T.root.left.right.right.key != 5 and T.root.left.right.left.key != 4.5):
        print("Insert or right left rotation fail")
        


def test2():
    print("test2")
    T = AVLTree.AVLTree()
    T.finger_insert(3,"Nami")
    T.finger_insert(1,"Luffy")
    T.finger_insert(2,"Zoro")
    T.finger_insert(4,"Ussop")
    T.finger_insert(5,"Sanji")
    T.finger_insert(6,"Choppa")
    T.finger_insert(7,"Robin")

#testing delete and heights
def test3():
    print("test3")
    T = AVLTree.AVLTree()
    T.finger_insert(8,"Yes Man")
    T.finger_insert(3,"Joshua Graham")
    T.finger_insert(5,"Caesar")
    T.insert(19,"Boomers")
    T.insert(2,"President Kimball")
    T.insert(6,"Veronica")
    T.insert(25,"Boone")
    T.insert(4,"White Gloves")
    T.insert(20,"Benny bad boy")
    T.insert(13,"Refael")
    T.insert(11,"Nightkin")
    T.insert(18,"Brotherhood of steel")
    T.insert(17,"Hoover Dam")
    T.insert(16,"Mr house")
    if(T.root.height != 4):
        print("problem with height of the root 1")
    if(T.root.right.height != 3):
        print("problem with height of the right child 2")
    if(T.root.left.left.height != 1):
        print("problem with height of the left left child 3")
    T.delete(T.root.left)
    if(T.root.left.height != 2):
        print("problem with height of the left child after delete 1")
    T.delete(T.root.right.right.right)
    T.delete(T.root.right.right.left)
    if(T.root.right.key != 17):
        print("wrong key in right child after delete")
    if(T.root.right.left.key != 13):
        print("wrong key on right left child after delete")
    if(T.root.height != 3):
        print("problem with the root's height after 2 deletes")

#checking avl_to_array and serach
def test4():
    print("test4")
    T = AVLTree.AVLTree()

    T.finger_insert(4,"Makima")
    T.finger_insert(66,"Denji")
    T.finger_insert(23,"Pochita")
    T.finger_insert(19,"Aki")
    T.finger_insert(5,"Asa")
    T.finger_insert(53,"kobeni")
    T.finger_insert(21,"Power")
    T.finger_insert(22,"War devil")
    T.finger_insert(33,"Bomb bitch")
    """
    T.insert(4,"Makima")
    T.insert(66,"Denji")
    T.insert(23,"Pochita")
    T.insert(19,"Aki")
    T.insert(5,"Asa")
    T.insert(53,"kobeni")
    T.insert(21,"Power")
    T.insert(22,"War devil")
    T.insert(33,"Bomb bitch")
    """""
    if T.avl_to_array() != [(4, 'Makima'), (5, 'Asa'), (19, 'Aki'), (21, 'Power'), (22, 'War devil'), (23, 'Pochita'), (33, 'Bomb bitch'), (53, 'kobeni'), (66, 'Denji')]:
        print("problem with avl_to_array")
    if(T.finger_search(5)[0] != T.root.left):
        print("problem with searching the left child")
    if(T.finger_search(222)[0] != None):
        print("problem with searching non-existant child child")
    if T.finger_search(23)[0] != T.root:
        print("problem with searching the root")
    if(T.finger_search(33)[0] != T.root.right.left):
        print("problem with searching the right left child")

def test5():
    print("test5")
    lst = [(x,"STOP USING THAT TESTER ITS MINE!!!!") for x in range(0,9999)]
    random.shuffle(lst)
    T = AVLTree.AVLTree()
    for x in lst:
        T.insert(x[0],x[1])
    if(T.avl_to_array() != sorted(lst)):
        print("Something slipped away")

test1()
test2()
test3()
test4()
test5()
