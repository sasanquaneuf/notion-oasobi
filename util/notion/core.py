import json
import os
import urllib.request
from pprint import pprint
from time import sleep
from urllib.error import HTTPError

token = os.environ.get("NOTION_TOKEN")
notion_debug_mode = False


def set_token(token_):
    global token
    token = token_


def set_debug_mode(is_debug_mode):
    global notion_debug_mode
    notion_debug_mode = is_debug_mode


def notion_get(url):
    """
    Notion APIのGETリクエストを送る
    :param url:
    :return:
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2021-08-16",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(url, headers=headers, method='GET')

    try:
        with urllib.request.urlopen(req) as res:
            body = json.load(res)
        return body
    except HTTPError as ex:
        print(ex)
        print(ex.read().decode("utf-8"))
    except Exception as ex:
        print(ex)


def notion_post(url, data):
    """
    Notion APIのPOSTリクエストを送る
    :param url:
    :param data:
    :return:
    """
    if notion_debug_mode:
        pprint(data)
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2021-08-16",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(
        url, data=json.dumps(data).encode("utf-8"), headers=headers, method='POST')

    try:
        with urllib.request.urlopen(req) as res:
            body = json.load(res)
        return body
    except HTTPError as ex:
        print(ex)
        print(ex.read().decode("utf-8"))
        raise ex
    except Exception as ex:
        print(ex)
        raise ex


def notion_patch(url, data):
    """
    Notion APIのPATCHリクエストを送る
    :param url:
    :param data:
    :return:
    """
    if notion_debug_mode:
        pprint(data)
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2021-08-16",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(
        url, data=json.dumps(data).encode("utf-8"), headers=headers, method='PATCH')

    try:
        with urllib.request.urlopen(req) as res:
            body = json.load(res)
        return body
    except HTTPError as ex:
        print(ex)
        print(ex.read().decode("utf-8"))
        raise ex
    except Exception as ex:
        print(ex)
        raise ex


def read_schema(database_id):
    """
    Notionのデータベースのスキーマを取得する
    :param database_id:
    :return:
    """
    url = f"https://api.notion.com/v1/databases/{database_id}"
    return notion_get(url)


def create_database(parent_page_id, title, properties):
    """
    Notionのデータベースを作成する
    :param parent_page_id:
    :param title:
    :param properties:
    :return:
    """
    url = "https://api.notion.com/v1/databases"
    data = {
        "parent": {"database_id": parent_page_id},
        "title": [{"type": "text", "text": {"content": title}}],
        "properties": properties,
    }
    return notion_post(url, data)


def query_to_database(database_id, filter_condition=None, sorts=None, start_cursor=None, page_size=100):
    """
    Notionのデータベースをクエリする（1回だけ、次ページ等は考慮しない）
    :param database_id:
    :param filter_condition:
    :param sorts:
    :param start_cursor:
    :param page_size:
    :return:
    """
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    data = {
        "page_size": page_size,
    }
    if filter_condition:
        data['filter'] = filter_condition
    if sorts:
        data['sorts'] = sorts
    if start_cursor:
        data['start_cursor'] = start_cursor
    return notion_post(url, data)


def query_to_database_all(database_id, filter_condition=None, sorts=None, page_size=100, limit=0):
    """
    Notionのデータベースをクエリする（全ページ）
    :param database_id:
    :param filter_condition:
    :param sorts:
    :param page_size:
    :param limit:
    :return:
    """
    start_cursor = None
    result = []
    while True:
        response = query_to_database(database_id, filter_condition, sorts, start_cursor, page_size)
        result += (response['results'] or [])
        if response.get('next_cursor'):
            start_cursor = response['next_cursor']
        else:
            break
        if len(result) >= limit > 0:
            result = result[:limit]
            break
        # api rate limitが3req/secなので、0.3秒待つ
        sleep(0.3)
    return result


def create_page_without_children(parent_database_id, properties):
    """
    Notionのページを作成する
    :param parent_database_id:
    :param properties:
    :return:
    """
    url = "https://api.notion.com/v1/pages"
    data = {
        "parent": {"database_id": parent_database_id},
        "properties": properties,
    }
    return notion_post(url, data)


def update_page_without_children(database_id, properties):
    """
    Notionのページを作成する
    :param database_id:
    :param properties:
    :return:
    """
    url = f"https://api.notion.com/v1/pages/{database_id}"
    data = {
        "properties": properties,
    }
    return notion_patch(url, data)