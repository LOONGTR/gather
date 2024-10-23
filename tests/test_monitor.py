# tests/test_monitor.py
import unittest
from src.monitor import get_process_info

class TestMonitor(unittest.TestCase):
    def test_get_process_info(self):
        processes = get_process_info()
        self.assertIsInstance(processes, list)
        if processes:
            self.assertIn('pid', processes[0])
            self.assertIn('name', processes[0])
            self.assertIn('exe', processes[0])
            self.assertIn('cmdline', processes[0])
            self.assertIn('cpu_percent', processes[0])
            self.assertIn('memory_info', processes[0])

if __name__ == '__main__':
    unittest.main()
