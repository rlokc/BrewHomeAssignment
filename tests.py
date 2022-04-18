import unittest

from change_monitor import ChangeMonitor
from data_generator import TestDataGenerator
import copy

from entities import CRAWLING_STATUSES


class ChangeMonitorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.monitor = ChangeMonitor()
        self.data_gen = TestDataGenerator()

    # General tests
    def test_created_object_notification(self):
        event1 = self.data_gen.get_event()
        change = self.monitor.check_for_changes(event1, None, event1.__class__.__name__)
        self.assertIsNotNone(change)
        self.assertEqual(event1, change.changed_object)

    def test_deleted_object_notification(self):
        event1 = self.data_gen.get_event()
        change = self.monitor.check_for_changes(None, event1, event1.__class__.__name__)
        self.assertIsNotNone(change)
        self.assertEqual(event1, change.changed_object)

    def test_is_deleted_change(self):
        event1 = self.data_gen.get_event()
        event2 = copy.copy(event1)
        event2.is_deleted = True
        change = self.monitor.check_for_changes(
            event2, event1, event1.__class__.__name__
        )
        self.assertIsNotNone(change)
        self.assertEqual(event2, change.changed_object)

    def test_shouldnt_return_on_no_changes(self):
        event1 = self.data_gen.get_event()
        self.assertIsNone(
            self.monitor.check_for_changes(event1, event1, event1.__class__.__name__)
        )

    # Tests for Company entity
    def test_company_is_deleted(self):
        company = self.data_gen.get_company()
        company2 = copy.copy(company)
        company2.is_deleted = True
        change = self.monitor.check_for_changes(
            company2, company, company.__class__.__name__
        )
        self.assertIsNotNone(change)
        self.assertEqual(company2, change.changed_object)

    def test_company_crawling_status(self):
        company = self.data_gen.get_company()
        company2 = copy.copy(company)
        company2.crawling_status = CRAWLING_STATUSES.TEXT_ANALYZED
        change = self.monitor.check_for_changes(
            company2, company, company.__class__.__name__
        )
        self.assertIsNotNone(change)
        self.assertEqual(company2, change.changed_object)

    def test_company_is_blacklisted_no_notification(self):
        company = self.data_gen.get_company()
        company2 = copy.copy(company)
        company2.is_blacklisted = True
        change = self.monitor.check_for_changes(
            company2, company, company.__class__.__name__
        )
        self.assertIsNone(change)

    # Tests for Event entity
    def test_event_is_deleted(self):
        event = self.data_gen.get_event()
        event2 = copy.copy(event)
        event2.is_deleted = True
        change = self.monitor.check_for_changes(event2, event, event.__class__.__name__)
        self.assertIsNotNone(change)
        self.assertEqual(event2, change.changed_object)

    def test_event_is_blacklisted(self):
        event = self.data_gen.get_event()
        event2 = copy.copy(event)
        event2.is_blacklisted = True
        change = self.monitor.check_for_changes(event2, event, event.__class__.__name__)
        self.assertIsNotNone(change)
        self.assertEqual(event2, change.changed_object)

    def test_event_crawling_status(self):
        event = self.data_gen.get_event()
        event2 = copy.copy(event)
        event2.crawling_status = CRAWLING_STATUSES.TEXT_ANALYZED
        change = self.monitor.check_for_changes(event2, event, event.__class__.__name__)
        self.assertIsNotNone(change)
        self.assertEqual(event2, change.changed_object)

    # Tests for Webinar entity
    def test_webinar_is_deleted(self):
        webinar = self.data_gen.get_webinar()
        webinar2 = copy.copy(webinar)
        webinar2.is_deleted = True
        change = self.monitor.check_for_changes(
            webinar2, webinar, webinar.__class__.__name__
        )
        self.assertIsNotNone(change)
        self.assertEqual(webinar2, change.changed_object)

    def test_webinar_is_blacklisted(self):
        webinar = self.data_gen.get_webinar()
        webinar2 = copy.copy(webinar)
        webinar2.is_blacklisted = True
        change = self.monitor.check_for_changes(
            webinar2, webinar, webinar.__class__.__name__
        )
        self.assertIsNotNone(change)
        self.assertEqual(webinar2, change.changed_object)

    def test_webinar_crawling_status(self):
        webinar = self.data_gen.get_webinar()
        webinar2 = copy.copy(webinar)
        webinar2.crawling_status = CRAWLING_STATUSES.TEXT_ANALYZED
        change = self.monitor.check_for_changes(
            webinar2, webinar, webinar.__class__.__name__
        )
        self.assertIsNotNone(change)
        self.assertEqual(webinar2, change.changed_object)

    # Tests for ContentItem entity
    def test_contentitem_is_deleted(self):
        content_item = self.data_gen.get_content_item()
        content_item2 = copy.deepcopy(content_item)
        content_item2.is_deleted = True
        change = self.monitor.check_for_changes(
            content_item2, content_item, content_item.__class__.__name__
        )
        self.assertIsNotNone(change)
        self.assertEqual(content_item2.company, change.changed_object)

    def test_contentitem_is_blacklisted(self):
        content_item = self.data_gen.get_content_item()
        content_item2 = copy.deepcopy(content_item)
        content_item2.is_blacklisted = True
        change = self.monitor.check_for_changes(
            content_item2, content_item, content_item.__class__.__name__
        )
        self.assertIsNotNone(change)
        self.assertEqual(content_item2.company, change.changed_object)

    def test_contentitem_crawling_status(self):
        content_item = self.data_gen.get_content_item()
        content_item2 = copy.deepcopy(content_item)
        content_item2.crawling_status = CRAWLING_STATUSES.TEXT_UPLOADED
        change = self.monitor.check_for_changes(
            content_item2, content_item, content_item.__class__.__name__
        )
        self.assertIsNotNone(change)
        self.assertEqual(content_item2.company, change.changed_object)

    # Tests for CompanyForEvent entity
    def test_companyforevent_is_deleted(self):
        companyforevent = self.data_gen.get_company_for_event()
        companyforevent2 = copy.deepcopy(companyforevent)
        companyforevent2.is_deleted = True
        change = self.monitor.check_for_changes(
            companyforevent2, companyforevent, companyforevent2.__class__.__name__
        )
        self.assertIsNotNone(change)
        self.assertEqual(companyforevent2.event, change.changed_object)

    def test_companyforevent_is_blacklisted(self):
        companyforevent = self.data_gen.get_company_for_event()
        companyforevent2 = copy.deepcopy(companyforevent)
        companyforevent2.is_blacklisted = True
        change = self.monitor.check_for_changes(
            companyforevent2, companyforevent, companyforevent2.__class__.__name__
        )
        self.assertIsNotNone(change)
        self.assertEqual(companyforevent2.event, change.changed_object)

    # Tests for CompanyCompetitor entity
    def test_companycompetitor_is_deleted(self):
        companycompetitor = self.data_gen.get_company_competitor()
        companycompetitor2 = copy.deepcopy(companycompetitor)
        companycompetitor2.is_deleted = True
        change = self.monitor.check_for_changes(
            companycompetitor2, companycompetitor, companycompetitor.__class__.__name__
        )
        self.assertIsNotNone(change)
        self.assertEqual(companycompetitor2.company, change.changed_object)

    # Tests for CompanyForWebinar entity
    def test_companyforwebinar_is_deleted(self):
        companyforwebinar = self.data_gen.get_company_for_webinar()
        companyforwebinar2 = copy.deepcopy(companyforwebinar)
        companyforwebinar2.is_deleted = True
        change = self.monitor.check_for_changes(
            companyforwebinar2, companyforwebinar, companyforwebinar.__class__.__name__
        )
        self.assertIsNotNone(change)
        self.assertEqual(companyforwebinar2.webinar, change.changed_object)

    def test_companyforwebinar_is_blacklisted(self):
        companyforwebinar = self.data_gen.get_company_for_webinar()
        companyforwebinar2 = copy.deepcopy(companyforwebinar)
        companyforwebinar2.is_blacklisted = True
        change = self.monitor.check_for_changes(
            companyforwebinar2, companyforwebinar, companyforwebinar.__class__.__name__
        )
        self.assertIsNotNone(change)
        self.assertEqual(companyforwebinar2.webinar, change.changed_object)


if __name__ == "__main__":
    unittest.main()
