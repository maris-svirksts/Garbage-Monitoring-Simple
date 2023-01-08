from garbage_monitoring import core, helpers
from datetime import date
import unittest, unittest.mock, io

class TestSuite(unittest.TestCase):

    # Check full name, surname, email address.
    def test_get_full_name(self):
        test_data = core.Employee("Maris", "Svirksts", 1901, "maris.svirksts@gmail.com", "+371 29611111", "Riga", '')
        self.assertEqual(test_data.get_full_name(), "<Maris Svirksts> maris.svirksts@gmail.com")

    # Check for forbidden values in first name.
    def test_non_alphabetic_name(self):
        with self.assertRaises(ValueError):
            core.Employee("Maris1", "Svirksts", 1901, "maris.svirksts@gmail.com", "+371 29611111", "Riga", '')

    # Check for forbidden values in surname.
    def test_non_alphabetic_surname(self):
        with self.assertRaises(ValueError):
            core.Employee("Maris", "Svirksts1", 1901, "maris.svirksts@gmail.com", "+371 29611111", "Riga", '')

    # Correct year of birth data p1.
    def test_get_year_of_birth_negative(self):
        test_data = core.Employee("Maris", "Svirksts", -1, "maris.svirksts@gmail.com", "+371 29611111", "Riga", '')
        self.assertEqual(test_data.get_year_of_birth(), 2000)

    # Correct year of birth data p2.
    def test_get_year_of_birth_characters(self):
        test_data = core.Employee("Maris", "Svirksts", 'abcd', "maris.svirksts@gmail.com", "+371 29611111", "Riga", '')
        self.assertEqual(test_data.get_year_of_birth(), 2000)

    # Update incomplete email data.
    def test_get_email_no_at(self):
        test_data = core.Employee("Maris", "Svirksts", 1901, "maris.svirksts", "+371 29611111", "Riga", '')
        self.assertEqual(test_data.get_email(), "maris.svirksts@gmail.com")

    # Clear mobile data so it contains only numbers.
    def test_get_mobile(self):
        test_data = core.Employee("Maris", "Svirksts", 1901, "maris.svirksts@gmail.com", "+371 29611111a", "Riga", '')
        self.assertEqual(test_data.get_mobile(), 37129611111)

    # Generate base64 code from image.
    def test_get_base64_image(self):
        test_data = core.Employee("Maris", "Svirksts", 1901, "maris.svirksts@gmail.com", "+371 29611111", "Riga", 'images/cbimage.png')
        self.assertEqual(test_data.get_base64_image(), b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=')

    # Check for forbidden file extensions.
    # Requirements say to allow only jpg, I'm allowing jpeg, jpg and png instead, testing for others.
    def test_set_forbidden_photo_extension(self):
        with self.assertRaises(ValueError):
            core.Employee("Maris", "Svirksts", 1901, "maris.svirksts@gmail.com", "+371 29611111", "Riga", 'images/cbimage.txt')

    # Confirm if admin flag is set.
    def test_set_admin_flag(self):
        with self.assertRaises(ValueError):
            core.Admin("Maris", "Svirksts", 1901, "maris.svirksts@gmail.com", "+371 29611111", "Riga", '', False)

    # Export a base64 encoded image to file.
    def test_write_base64_image_to_file(self):
        source_image  = 'images/cbimage.png'
        result_image  = 'images/test.png'

        test_data = core.Employee("Maris", "Svirksts", 1901, "maris.svirksts@gmail.com", "+371 29611111", "Riga", source_image)
        test_data.export_photo(result_image)

        self.assertEqual(test_data.get_base64_image(), helpers.base64_encode_photo(result_image))

    # Allow to add only certain types of garbage.
    def test_garbage_type(self):
        test_data = core.Volunteer("Maris", "Svirksts", 1901, "maris.svirksts@gmail.com", "+371 29611111", "Riga", '')

        with self.assertRaises(ValueError):
            test_data.add_collected_garbage('gl', 100, 5, '2023-01-03')

    # Add and print to console all of the data about the garbage collected by the volunteer.
    @unittest.mock.patch('sys.stdout', new_callable = io.StringIO)
    def test_collected_garbage(self, mock_stdout):
        test_data = core.Volunteer("Maris", "Svirksts", 1901, "maris.svirksts@gmail.com", "+371 29611111", "Riga", '')

        test_data.add_collected_garbage('glass', 100, 5, '2023-01-03')
        test_data.add_collected_garbage('paper', 100, 2)
        test_data.print_collected_garbage()

        self.assertEqual(mock_stdout.getvalue(), f"2023-01-03: garbage type - glass, garbage weight - 100.0, garbage volume - 5.0, garbage density - 20.0\n{date.today()}: garbage type - paper, garbage weight - 100.0, garbage volume - 2.0, garbage density - 50.0\n")

    # Get part of values, sum them.
    def test_filter_garbage(self):
        test_data = core.Volunteer("Maris", "Svirksts", 1901, "maris.svirksts@gmail.com", "+371 29611111", "Riga", '')

        test_data.add_collected_garbage('glass', 100, 5, '2023-01-03')
        test_data.add_collected_garbage('plastic', 100, 10, '2023-01-04')
        test_data.add_collected_garbage('glass', 10, 5, '2023-01-05')
        test_data.add_collected_garbage('glass', 200, 5, '2023-01-06')
        test_data.add_collected_garbage('glass', 150, 5, '2023-01-07')
        test_data.add_collected_garbage('paper', 100, 2)

        self.assertEqual(test_data.calculate_sums('glass', 'weight', '2023-01-04', '2023-01-06'), float(210))

    # Get all sums.
    @unittest.mock.patch('sys.stdout', new_callable = io.StringIO)
    def test_total_sums(self, mock_stdout):
        test_data = core.Volunteer("Maris", "Svirksts", 1901, "maris.svirksts@gmail.com", "+371 29611111", "Riga", '')

        test_data.add_collected_garbage('glass', 100, 5, '2023-01-03')
        test_data.add_collected_garbage('plastic', 100, 10, '2023-01-04')
        test_data.add_collected_garbage('glass', 10, 5, '2023-01-05')
        test_data.add_collected_garbage('glass', 200, 5, '2023-01-06')
        test_data.add_collected_garbage('glass', 150, 5, '2023-01-07')
        test_data.add_collected_garbage('paper', 100, 2)

        test_data.total_sums()

        self.assertEqual(mock_stdout.getvalue(), '460.0: glass weight\n20.0: glass volume\n92.0: glass density\n100.0: paper weight\n2.0: paper volume\n50.0: paper density\n100.0: plastic weight\n10.0: plastic volume\n10.0: plastic density\n')

if __name__ == '__main__':
    unittest.main()
