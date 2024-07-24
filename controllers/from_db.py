import pydantic
import beanie
from typing import Type
from schemas.consulate import ConsulateOut
from schemas.embassy import EmbassyOut
from schemas.representation import RepresentationOut


def _process_embassy_consulates(consulate_list: list[dict]):
    return [ConsulateOut(city=consulate["host_city"],
                         head_of_mission=consulate["head_of_mission"][
                                             "first_name"] + " " +
                                         consulate["head_of_mission"]["last_name"])
            for consulate in consulate_list if consulate["head_of_mission"]]


def _an_embassy_from(item: dict) -> EmbassyOut:
    return EmbassyOut(country=item['host_country'],
                      head_of_mission=item['head_of_mission'][
                                          'first_name']
                                      + " " + item['head_of_mission'][
                                          'last_name'],
                      address=item['contact'].get('address1'),
                      telephone=item['contact'].get('tel'),
                      consulates=_process_embassy_consulates(
                          item.get('consulates', [])), )


def _a_consulate_from(item: dict) -> ConsulateOut:
    return ConsulateOut(city=item['host_city'],
                        head_of_mission=item['head_of_mission'][
                                            'first_name']
                                        + " " + item['head_of_mission'][
                                            'last_name'])


def _a_representation_from(item: dict) -> RepresentationOut:
    return RepresentationOut(
        rep_name=item['representation_name'],
        head_of_mission=item['head_of_mission'][
                            'first_name'] + " " + item['head_of_mission'][
                            'last_name'],
        address=item['contact'].get('address1'), )


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

    return items


def pydantic_response_for_one_item(response: beanie.Document,
                                   response_model: Type[pydantic.BaseModel]):
    item = response.model_dump()
    if response_model == EmbassyOut:
        return _an_embassy_from(item)

    elif response_model == RepresentationOut:
        return _a_representation_from(item)

    else:
        return _a_consulate_from(item)
