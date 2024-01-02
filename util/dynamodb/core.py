import os

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute


class ApiSettingModel(Model):
    """
    A DynamoDB User
    """
    class Meta:
        table_name = 'api-setting'
        region = 'ap-northeast-1'
    setting_key = UnicodeAttribute(hash_key=True)
    notion_token = UnicodeAttribute()
    github_database_id_list = UnicodeAttribute()
    parent_database_id = UnicodeAttribute()
    union_database_id = UnicodeAttribute()
    last_updated_at = UnicodeAttribute(null=True)


def get_api_setting() -> ApiSettingModel:
    return ApiSettingModel.get('github-linkage')


if __name__ == '__main__':
    ApiSettingModel.create_table(read_capacity_units=1, write_capacity_units=1)
    api_setting = ApiSettingModel(
        setting_key='github-linkage',
        notion_token=os.environ.get("NOTION_TOKEN"),
        github_database_id_list=os.environ.get("GITHUB_DATABASE_ID_LIST"),
        parent_database_id=os.environ.get("PARENT_DATABASE_ID"),
        union_database_id='',
    )
    api_setting.save()
