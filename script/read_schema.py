import json
from pprint import pprint

from util.dynamodb.core import get_api_setting
from util.notion.core import set_token, read_schema


def read_database():
    api_setting = get_api_setting()
    set_token(api_setting.notion_token)
    original_database_id_list = json.loads(api_setting.github_database_id_list)
    data = read_schema(original_database_id_list[0])
    pprint(data)
    data = read_schema(api_setting.union_database_id)
    pprint(data)


if __name__ == '__main__':
    read_database()
