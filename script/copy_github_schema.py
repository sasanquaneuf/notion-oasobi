import json

from util.dynamodb.core import get_api_setting
from util.notion.core import read_schema, create_database, set_token


def copy_github_schema():
    api_setting = get_api_setting()
    set_token(api_setting.notion_token)
    github_database_id_list = json.loads(api_setting.github_database_id_list)
    original_database_id = github_database_id_list[0]
    parent_database_id = api_setting.parent_database_id
    original_schema = read_schema(original_database_id)
    new_schema_title = 'GitHub PR Union Database'
    new_properties = {
        'Union Key': {'rich_text': {}},
    }
    for key, type_setting in original_schema['properties'].items():
        if key == 'id':
            continue
        type_ = type_setting['type']
        if type_ in ('relation', 'rollup'):
            type_ = 'rich_text'
        if type_ not in ('select', 'multi_select'):
            option = {}
        else:
            option = {'options': type_setting[type_]['options']}
        new_properties[key] = {
            type_: option
        }
    new_schema = create_database(parent_database_id, new_schema_title, new_properties)
    print(new_schema)
    print('save union_database_id...')
    api_setting.union_database_id = new_schema['id']
    api_setting.save()
    print('done')


if __name__ == '__main__':
    copy_github_schema()
