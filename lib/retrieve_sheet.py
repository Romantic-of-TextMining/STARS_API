import os
import config
import pandas

DEFAULT_PATH = os.path.join(config.basedir, "dataset")

class FieldSheet:

    def __init__(self, param):

        self.root_path = self.__create_path_by_param(param) 
        self.field_sheet = self.__combine_all_files_by_path()
    
    def get_field_sheet(self):
        return self.field_sheet

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
                sheet = self.__add_category_col2sheet(sheet, list)
                self.field_sheet = pandas.concat([self.field_sheet, sheet], axis=0, ignore_index=True)

        return self.field_sheet

    def __add_category_col2sheet(self, sheet, cols):
        for col in cols:
            sheet[col] = col

        return sheet

    def __root2list(self, root):
        dir = root.replace(self.root_path, "")
        
        category_list = dir.split("/")
        return category_list[1:]

    """def __import_dataset():
        file_root = os.path.join(config.basedir, "test_file") 
        # Read the two excel respectively
        df0 = pandas.read_excel(os.path.join(file_root, "PublicEngagement_plat.xlsx") , header=2).iloc[3:,:7]
        df1 = pandas.read_excel(os.path.join(file_root, "PublicEngagement_bron.xlsx"), header=2).iloc[3:,:7]
    # Add the new column to record "Rating Level"
        level = []
        for _ in range(len(df0)):
        level.append('Platinum')
        for _ in range(len(df1)):
        level.append('Bronze')

        # Merge the datasets
        df = pandas.concat([df0, df1], axis=0, ignore_index=True)
        df.columns = ['School', 'Location', 'Program Type', 'Version', 'Earned Score', 'Total Score', 'Description']
        df['Rated Level'] = level
        df = df.dropna(subset=['Description', 'Rated Level'])
        return df"""

    #compose sheet by parameter
    pass

class FieldSheetRetriever:
    #retrieve singel sheet by parameter
    pass

'''
import os
import config
import pandas
DEFAULT_PATH = os.path.join(config.basedir, "dataset")
from lib import retrieve_sheet
test = retrieve_sheet.FieldSheet("en-14_participation_in_public_policy")
test.get_field_sheet()
'''