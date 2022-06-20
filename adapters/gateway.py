from argparse import ArgumentError
import os
import config
import json

# 3rd party
import pandas

DEFAULT_PATH = os.path.join(config.basedir, "dataset")

class FieldSheet:

    def __init__(self, field):
        self.root_path = self.__create_path_by_param(field)

    def get_field_sheet(self):
        self.field_sheet = self.__combine_all_files_by_path()
        return self.field_sheet

    def get_items_from_field(self, item = ""):
        self.dict_for_items = {
            'Rated Level': {}
        }
        for (root,dirs,files) in os.walk(self.root_path, topdown=True):
            dir_list = self.__root2list(root)

            if dir_list == []:
                continue
            else:
                level = dir_list[0]
    
            for idx, file in enumerate(files):
                if idx == 0:
                    self.dict_for_items['Rated Level'][level] = {}

                if file == '.DS_Store': continue

                filename = file.replace(".xlsx", "")
                if (item != "" and item!=filename):
                    continue
                else:
                    self.__push_item_to_dict(root, level, file, filename)

        return self.dict_for_items

    def __push_item_to_dict(self, root, level, file, filename):
            self.dict_for_items['Rated Level'][level][filename] = {}

            sheet_path = os.path.join(root, file)
            sheet = pandas.read_excel(sheet_path, header=2).iloc[3:,:7]

            sheet.columns.values[6] = "Description"
            sheet = sheet.dropna(subset=['Description'])

            description = sheet.loc[:,"Description"].tolist()
            self.dict_for_items['Rated Level'][level][filename]['Description'] = description

    def __create_path_by_param(self, param, path = DEFAULT_PATH):
        result_path = os.path.join(path, param)

        return result_path

    def __combine_all_files_by_path(self):

        self.field_sheet = pandas.DataFrame()

        for (root,dirs,files) in os.walk(self.root_path, topdown=True):
            list = self.__root2list(root)
            
            for file in files:
                if file == '.DS_Store': continue

                sheet_path = os.path.join(root, file)
                sheet = pandas.read_excel(sheet_path, header=2).iloc[3:,:7]
                sheet = sheet.drop_duplicates()
                sheet.columns.values[6] = "Description"
                sheet = self.__add_category_col2sheet(sheet, list)
                sheet['Item'] = file.replace(".xlsx", "")
                self.field_sheet = pandas.concat([self.field_sheet, sheet], axis=0, ignore_index=True)
                print(f"self.field_sheet.columns: {self.field_sheet.columns}")

        self.field_sheet = self.field_sheet.dropna(subset=['Description'])

        return self.field_sheet

    def __add_category_col2sheet(self, sheet, cols):
        sheet['Rated Level'] = cols[0]
        return sheet

    def __root2list(self, root):
        dir = root.replace(self.root_path, "")
        
        category_list = dir.split("/")
        return category_list[1:]

    pass

class FieldSheetRetriever:
    #retrieve single sheet by parameter
    pass

'''
import os
import config
import pandas
DEFAULT_PATH = os.path.join(config.basedir, "dataset")
from adapters import gateway
test = gateway.FieldSheet("en_14_participation_in_public_policy")
result = test.get_items_from_field()
result['Rated Level']['gold']['national level'].keys()

item = test.get_items_from_field("national level")
item['Rated Level']['gold'].keys()

test.get_field_sheet()
'''