from datetime import datetime
from typing import Dict, List, Optional, Union

from pydantic import BaseModel


class Label(BaseModel):
    """Label schema."""

    id: str
    name: str
    color: str


class Coordinates(BaseModel):
    """Coordinates schema."""

    latitude: float
    longitude: float


class Ticket(BaseModel):
    """Ticket schema."""

    id: str
    badges: Dict[str, Union[str, int]]
    checkItemStates: Optional[List[Dict[str, Union[str, int, bool]]]]
    closed: bool
    dateLastActivity: datetime
    desc: str
    descData: Optional[Dict[str, Union[str, int, bool]]]
    due: Optional[datetime]
    dueComplete: bool
    idAttachmentCover: Optional[str]
    idBoard: str
    idChecklists: List[str]
    idLabels: List[str]
    idList: str
    idMembers: List[str]
    idMembersVoted: List[str]
    idShort: int
    labels: List[Label]
    manualCoverAttachment: bool
    name: str
    pos: float
    shortLink: str
    shortUrl: str
    start: Optional[datetime]
    subscribed: bool
    url: str
    address: Optional[str]
    locationName: Optional[str]
    coordinates: Optional[Union[str, Coordinates]]
