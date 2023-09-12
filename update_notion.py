import requests
   

# https://www.notion.so/fd184b2175c8414d82685bcea28ea5d0?v=7ec5da1b41a5414ab5c7e19aac05940a

def add_grocery_item(grocery_item):
    # create a request to the Notion API
    r = requests.post(
        "https://api.notion.com/v1/pages",
        headers={
            "Authorization": "secret_Twz7Zkf03Vbmmeb0dp23gIyx0B5SJn5xMf7cFySekgs",
            "Notion-Version": "2021-08-16",
            "Content-Type": "application/json"
        },
        json={
            "parent": {"database_id": "fd184b2175c8414d82685bcea28ea5d0"},
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": grocery_item
                            }
                        }
                    ]
                }
            }
        }
    )

    print(r.json())

