#!/usr/bin/env python3
import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import importlib.util

# Load module with hyphenated filename
src_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'gnome-web-search-provider.py')
spec = importlib.util.spec_from_file_location("gnome_web_search_provider", src_path)
gnome_web_search_provider = importlib.util.module_from_spec(spec)
sys.modules["gnome_web_search_provider"] = gnome_web_search_provider
spec.loader.exec_module(gnome_web_search_provider)

WebSearchProvider = gnome_web_search_provider.WebSearchProvider
BUS_NAME = gnome_web_search_provider.BUS_NAME
OBJECT_PATH = gnome_web_search_provider.OBJECT_PATH


class TestWebSearchProvider(unittest.TestCase):
    def setUp(self):
        self.provider = WebSearchProvider()

    def test_bus_name(self):
        self.assertEqual(BUS_NAME, "org.gnome.WebSearch.SearchProvider")

    def test_object_path(self):
        self.assertEqual(OBJECT_PATH, "/org/gnome/WebSearch/SearchProvider")

    def test_get_initial_result_set_single_term(self):
        result = self.provider.GetInitialResultSet(["hello"])
        self.assertEqual(result, ["hello"])

    def test_get_initial_result_set_multiple_terms(self):
        result = self.provider.GetInitialResultSet(["hello", "world"])
        self.assertEqual(result, ["hello world"])

    def test_get_initial_result_set_empty(self):
        result = self.provider.GetInitialResultSet([])
        self.assertEqual(result, [""])

    def test_get_subsearch_result_set(self):
        result = self.provider.GetSubsearchResultSet(["previous"], ["new", "search"])
        self.assertEqual(result, ["new search"])

    def test_get_result_metas_structure(self):
        result = self.provider.GetResultMetas(["test query"])
        self.assertEqual(len(result), 1)
        meta = result[0]
        self.assertIn("id", meta)
        self.assertIn("name", meta)
        self.assertIn("description", meta)
        self.assertIn("icon", meta)

    def test_get_result_metas_values(self):
        result = self.provider.GetResultMetas(["test query"])
        meta = result[0]
        # Variant wraps the value, access with get_string() or unpack()
        self.assertEqual(meta["id"].unpack(), "test query")
        self.assertEqual(meta["name"].unpack(), "Search Google for 'test query'")
        self.assertEqual(meta["description"].unpack(), "Press Enter to open in browser")
        self.assertEqual(meta["icon"].unpack(), "web-browser")

    def test_get_result_metas_multiple(self):
        result = self.provider.GetResultMetas(["query1", "query2"])
        self.assertEqual(len(result), 2)

    @patch('gnome_web_search_provider.subprocess.Popen')
    def test_activate_result(self, mock_popen):
        self.provider.ActivateResult("test query", ["test", "query"], 0)
        mock_popen.assert_called_once()
        call_args = mock_popen.call_args[0][0]
        self.assertEqual(call_args[0], "xdg-open")
        self.assertIn("google.com/search", call_args[1])
        self.assertIn("q=test query", call_args[1])

    @patch('gnome_web_search_provider.subprocess.Popen')
    def test_activate_result_escapes_html(self, mock_popen):
        self.provider.ActivateResult("<script>", ["<script>"], 0)
        mock_popen.assert_called_once()
        call_args = mock_popen.call_args[0][0]
        self.assertIn("&lt;script&gt;", call_args[1])

    def test_launch_search_does_nothing(self):
        # LaunchSearch is a no-op, just verify it doesn't raise
        self.provider.LaunchSearch(["test"], 0)

    def test_dbus_xml_interface(self):
        # Verify the D-BUS XML contains required interface
        self.assertIn("org.gnome.Shell.SearchProvider2", self.provider.__dbus_xml__)
        self.assertIn("GetInitialResultSet", self.provider.__dbus_xml__)
        self.assertIn("GetSubsearchResultSet", self.provider.__dbus_xml__)
        self.assertIn("GetResultMetas", self.provider.__dbus_xml__)
        self.assertIn("ActivateResult", self.provider.__dbus_xml__)
        self.assertIn("LaunchSearch", self.provider.__dbus_xml__)


if __name__ == "__main__":
    unittest.main()
