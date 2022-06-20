import os
import config

DEFAULT_PATH = os.path.join(config.basedir, "dataset")
class PathTree2DictManager:
    def __init__(self, root_path=DEFAULT_PATH):
        #create a dict base on specify root
        self.dict = {}
        for (root,dirs,files) in os.walk(root_path, topdown=True):
            self.__path2dict__(root,dirs,files) 
    
    def get_dict(self):
        return self.dict
    
    def get_path(self, filename):
        self.dict.get("")
        pass
        #reture path based on filename
    
    def __path2dict__(self, root, dirs, files):
        files.remove('.DS_Store')
        target_dict = self.__get_dict_by_dir__(root)
        for dir in dirs:
            target_dict[dir] = {}
        
        for file in files:
            target_dict[file] = None
    
    def lookup_filename(self, filename):
        pass
        #check keys
        #if not, iterate to value without NONE
        #return f"{key}/{filename}"

    def __get_dict_by_dir__(self, path):
        path = path.replace(DEFAULT_PATH, "")
        if path == "": 
            return self.dict
        
        dirs = path.split("/")
        result_dict = self.dict.get(dirs[1])

        if result_dict == {}:
            return result_dict

        for dir in dirs[2:]:
            result_dict = result_dict.get(dir)
        return result_dict

'''
import config
import os
from lib import path_tree_to_dict
test2 = path_tree_to_dict.PathTree2DictManager()
'''