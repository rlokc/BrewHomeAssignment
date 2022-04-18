from faker import Faker
from entities import (
    Event,
    Company,
    Webinar,
    ContentItem,
    CompanyForEvent,
    CompanyCompetitor,
    CompanyForWebinar,
)


class TestDataGenerator:
    def __init__(self):
        self.fake = Faker()

    def get_event(self):
        return Event(
            start_date=self.fake.date(),
            end_date=self.fake.date(),
            description=self.fake.sentence(),
            location=self.fake.word(),
            link=self.fake.url(),
            name=self.fake.word(),
        )

    def get_company(self):
        return Company(
            link=self.fake.url(),
            name=self.fake.word(),
            employees_min=5,
            employees_max=10,
        )

    def get_webinar(self):
        return Webinar(
            link=self.fake.url(),
            name=self.fake.word(),
            start_date=self.fake.date(),
        )

    def get_content_item(self):
        return ContentItem(
            link=self.fake.url(), name=self.fake.word(), company=self.get_company()
        )

    def get_company_for_event(self):
        return CompanyForEvent(
            event=self.get_event(),
            company=self.get_company(),
        )

    def get_company_competitor(self):
        return CompanyCompetitor(
            company=self.get_company(), competitor=self.get_company()
        )

    def get_company_for_webinar(self):
        return CompanyForWebinar(webinar=self.get_webinar(), company=self.get_company())
