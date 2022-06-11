from argparse import ArgumentError
import os
import config
import json

# 3rd party
import pandas

DEFAULT_PATH = os.path.join(config.basedir, "dataset")

class FieldSheet:

    def __init__(self, param):
        self.root_path = self.__create_path_by_param(param) 

    def get_field_sheet(self):
        self.field_sheet = self.__combine_all_files_by_path()
        return self.field_sheet

    def get_items_from_field(self):
        self.dict_for_items = {
            'Rated Level': {}
        }
        for (root,dirs,files) in os.walk(self.root_path, topdown=True):
            list = self.__root2list(root)
            files.remove('.DS_Store')
            for idx, file in enumerate(files):
                level = list[0]
                if idx == 0:
                    self.dict_for_items['Rated Level'][level] = {}
                filename = file.replace(".xlsx", "")
                self.dict_for_items['Rated Level'][level][filename] = {}

                sheet_path = os.path.join(root, file)
                sheet = pandas.read_excel(sheet_path, header=2).iloc[3:,:7]

                sheet.columns.values[6] = "Description"
                sheet = sheet.dropna(subset=['Description'])

                description = sheet.loc[:,"Description"].tolist()
                self.dict_for_items['Rated Level'][level][filename]['Description'] = description
        return self.dict_for_items


    def __create_path_by_param(self, param, path = DEFAULT_PATH):
        result_path = os.path.join(path, param)

        return result_path

    def __combine_all_files_by_path(self):

        self.field_sheet = pandas.DataFrame()

        for (root,dirs,files) in os.walk(self.root_path, topdown=True):
            list = self.__root2list(root)
            files.remove('.DS_Store')
            for file in files:
                sheet_path = os.path.join(root, file)
                sheet = pandas.read_excel(sheet_path, header=2).iloc[3:,:7]
                sheet.columns.values[6] = "Description"
                sheet = self.__add_category_col2sheet(sheet, list)
                sheet['Item'] = file.replace(".xlsx", "")
                self.field_sheet = pandas.concat([self.field_sheet, sheet], axis=0, ignore_index=True)

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
test = gateway.FieldSheet("en-14_participation_in_public_policy")
test.get_items_from_field()

test.get_field_sheet()
'''