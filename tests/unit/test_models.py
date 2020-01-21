import unittest
from unittest.mock import patch

from programlibrary.models import *

"""
Tests that model constructors do the expected thing, and that serialization results in the expected thing
"""
class TestModelMethods(unittest.TestCase):

    def test_format_program(self):
        p = Program((1, "name", "description"))
        self.assertEqual(p.id, 1)
        self.assertEqual(p.name, "name")
        self.assertEqual(p.description, "description")
        self.assertEqual(p.serialize(), {"id":1, "name": "name", "description": "description"})

    def test_format_section(self):
        s = Section((1, 1, "name", "description", 1, "132423.jpg"), "www.mydomain.com:5000/")
        self.assertEqual(s.serialize(), 
            {"id":1, 
            "program_id": 1,
            "name": "name",
            "description": "description",
            "orderIndex": 1,
            "imageUrl": "www.mydomain.com:5000/api/v1/image/132423.jpg"})

    def test_format_activity_static(self):
        a = Activity((1, 1, "<html>hello world <a href='www.fakelink.com'> link </a></html>", None, None))
        self.assertEqual(a.serialize(), 
            {"id":1, 
            "section_id": 1,
            "staticContent": "<html>hello world <a href='www.fakelink.com'> link </a></html>",
            "question_text": None,
            "answers": None,
            "type": "STATIC"})

    def test_format_activity_multiple_choice(self):
        a = Activity((1, 1, None, "<p>some text </p>", ["answer 1", "answer 2"]))
        self.assertEqual(a.serialize(), 
            {"id":1, 
            "section_id": 1,
            "staticContent": None,
            "question_text": "<p>some text </p>",
            "answers": ["answer 1", "answer 2"],
            "type": "MULTIPLE_CHOICE"})


if __name__ == '__main__':
    unittest.main()