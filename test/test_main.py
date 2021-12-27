from main import user_json_praser


def test_single_user_data_parsed_correctly(user_data):
    single_user_data = [user_data[0]]
    assert user_json_praser(single_user_data) == [
        {"id": 1, "name": "Leanne Graham", "city": "Gwenborough"}
    ]


def test_many_user_data_parsed_correctly(user_data):
    assert user_json_praser(user_data) == [
        {"id": 1, "name": "Leanne Graham", "city": "Gwenborough"},
        {"id": 2, "name": "Ervin Howell", "city": "Wisokyburgh"}
    ]
