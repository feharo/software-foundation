import unittest
from scripts.new_saas import setup_copy_command


class WindowsOutputTests(unittest.TestCase):
    def test_windows_uses_powershell_copy_item(self):
        self.assertEqual(setup_copy_command("win32"), "Copy-Item .env.example .env.local")

    def test_linux_uses_cp(self):
        self.assertEqual(setup_copy_command("linux"), "cp .env.example .env.local")


if __name__ == "__main__":
    unittest.main()
