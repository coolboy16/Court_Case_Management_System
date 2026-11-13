import os
import tempfile
import unittest
from unittest.mock import patch
import main


class CourtCaseSystemTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_dir = os.getcwd()
        os.chdir(self.temp_dir.name)
        main.initialize_files()

    def tearDown(self):
        os.chdir(self.old_dir)
        self.temp_dir.cleanup()

    def test_search_case_number_data_can_be_found(self):
        main.write_records(main.CASES_FILE, main.CASE_FIELDS, [{
            "case_number": "CC001", "case_title": "Sample v Example",
            "case_type": "Civil", "filing_date": "2026-11-01",
            "status": "Open", "notes": "Fictional"
        }])
        with patch("builtins.input", side_effect=["1", "CC001"]), \
             patch("builtins.print") as printed:
            main.search_case()
        self.assertTrue(any("Sample v Example" in str(call) for call in printed.call_args_list))

    def test_hearing_rejects_unknown_case(self):
        with patch("builtins.input", side_effect=["CC999"]), \
             patch("builtins.print") as printed:
            main.schedule_hearing()
        self.assertTrue(any("does not exist" in str(call) for call in printed.call_args_list))
        self.assertEqual(main.read_records(main.HEARINGS_FILE, main.HEARING_FIELDS), [])

    def test_status_update(self):
        main.write_records(main.CASES_FILE, main.CASE_FIELDS, [{
            "case_number": "CC001", "case_title": "Sample v Example",
            "case_type": "Civil", "filing_date": "2026-11-01",
            "status": "Open", "notes": ""
        }])
        with patch("builtins.input", side_effect=["CC001", "Closed"]), \
             patch("builtins.print"):
            main.update_case_status()
        saved = main.read_records(main.CASES_FILE, main.CASE_FIELDS)
        self.assertEqual(saved[0]["status"], "Closed")

    def test_date_and_time_validation(self):
        self.assertTrue(main.valid_date("2026-11-19"))
        self.assertFalse(main.valid_date("19-11-2026"))
        self.assertTrue(main.valid_time("09:30"))
        self.assertFalse(main.valid_time("9:30 PM"))


if __name__ == "__main__":
    unittest.main()
