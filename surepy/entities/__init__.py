from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from surepy.enums import EntityType, Location


class SurepyEntity(ABC):
    def __init__(self, data: dict[str, Any]):

        # sure petcare id
        self._id: int = int(data.get("id", data.get("_id")))

        # self._sac: SureAPIClient = sac
        self._data = data
        self._type = EntityType(int(data.get("product_id", 0)))

        self._name: str = str(self._data.get("name"))

    @property
    def id(self) -> int:
        return self._id

    @property
    def unique_id(self):
        return f"{self.household_id}-{self.id}"

    @property
    def name(self) -> str:
        return self._name

    @property
    def full_name(self) -> str:
        return f"{self.type.name}_{self.name}"

    @property
    def type(self) -> EntityType:
        return self._type

    @property
    def household_id(self) -> int | None:
        """ID of the household the entity belongs to."""
        return (
            int(household_id) if (household_id := self._data.get("household_id")) else None  # noqa
        )

    def raw_data(self) -> dict[str, Any]:
        return self._data


@dataclass
class StateFeeding:
    change: list[float]
    at: datetime | None


@dataclass
class StateDrinking:
    change: list[float]
    at: datetime | None


@dataclass
class PetLocationData:

    where: Location
    since: datetime | None

    def __str__(self) -> str:
        return self.where.name.title()


@dataclass
class PetActivity(PetLocationData):
    pass


@dataclass
class PetLocation(PetLocationData):
    pass
