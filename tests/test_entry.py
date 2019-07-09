import json
import unittest
import sys
import context

from query import Query
from entry import Entry


class TestData:
    def __init__(self, test_data_file):
        self.test_data = self.load(test_data_file)

    def load(self, test_data_file):
        try:
            with open(test_data_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"File: {test_data_file}, not found!")
        except JSONDecodeError:
            raise JSONDecodeError(
                f"File: {test_data_file}, could not be loaded!")


class TestQuery(unittest.TestCase):
    data = TestData("test_data/test_entry_inputs.json")

    def setUp(self):
        self.entry = Entry(self.data.test_data, "test", "_id", "users")

    def test_process(self):
        entry = Entry(self.data.test_data, "123HÈLLOÆ", "_id", "users")
        self.assertEqual(entry.string, "123hèlloæ")

    def test_get_field_exists(self):
        self.entry.data = {"field": "return me"}
        field_data = self.entry.get_field("field")
        self.assertEqual(field_data, "return me")

    def test_get_field_missing(self):
        self.entry.data = {"no_field": "return none"}
        self.assertRaises(KeyError, lambda: self.entry.get_field("field"))

    def test_create_query_field_exists(self):
        self.entry.data = self.data.test_data["org_all_fields"]
        query = self.entry._create_query("_id", "organization_id", "users")
        id = self.entry.data["_id"]

        self.assertEqual(query.string, str(id))
        self.assertEqual(query.field, "organization_id")
        self.assertEqual(query.group, "users")

    def test_create_query_field_missing(self):
        self.entry.data = self.data.test_data["org_missing_id"]
        query = self.entry._create_query("_id", "organization_id", "users")
        self.assertEqual(query, None)

    def test_get_related_queries_user(self):
        test_case = "user_all_fields"
        self.entry.group = "users"

        self.entry.data = self.data.test_data[test_case]
        org_id = self.entry.data["organization_id"]
        id = self.entry.data["_id"]

        related = self.entry.get_related_queries()
        org_query = related["org"]
        submitter_query = related["submitted_tickets"]
        assigned_query = related["assigned_tickets"]

        # check organisation id query
        self.assertEqual(org_query.string, str(org_id))
        self.assertEqual(org_query.field, "_id")
        self.assertEqual(org_query.group, "orgs")

        # check submitter query
        self.assertEqual(submitter_query.string, str(id))
        self.assertEqual(submitter_query.field, "submitter")
        self.assertEqual(submitter_query.group, "tickets")

        # check assigned query
        self.assertEqual(assigned_query.string, str(id))
        self.assertEqual(assigned_query.field, "assignee_id")
        self.assertEqual(assigned_query.group, "tickets")

    def test_get_related_queries_org(self):
        test_case = "org_all_fields"
        self.entry.group = "orgs"

        self.entry.data = self.data.test_data[test_case]
        id = self.entry.data["_id"]

        related = self.entry.get_related_queries()
        user_query = related["users"]
        tickets_query = related["tickets"]

        # check user query
        self.assertEqual(user_query.string, str(id))
        self.assertEqual(user_query.field, "organization_id")
        self.assertEqual(user_query.group, "users")

        # check tickets query
        self.assertEqual(tickets_query.string, str(id))
        self.assertEqual(tickets_query.field, "organization_id")
        self.assertEqual(tickets_query.group, "tickets")

    def test_get_related_query_ticket(self):
        test_case = "ticket_all_fields"
        self.entry.group = "tickets"

        self.entry.data = self.data.test_data[test_case]
        org_id = self.entry.data["organization_id"]
        submitter_id = self.entry.data["submitter_id"]
        assignee_id = self.entry.data["assignee_id"]

        related = self.entry.get_related_queries()
        org_query = related["org"]
        submitter_query = related["submitter"]
        assignee_query = related["assignee"]

        # check organisation id query
        self.assertEqual(org_query.string, str(org_id))
        self.assertEqual(org_query.field, "_id")
        self.assertEqual(org_query.group, "orgs")

        # check submitter query
        self.assertEqual(submitter_query.string, str(submitter_id))
        self.assertEqual(submitter_query.field, "_id")
        self.assertEqual(submitter_query.group, "users")

        # check assigned query
        self.assertEqual(assignee_query.string, str(assignee_id))
        self.assertEqual(assignee_query.field, "_id")
        self.assertEqual(assignee_query.group, "users")

    def test_get_related_queries_missing_fields(self):
        test_case = "user_missing_fields"
        self.entry.data = self.data.test_data[test_case]
        related = self.entry.get_related_queries()

        self.assertEqual(related["assigned_tickets"], None)
        self.assertEqual(related["submitted_tickets"], None)
        self.assertEqual(related["org"], None)

    def test_save_related_results_all_fields(self):
        user_data = self.data.test_data["user_all_fields"]
        org_data = self.data.test_data["org_all_fields"]
        ticket_data = self.data.test_data["ticket_all_fields"]

        # build expected strings
        user_id = user_data["_id"]
        user_name = user_data["name"]
        user_info = f"{user_name} | {user_id}"

        org_id = org_data["_id"]
        org_name = org_data["name"]
        org_info = f"{org_name} | {org_id}"

        ticket_id = ticket_data["_id"]
        ticket_subject = ticket_data["subject"]
        ticket_info = f"{ticket_subject} | {ticket_id}"

        # create dummy entries
        user = Entry(user_data, "test", "_id", "users")
        org = Entry(org_data, "test", "_id", "orgs")
        ticket = Entry(ticket_data, "test", "_id", "tickets")

        expected = {
            "users": [user_info],
            "org": [org_info],
            "ticket": [ticket_info],
            "none": None
        }
        self.entry.related_results = {
            "users": [user],
            "org": [org],
            "ticket": [ticket],
            "none": None
        }
        self.entry.save_related_results()
        self.assertEqual(self.entry.related_results, expected)

    def test_save_related_results_missing_fields(self):
        user_data = self.data.test_data["user_missing_id"]
        org_data = self.data.test_data["org_all_fields"]
        ticket_data = self.data.test_data["ticket_missing_id"]

        # build expected strings
        user_id = None
        user_name = user_data["name"]
        user_info = f"{user_name} | {user_id}"

        org_id = org_data["_id"]
        org_name = org_data["name"]
        org_info = f"{org_name} | {org_id}"

        ticket_id = None
        ticket_subject = ticket_data["subject"]
        ticket_info = f"{ticket_subject} | {ticket_id}"

        # create dummy entries
        user = Entry(user_data, "test", "_id", "users")
        org = Entry(org_data, "test", "_id", "orgs")
        ticket = Entry(ticket_data, "test", "_id", "tickets")

        expected = {
            "users": [user_info],
            "org": [org_info],
            "ticket": [ticket_info],
            "none": None
        }
        self.entry.related_results = {
            "users": [user],
            "org": [org],
            "ticket": [ticket],
            "none": None
        }
        self.entry.save_related_results()
        self.assertEqual(self.entry.related_results, expected)


if __name__ == "__main__":
    unittest.main()