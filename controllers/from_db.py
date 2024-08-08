import pydantic
import beanie
from typing import Type
from schemas.pydantic_schemas import (DiplomatOut, EmbassyOut, ConsulateOut,
                                      RepresentationOut, CountryOut, MissionOut)


# ------------------------------------------------------------------------------
# Direct call Functions
# ------------------------------------------------------------------------------

def pydantic_response_for_all_items(response: list[beanie.Document],
                                    response_model: Type[pydantic.BaseModel]):
    items = []
    for item in response:
        item = item.model_dump()
        if response_model == EmbassyOut:
            items.append(_an_embassy_from(item)
                         )
        elif response_model == RepresentationOut:
            items.append(_a_representation_from(item))

        elif response_model == ConsulateOut:
            items.append(_a_consulate_from(item))

        elif response_model == DiplomatOut:
            items.append(_a_diplomat_from(item))

        elif response_model == MissionOut:
            items.append(_a_mission_from(item))

        else:
            items.append(_a_country_from(item))

    return items


def pydantic_response_for_one_item(response: beanie.Document,
                                   response_model: Type[pydantic.BaseModel]):
    item = response.model_dump()
    if response_model == EmbassyOut:
        return _an_embassy_from(item)

    elif response_model == RepresentationOut:
        return _a_representation_from(item)

    elif response_model == ConsulateOut:
        return _a_consulate_from(item)

    else:
        return _a_diplomat_from(item)


# ------------------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------------------


def _process_embassy_consulates(consulate_list: list[dict]):
    return [ConsulateOut(id=consulate["id"], city=consulate["host_city"],
                         head_of_mission=consulate["head_of_mission"][
                                             "first_name"] + " " +
                                         consulate["head_of_mission"]["last_name"], )
            for consulate in consulate_list if consulate["head_of_mission"]]


def _an_embassy_from(item: dict) -> EmbassyOut:
    return EmbassyOut(id=item["id"], country=item['host_country'],
                      head_of_mission=item['head_of_mission'][
                                          'first_name']
                                      + " " + item['head_of_mission'][
                                          'last_name'],
                      address=item['contact'].get('address1'),
                      telephone=item['contact'].get('tel'),
                      consulates=_process_embassy_consulates(
                          item.get('consulates', [])))


def _a_consulate_from(item: dict) -> ConsulateOut:
    return ConsulateOut(id=item["id"], city=item['host_city'],
                        head_of_mission=item['head_of_mission'][
                                            'first_name']
                                        + " " + item['head_of_mission'][
                                            'last_name'], )


def _a_representation_from(item: dict) -> RepresentationOut:
    return RepresentationOut(
        rep_name=item['representation_name'],
        head_of_mission=item['head_of_mission'][
                            'first_name'] + " " + item['head_of_mission'][
                            'last_name'],
        address=item['contact'].get('address1'), id=item["id"])


def _a_diplomat_from(item: dict) -> DiplomatOut:
    return DiplomatOut(full_name=item["full_name"],
                       last_name=item['last_name'],
                       first_name=item['first_name'],
                       title="Ambassador" if item['mission_type'] == "embassy" else
                       "Consul General",
                       mission_type=item['mission_type'],
                       mission_title=item['mission_title'],
                       id=item["id"])


def _a_country_from(item: dict) -> CountryOut:
    return CountryOut(
        id=item["id"],
        country_name=item['country_name'],
        accredited_to_ireland=item['accredited_to_ireland'],
        with_mission_in=item['with_mission_in'],
        hosts_irish_mission=item['hosts_irish_mission'],
        iso3_code=item['iso3_code'], )


def _a_mission_from(item: dict) -> MissionOut:
    return MissionOut(
        id=item["id"],
        mission_title=item['head_of_mission']['mission_title'],
        head_of_mission=item['head_of_mission']['full_name']
        )
