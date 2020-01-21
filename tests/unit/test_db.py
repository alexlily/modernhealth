import unittest
from unittest.mock import patch

from programlibrary.db import *

class TestDBMethods(unittest.TestCase):

    def test_format_query(self):
        self.assertEqual(format_query(GET_PROGRAMS_QUERY, []), """select * from programs;""")
        self.assertEqual(format_query("""select with arguments: {} {} """, [1, 2]), """select with arguments: 1 2 """)

    @patch("psycopg2.connect")
    def test_make_query_throws_exception(self, mock_connect):
        mock_connect.return_value.cursor.return_value.execute.side_effect = Exception("throw an exception")
        expected = []
        mock_connect.return_value.cursor.return_value.fetchall.return_value = expected

        result = makeQuery(GET_PROGRAMS_QUERY)

        self.assertEqual(result, None)

    @patch("psycopg2.connect")
    def test_make_query_list_happy(self, mock_connect):
        expected = [(1, "program 1", "desc 1"), (2, "program 2", "desc 2"), (3, "program 3", "desc 3")]
        mock_connect.return_value.cursor.return_value.fetchall.return_value = expected

        result = makeQuery("""select * from public."programs";""")

        self.assertEqual(result, expected)

    @patch("psycopg2.connect")
    def test_make_query_with_arg_happy(self, mock_connect):
        expected = [(1, "section 1", "desc 1")]
        mock_connect.return_value.cursor.return_value.fetchall.return_value = expected

        result = makeQuery("""select * from public.sections where program_id = {}""", 1)

        self.assertEqual(result, expected)


if __name__ == '__main__':
    pwd = os.getenv('PWD')
    sys.path.append(pwd)
    sys.path.append(pwd+'/src/programlibrary')
    sys.path.append(pwd+'/src/config')
    unittest.main()