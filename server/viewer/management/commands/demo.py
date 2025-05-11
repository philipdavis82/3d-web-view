from __future__ import annotations

import os,sys
import glob,pickle

from typing_extensions import Generator,Callable,Optional

from django.core.management.base import BaseCommand, CommandError
import viewer.models as view



FILEDIR = os.path.dirname(os.path.abspath(__file__))
DATADIR  = os.path.join(FILEDIR,"data")
DATAPATH = os.path.join(FILEDIR,"data","stl_graph.pickle")

class FileObject():
    path:str

    def __init__(self,path:str):
        self.path = os.path.abspath(path)
    
    def ext(self) -> str:
        return self.path.split(".")[-1].lower()
    
    def name(self) -> str:
        return os.path.basename(self.path)

    def exists(self) -> bool:
        return os.path.exists(self.path)
    
    def isDir(self) -> bool:
        return os.path.isdir(self.path)

    def isFile(self) -> bool:
        return os.path.isfile(self.path)

    def dirs(self) -> Generator[FileObject] :
        for file in glob.glob(os.path.join(self.path,"*")):
            fo = FileObject(file)
            if(fo.isDir()): yield fo
    
    def files(self) -> Generator[FileObject] :
        for file in glob.glob(os.path.join(self.path,"*")):
            fo = FileObject(file)
            if(fo.isFile()): yield fo

class Item():
    parent:ItemGraph
    file:FileObject
    def __init__(self,file:FileObject,parent:ItemGraph):
        self.parent = parent
        self.file   = file

class ItemGraph():  
    file:FileObject
    parent:ItemGraph
    children:list[ItemGraph]
    items:list[Item]
    def __init__(self,file:FileObject,parent:Optional[ItemGraph] = None):
        self.file     = file
        self.parent   = parent
        self.children = []
        self.items    = []
    
    def addItem(self,item:Item):
        self.items.append(item)
    
    def addChild(self,child:ItemGraph):
        self.children.append(child)

    def str(self,lines:list[str]=None,tab:str="") -> str:
        output = lambda lines: None 
        if lines is None: 
            lines = []
            lines.append(tab+self.file.name())
            output = lambda lines: "\n".join(lines)

        for i,item in enumerate(self.items):
            lines.append(tab)
            if(i == len(self.items)-1 and len(self.children) == 0): 
                lines[-1] += "└── " + item.file.name()
            else:                       
                lines[-1] += "├── " + item.file.name()
        for i,child in enumerate(self.children):
            lines.append(tab)
            if i == len(self.children) - 1:
                lines[-1] += "├── " + child.file.name()
            else:
                lines[-1] += "├── " + child.file.name()
            child.str(lines,tab+"│   ")
        
        return output(lines)

import __main__
__main__.ItemGraph = ItemGraph
__main__.Item = Item
__main__.FileObject = FileObject
        

def recurssive_search(cdir:FileObject, check:Callable[[FileObject],bool], graph:ItemGraph) -> bool:
    found = False
    for file in cdir.files():
        # print(file.path)
        if(check(file)):
            graph.addItem(Item(file,graph))
            found = True
        else:
            print(file.path)

    for dir in cdir.dirs():
        next_graph = ItemGraph(dir,graph)
        next_found = recurssive_search(dir,check,next_graph)
        if(next_found):
            graph.addChild(next_graph)
            found = True
    
    return found

def main_search(root):
    # if(len(sys.argv) <= 1):
        # print("python collect-stls.py [root path]")
        # exit(-1)
    # root = sys.argv[1]
    print(f"Search Root: {root}")
    root_obj   = FileObject(root)
    root_graph = ItemGraph(root_obj)
    recurssive_search(
        root_obj,
        lambda file: file.ext()=="stl",
        root_graph
    ) 
    print(root_graph.str())
    os.makedirs(DATADIR,exist_ok=True)
    with open(DATAPATH,"wb") as file:
        pickle.dump(root_graph,file)

def main_load() -> ItemGraph:
    print(DATAPATH)
    with open(DATAPATH,"rb") as file:
        root_graph = pickle.load(file)
    return root_graph
    # print(root_graph.str())


def recurssive_filter(graph:ItemGraph,parent:view.DIRECTORY) -> None:
    for item in graph.items:
        stl = view.STL.objects.get_or_create(
            dir  = parent,
            path = item.file.path,
            name = item.file.name())[0]
        stl.dirid = parent.id
        print("  --  Item: ",item.file.name(),"dirid: ",parent.id)
        stl.save()
    
    for child in graph.children:
        print("Item: ",child.file.path)
        dir = view.DIRECTORY.objects.get_or_create(
            dir  = parent,
            path = child.file.path,
            name = child.file.name())[0]
        dir.dirid = parent.id
        print("  --  Directory: ",child.file.name(),"dirid: ",parent.id)
        dir.save()
        recurssive_filter(child,dir) 


class Command(BaseCommand):
    help = "Populates database"
    def handle(self, *args, **kwargs):
        if not os.path.exists(DATAPATH):
            print(f"Search Root: ./demofiles")
            main_search("./demofiles")
        print("Loading Graph Into Database")
        graph = main_load()
        root_entry = view.DIRECTORY.objects.get_or_create(
            path = graph.file.path,
            name = graph.file.name())[0]
        # root_entry.path = graph.file.path
        # root_entry.name = graph.file.name()
        root_entry.dirid = 0
        root_entry.save()
        recurssive_filter(graph,root_entry)
        # print("Done")
        
        

# if __name__ == "__main__" : 
#     main_search()
#     # main_load()

    
        
