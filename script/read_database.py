from util.dynamodb.core import get_api_setting
from util.notion.core import query_to_database_all, set_token


def read_database():
    api_setting = get_api_setting()
    set_token(api_setting.notion_token)
    data = query_to_database_all(api_setting.union_database_id, page_size=100)
    print(data)


if __name__ == '__main__':
    read_database()
