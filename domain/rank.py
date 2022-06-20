import json

from adapters import gateway

class RankCalCulator:
    
    @classmethod
    def get_rank_by_field(self, msg):
        rank_dict = {}
        self.field = msg["field"]
        self.__get_field_sheet(self)
        self.__get_items(self)

        for item in self.items:
            item_dict = self.__get_ranking_through_items(self, item)
            rank_dict[item] = item_dict

        result = json.dumps(rank_dict, indent = 4)

        return result

    def __get_field_sheet(self):
        self.field_object = gateway.FieldSheet(self.field)
        self.field_sheet = self.field_object.get_field_sheet()

    def __get_items(self):
        self.items = self.field_sheet["Item"].unique().tolist()

    def __get_ranking_through_items(self, item):
        item_index = self.field_sheet["Item"] == item
        item_field = self.field_sheet.loc[item_index,:]
        item_field = item_field.sort_values(by=["Points Earned", "STARS Version"], ascending = [False, False])
        return item_field.to_dict('index')

"""
from domain import rank
msg = {}
msg["field"] = "en_14_participation_in_public_policy"
rank_result = rank.RankCalCulator.get_rank_by_items(msg)
"""