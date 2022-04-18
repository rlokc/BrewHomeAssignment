from dataclasses import dataclass
from typing import Optional, Tuple, Any, Dict

import entities
import pprint


@dataclass
class ChangeMessage:
    changed_object: entities.CrawlableEntity

    def __post_init__(self):
        # Here printing the dict because the entities don't have __repr__
        # Also ideally creating an object shouldn't have side effects like this, but this is just a quick thing
        # so I don't have to handle the ChangeMessage anywhere else
        print(f"Notify on:\r\n{pprint.pformat(self.changed_object.__dict__, indent=4)}")


class ChangeMonitor:
    """
    Service that checks for changes that happen to the entities
    Every entity is checked whether it is physically a new entity, or it got deleted
    Plus for every entity we do specific checks according to the _change_notification_check map
    """

    _not_same_check = lambda old, new: old != new
    _check_for_finished_crawling = lambda old, new: old != new and new in (
        entities.CRAWLING_STATUSES.TEXT_ANALYZED,
        entities.CRAWLING_STATUSES.TEXT_UPLOADED,
    )

    _change_notification_checks = {
        "Company": {
            "is_deleted": _not_same_check,
            "crawling_status": _check_for_finished_crawling,
        },
        "Event": {
            "is_deleted": _not_same_check,
            "is_blacklisted": _not_same_check,
            "crawling_status": _check_for_finished_crawling,
        },
        "Webinar": {
            "is_deleted": _not_same_check,
            "is_blacklisted": _not_same_check,
            "crawling_status": _check_for_finished_crawling,
        },
        "ContentItem": {
            "is_deleted": _not_same_check,
            "is_blacklisted": _not_same_check,
            "crawling_status": _check_for_finished_crawling,
        },
        "CompanyForEvent": {
            "is_deleted": _not_same_check,
            "is_blacklisted": _not_same_check,
        },
        "CompanyCompetitor": {
            "is_deleted": _not_same_check,
        },
        "CompanyForWebinar": {
            "is_deleted": _not_same_check,
            "is_blacklisted": _not_same_check,
        },
    }

    def check_for_changes(
        self,
        entity_obj: Optional[object],
        original_entity_obj: Optional[object],
        entity_type: str,
    ) -> Optional[ChangeMessage]:
        if entity_obj is None and original_entity_obj is None:
            raise RuntimeError("Both of the input entities are None")
        if entity_obj is None:
            return ChangeMessage(self.extract_notification_object(original_entity_obj))
        if original_entity_obj is None:
            return ChangeMessage(self.extract_notification_object(entity_obj))

        changes = self.get_entity_changes(original_entity_obj, entity_obj)
        if entity_type not in self._change_notification_checks:
            raise RuntimeError(f"No change checks defined for type {entity_type}")
        for prop, check_fn in self._change_notification_checks[entity_type].items():
            if prop not in changes:
                continue
            old_value, new_value = changes[prop]
            if check_fn(old_value, new_value):
                return ChangeMessage(self.extract_notification_object(entity_obj))
        return None

    @staticmethod
    def get_entity_changes(obj1: object, obj2: object) -> Dict[str, Tuple[Any, Any]]:
        changes = {}
        # Note: this will not work with any deferred loaded entities,
        #       so only works on this simplistic home assignment case
        changeset = obj1.__dict__.items() ^ obj2.__dict__.items()
        for key, value in changeset:
            if key in changes:
                continue
            changes[key] = (obj1.__dict__.get(key), obj2.__dict__.get(key))
        return changes

    @staticmethod
    def extract_notification_object(entity) -> entities.CrawlableEntity:
        """
        Extract the object that will be the notification target
        """
        if type(entity) is entities.ContentItem:
            return entity.company
        if type(entity) is entities.CompanyForEvent:
            return entity.event
        elif type(entity) is entities.CompanyCompetitor:
            return entity.company
        elif type(entity) is entities.CompanyForWebinar:
            return entity.webinar
        else:
            return entity
