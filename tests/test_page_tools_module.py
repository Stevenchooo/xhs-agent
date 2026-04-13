import unittest

from pages import page_content
from pages import page_engagement
from pages import page_extras
from pages import page_lab
from pages import page_management
from pages import page_tools


class PageToolsModuleTests(unittest.TestCase):
    def test_exif_helpers_define_required_module_constants(self):
        self.assertTrue(hasattr(page_tools, "PROJECT_ROOT"))
        self.assertTrue(hasattr(page_tools, "EXIF_SCRIPT_PATH"))
        self.assertTrue(hasattr(page_tools, "SUPPORTED_IMAGE_SUFFIXES"))

    def test_load_exif_camera_options_returns_tuple(self):
        options, error = page_tools.load_exif_camera_options()

        self.assertIsInstance(options, list)
        self.assertIsInstance(error, str)

    def test_ai_pages_expose_shared_ai_gate(self):
        for module in (
            page_content,
            page_engagement,
            page_extras,
            page_lab,
            page_management,
        ):
            self.assertTrue(hasattr(module, "OPENAI_API_KEY"))
            self.assertTrue(hasattr(module, "AI_SETUP_ERROR"))
            self.assertIsNotNone(module.OPENAI_API_KEY)
            self.assertIsInstance(module.AI_SETUP_ERROR, str)


if __name__ == "__main__":
    unittest.main()
