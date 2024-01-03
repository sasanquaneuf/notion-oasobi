import argparse

from util.dynamodb.core import get_api_setting
from util.notion.core import set_token, copy_schema


def copy_some_schema(original_database_id, new_schema_title):
    api_setting = get_api_setting()
    set_token(api_setting.notion_token)
    parent_database_id = api_setting.parent_database_id
    new_schema = copy_schema(parent_database_id, original_database_id, new_schema_title)
    print(new_schema)
    print('done')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--d", help="original(=from) database id, i.e. first part of the path of the URL.", type=str)
    parser.add_argument("--t", help="new(=to) schema title", type=str)
    args = parser.parse_args()
    copy_some_schema(args.d, args.t)
