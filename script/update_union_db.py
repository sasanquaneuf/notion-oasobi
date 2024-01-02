import json
from datetime import datetime

from util.dynamodb.core import get_api_setting
from util.notion.core import query_to_database_all, set_token, create_page_without_children, read_schema, \
    update_page_without_children


def update_union_db(api_setting, original_database_id, limit=0, skip_update=False):
    union_schema_data = read_schema(api_setting.union_database_id)
    filter_condition = {
        'and': [{
            'property': 'Last edited time',
            "date": {
                "after": api_setting.last_updated_at,
            }
        }]
    }
    rows = query_to_database_all(original_database_id, filter_condition=filter_condition, page_size=100, limit=limit)
    for row in rows:
        properties = {
            'Union Key': {
                'rich_text': [{'type': 'text', 'text': {'content': row['id']}}]
            }
        }
        for key, value in row['properties'].items():
            if key in ('id', 'Last edited time'):
                continue
            if key not in union_schema_data['properties']:
                # print(f'Union Databaseに存在しないため無視されました：{key}')
                continue
            properties[key] = value
            if 'id' in value:
                del value['id']
            if 'select' in value and value['select']:
                properties[key] = {
                    'type': 'select',
                    'select': {'name': value['select']['name']}
                }
        existed_rows = query_to_database_all(api_setting.union_database_id, filter_condition={
            'and': [{
                'property': 'Union Key',
                "rich_text": {
                    "contains": row['id'],
                }
            }]
        }, page_size=100)
        if existed_rows:
            if not skip_update:
                update_page_without_children(existed_rows[0]['id'], properties)
                print(f'updated one row: {row["id"]}')
        else:
            create_page_without_children(api_setting.union_database_id, properties)
            print(f'inserted one row: {row["id"]}')
    print(f'updated rows of {original_database_id}')


def update_union_db_all(limit=0, skip_update=False):
    api_setting = get_api_setting()
    set_token(api_setting.notion_token)
    original_database_ids = json.loads(api_setting.github_database_id_list)
    if True or not api_setting.last_updated_at:
        api_setting.last_updated_at = '2000-01-01T00:00:00Z'
    print(f'last_updated_at: {api_setting.last_updated_at}')
    now_ = datetime.now()
    for original_database_id in original_database_ids:
        update_union_db(api_setting, original_database_id, limit, skip_update)
    api_setting.last_updated_at = now_.strftime('%Y-%m-%dT%H:%M:%SZ')
    api_setting.save()
    print('done')


if __name__ == '__main__':
    update_union_db_all()
