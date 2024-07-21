from services import process_country_data


def test_get_proper_name():
    # Test specific mappings
    assert process_country_data._get_proper_name(
        "United Kingdom of Great Britain and Northern Ireland") == "United Kingdom"
    assert process_country_data._get_proper_name(
        "Korea, Republic of") == "South Korea"
    assert process_country_data._get_proper_name(
        "Netherlands, Kingdom of the") == "Netherlands"
    assert process_country_data._get_proper_name(
        "Russian Federation") == "Russia"
    assert process_country_data._get_proper_name(
        "Tanzania, United Republic of") == "Tanzania"
    assert process_country_data._get_proper_name("Viet Nam") == "Vietnam"
    assert process_country_data._get_proper_name(
        "Slovak Republic") == "Slovakia"
    assert process_country_data._get_proper_name("Türkiye") == "Turkey"
    assert process_country_data._get_proper_name(
        "United States of America") == "United States"

    # Test default behavior
    assert process_country_data._get_proper_name("France") == "France"
    assert process_country_data._get_proper_name("Spain") == "Spain"
    assert process_country_data._get_proper_name("Canada") == "Canada"
