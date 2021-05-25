# -*- coding: utf-8 -*-
"""
Created on Mon May  3 21:20:30 2021

@author: benoi_000
"""
from PyQt5.QtCore import QObject , pyqtSlot, QMetaObject

from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QStandardItemModel, QStandardItem
import numpy as np
import sys

class QtTreeSimple(QTreeWidget):
    Items=[]
    def __init__(self):
        super().__init__()
        self.setHeaderHidden(True)
        self.itemActivated.connect(self.Print_selected_item)
        # self.Root=QTreeWidgetItem(["z","Colone 2"])
        # self.subItem = QTreeWidgetItem(["b","Colone 2"])
        # self.subItem2 = QTreeWidgetItem(["c","Colone 2"])
        # self.subItem3 = QTreeWidgetItem(["d","Colone 2"])
        # self.subItem4 = QTreeWidgetItem(["e","Colone 2"])
        # self.subItem5 = QTreeWidgetItem(["f","Colone 2"])
        # self.subItem2.addChild(self.subItem3)
        # self.subItem2.addChild(self.subItem4)
        # self.subItem4.addChild(self.subItem5)
        # self.Root.addChild(self.subItem)
        # self.addTopLevelItems([self.Root,self.subItem2])
        # self.addTopLevelItems
    
    def GetItem(self, Selected_Item = "self.invisibleRootItem()", list_item = []):       
        '''
        Get a list that contains all element in tree (on string by path)
        For instance 
        a
        -b
        --c
        --d
        ---e
        ---f
        will be transformed to 
        ["a//b//c","a//b//c//d//e","a//b//c//d//f"]
        Parameters
        ----------
        Selected_Item : TYPE QtTreeItem, optional
            Selected root item. The default is "self.invisibleRootItem()".
            this parameter is mostly used for the recursive function
        list_item : TYPE list, optional
            List of all child. The default is [].

        Returns
        -------
        list_item : TYPE list
            Returned list of child .

        '''
        is_Root = False
        if type(Selected_Item) == type("string"):
            Selected_Item = self.invisibleRootItem()
            is_Root = True
        child_count = Selected_Item.childCount()
        if child_count > 0 :
            for i in range(child_count):
               new_list_item = self.GetItem(Selected_Item.child(i),[])
               for i in np.arange(0,len(new_list_item)):
                   if not is_Root :
                       new_list_item[i] = "{}//{}".format(Selected_Item.text(0), new_list_item[i])
                   list_item.append(new_list_item[i])
        else: 
            list_item = [Selected_Item.text(0)]
        return list_item
    
    def add_item_check_if_section_exist(self , name , ItemTree) :
        '''
        Sub function of add_item use to check if item with name exist in ItemTree. If it does
        not exist, the item is created and added to the ItemTree

        Parameters
        ----------
        name : TYPE string 
            Name that need to be added to the tree (in column 0)
        ItemTree : TYPE QTreeItem
            Root QtreeItem that will contains an item named "name"

        Returns
        -------
        TYPE : QTreeItem
            Child QTreeItem contained in ItemTree (input). If this item was not
            present it is created by this function. Otherwise the child is returned

        '''
        child_count = ItemTree.childCount()
        for i in np.arange(0,child_count):
            if name == ItemTree.child(i).text(0):
                return ItemTree.child(i)
        # if not fond, create a new item tree and test
        subItem = QTreeWidgetItem([name])
        ItemTree.addChild(subItem)
        return subItem
    
    def add_item(self, new_item):
        '''
        Add item to the tree. it create all the required intermediate QTreeItem 

        Parameters
        ----------
        new_item : TYPE either string (tag separated by "//") or an array of string

        Returns 
        -------
        None.

        '''
        if type(new_item) == type("string"):
            new_item = new_item.split("//")
        selected_item = self.invisibleRootItem()
        for i in new_item :
            selected_item = self.add_item_check_if_section_exist(i,selected_item)
        self.expandAll()
        
    def Print_selected_item( self , SelectedItem, inte):
        outputstring = ""
        
        try :
            parent=SelectedItem.parent()
        except : 
            parent=self.invisibleRootItem()
        list_item =[]
        while parent != self.invisibleRootItem():
            list_item.append(SelectedItem.text(0))
            try :
                SelectedItem = SelectedItem.parent()
                parent = SelectedItem.parent()
            except : 
                parent =self.invisibleRootItem()
        list_item.reverse()
        outputsting=""
        for item in list_item:
            outputstring += item +"//"
        outputstring = outputstring[:-2]
        print(outputstring)
   
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    centralwidget = QtWidgets.QWidget(window)
    verticalLayoutWidget = QtWidgets.QWidget(centralwidget)
    verticalLayout = QtWidgets.QVBoxLayout(verticalLayoutWidget)
    Tree=QtTreeSimple()
    verticalLayout.addWidget(Tree)
    window.setCentralWidget(centralwidget)
    window.show()
    Tree.add_item(["a","b","c"])
    Tree.add_item(["a","b","d"])
    Tree.add_item(["z","b","c"])
    print(Tree.GetItem())
    
    # Tree.add_item(["a","b","bonjourtout lesmonde"])
    # window.close()
    sys.exit(app.exec_())
    