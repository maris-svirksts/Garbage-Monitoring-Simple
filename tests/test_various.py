from garbage_monitoring import core, helpers
import unittest
import os

class TestSuite(unittest.TestCase):

    def test_get_full_name(self):
        test_data = core.Employee("Maris", "Svirksts", 1901, "maris.svirksts@gmail.com", "+371 29611111", "Riga", '')
        results   = test_data.get_full_name()

        self.assertEqual(results, "<Maris Svirksts> maris.svirksts@gmail.com")

    def test_non_alphabetic_name(self):
        with self.assertRaises(ValueError):
            core.Employee("Maris1", "Svirksts", 1901, "maris.svirksts@gmail.com", "+371 29611111", "Riga", '')

    def test_non_alphabetic_surname(self):
        with self.assertRaises(ValueError):
            core.Employee("Maris", "Svirksts1", 1901, "maris.svirksts@gmail.com", "+371 29611111", "Riga", '')

    def test_get_year_of_birth_negative(self):
        test_data = core.Employee("Maris", "Svirksts", -1, "maris.svirksts@gmail.com", "+371 29611111", "Riga", '')
        results   = test_data.get_year_of_birth()

        self.assertEqual(results, 2000)

    def test_get_year_of_birth_characters(self):
        test_data = core.Employee("Maris", "Svirksts", 'abcd', "maris.svirksts@gmail.com", "+371 29611111", "Riga", '')
        results   = test_data.get_year_of_birth()

        self.assertEqual(results, 2000)

    def test_get_email_no_at(self):
        test_data = core.Employee("Maris", "Svirksts", 1901, "maris.svirksts", "+371 29611111", "Riga", '')
        results   = test_data.get_email()

        self.assertEqual(results, "maris.svirksts@gmail.com")

    def test_get_mobile(self):
        test_data = core.Employee("Maris", "Svirksts", 1901, "maris.svirksts@gmail.com", "+371 29611111a", "Riga", '')

        self.assertEqual(test_data.get_mobile(), 37129611111)

    def test_get_base64_image(self):
        test_data = core.Employee("Maris", "Svirksts", 1901, "maris.svirksts@gmail.com", "+371 29611111", "Riga", 'images/cbimage.png')

        self.assertEqual(test_data.get_base64_image(), b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=')

    def test_set_forbidden_photo_extension(self): # Requirements say to allow only jpg, I'm allowing jpeg, jpg and png instead, testing for others.
        with self.assertRaises(ValueError):
            core.Employee("Maris", "Svirksts", 1901, "maris.svirksts@gmail.com", "+371 29611111", "Riga", 'images/cbimage.txt')

    def test_set_admin_flag(self):
        with self.assertRaises(ValueError):
            core.Admin("Maris", "Svirksts", 1901, "maris.svirksts@gmail.com", "+371 29611111", "Riga", '', False)

    def test_write_base64_image_to_file(self):
        source_image  = 'images/cbimage.png'
        result_image  = 'images/test.png'

        test_data = core.Employee("Maris", "Svirksts", 1901, "maris.svirksts@gmail.com", "+371 29611111", "Riga", source_image)
        test_data.export_photo(result_image)

        self.assertEqual(test_data.get_base64_image(), helpers.base64_encode_photo(result_image))

if __name__ == '__main__':
    unittest.main()
