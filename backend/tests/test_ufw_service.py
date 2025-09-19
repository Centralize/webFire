# (C) 2025 by OPNLAB Development. All rights reserved.
import unittest
from unittest.mock import patch, MagicMock

from ufw_service import (
    get_ufw_status,
    get_ufw_rules,
    add_ufw_rule,
    delete_ufw_rule,
    enable_ufw,
    disable_ufw,
    Rule,
)

class TestUfwService(unittest.TestCase):

    @patch('ufw_service.subprocess.run')
    def test_get_ufw_status_active(self, mock_run):
        mock_result = MagicMock()
        mock_result.stdout = "Status: active"
        mock_run.return_value = mock_result
        status = get_ufw_status()
        self.assertEqual(status, {"status": "active"})

    @patch('ufw_service.subprocess.run')
    def test_get_ufw_status_inactive(self, mock_run):
        mock_result = MagicMock()
        mock_result.stdout = "Status: inactive"
        mock_run.return_value = mock_result
        status = get_ufw_status()
        self.assertEqual(status, {"status": "inactive"})

    @patch('ufw_service.subprocess.run')
    def test_get_ufw_rules(self, mock_run):
        mock_result = MagicMock()
        mock_result.stdout = "Status: active\nTo                         Action      From\n--                         ------      ----\n22/tcp                     ALLOW       Anywhere\n80/tcp                     ALLOW       Anywhere\n"
        mock_run.return_value = mock_result
        rules = get_ufw_rules()
        self.assertEqual(rules['status'], 'active')
        self.assertEqual(len(rules['rules']), 2)
        self.assertEqual(rules['rules'][0]['To'], '22/tcp')
        self.assertEqual(rules['rules'][0]['Action'], 'ALLOW')
        self.assertEqual(rules['rules'][0]['From'], 'Anywhere')


    @patch('ufw_service.subprocess.run')
    def test_add_ufw_rule(self, mock_run):
        mock_result = MagicMock()
        mock_result.stdout = "Rule added"
        mock_run.return_value = mock_result
        rule = Rule(action="allow", port="80", protocol="tcp")
        result = add_ufw_rule(rule)
        self.assertEqual(result, {"status": "success", "message": "Rule added"})

    @patch('ufw_service.subprocess.run')
    def test_delete_ufw_rule(self, mock_run):
        mock_result = MagicMock()
        mock_result.stdout = "Rule deleted"
        mock_run.return_value = mock_result
        result = delete_ufw_rule(1)
        self.assertEqual(result, {"status": "success", "message": "Rule deleted"})

    @patch('ufw_service.subprocess.run')
    def test_enable_ufw(self, mock_run):
        mock_result = MagicMock()
        mock_result.stdout = "Firewall is active and enabled on system startup"
        mock_run.return_value = mock_result
        result = enable_ufw()
        self.assertEqual(result, {"status": "success", "message": "Firewall is active and enabled on system startup"})

    @patch('ufw_service.subprocess.run')
    def test_disable_ufw(self, mock_run):
        mock_result = MagicMock()
        mock_result.stdout = "Firewall stopped and disabled on system startup"
        mock_run.return_value = mock_result
        result = disable_ufw()
        self.assertEqual(result, {"status": "success", "message": "Firewall stopped and disabled on system startup"})


if __name__ == '__main__':
    unittest.main()
