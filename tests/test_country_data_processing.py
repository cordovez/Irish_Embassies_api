from services import process_country_data
from mongodb.models import CountryDocument


class TestCountryData:
    # def test_country_from_json(self):
    #     mock_data = [
    #         {
    #             "type_of": "country",
    #             "name": "Country A",
    #             "is_represented": True
    #             },
    #         {
    #             "type_of": "country",
    #             "name": "Country B",
    #             "is_represented": False
    #             },
    #         {
    #             "type_of": "not_a_country",
    #             "name": "Not a Country",
    #             "is_represented": False
    #             }
    #         ]
    #
    #     # Expected output
    #     expected_output = [
    #         CountryDocument(
    #             country_name="Country A",
    #             accredited_to_ireland=True,
    #             with_mission_in="london",
    #             hosts_irish_mission=True,
    #             iso3_code=None
    #             ),
    #         CountryDocument(
    #             country_name="Country B",
    #             accredited_to_ireland=True,
    #             with_mission_in="dublin",
    #             hosts_irish_mission=False,
    #             iso3_code=None
    #             )
    #         ]
    #
    #     result = process_country_data._countries_from_json(mock_data)
    #     assert len(result) == len(expected_output)
    #
    #     for res, exp in zip(result, expected_output):
    #         assert res.country_name == exp.country_name
    #         assert res.accredited_to_ireland == exp.accredited_to_ireland
    #         assert res.with_mission_in == exp.with_mission_in
    #         assert res.hosts_irish_mission == exp.hosts_irish_mission
    #         assert res.iso3_code == exp.iso3_code
    #

    def test_country_accredited_to_ie(self):
        assert isinstance(process_country_data._country_accredited_to_ie('Argentina'), bool)

    def test_location_of_foreign_mission_for(self):
        assert process_country_data._location_of_foreign_mission_for("Australia") == 'dublin'
        assert process_country_data._location_of_foreign_mission_for('Aruba') is None
        assert (process_country_data._location_of_foreign_mission_for('Afghanistan') ==
                'london')

    def test_get_proper_name(self):
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
