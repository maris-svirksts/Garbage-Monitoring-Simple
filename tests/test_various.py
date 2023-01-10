"""Overall Test Suite."""

from datetime import date
import unittest
import unittest.mock
import io
from garbage_monitoring import core, helpers

class TestSuite(unittest.TestCase):
    """Overall Test Class."""

    def test_get_full_name(self):
        """Check full name, surname, email address."""
        test_data = core.Employee({
            'name': "Maris",
            'surname': "Svirksts",
            'year_of_birth': 1901,
            'email': "maris.svirksts@gmail.com",
            'mobile': "+371 29611111",
            'address': "Riga"
        })
        self.assertEqual(test_data.get_full_name(), "<Maris Svirksts> maris.svirksts@gmail.com")

    def test_non_alphabetic_name(self):
        """Check for forbidden values in first name."""
        with self.assertRaises(ValueError):
            core.Employee({
                'name': "Maris1",
                'surname': "Svirksts",
                'year_of_birth': 1901,
                'email': "maris.svirksts@gmail.com",
                'mobile': "+371 29611111",
                'address': "Riga"
            })

    def test_non_alphabetic_surname(self):
        """Check for forbidden values in surname."""
        with self.assertRaises(ValueError):
            core.Employee({
                'name': "Maris",
                'surname': "Svirksts1",
                'year_of_birth': 1901,
                'email': "maris.svirksts@gmail.com",
                'mobile': "+371 29611111",
                'address': "Riga"
            })

    def test_get_year_of_birth_negative(self):
        """Correct year of birth data p1."""
        test_data = core.Employee({
            'name': "Maris",
            'surname': "Svirksts",
            'year_of_birth': -1,
            'email': "maris.svirksts@gmail.com",
            'mobile': "+371 29611111",
            'address': "Riga"
        })
        self.assertEqual(test_data.get_year_of_birth(), 2000)

    def test_get_year_of_birth_characters(self):
        """Correct year of birth data p2."""
        test_data = core.Employee({
            'name': "Maris",
            'surname': "Svirksts",
            'year_of_birth': 'abcd',
            'email': "maris.svirksts@gmail.com",
            'mobile': "+371 29611111",
            'address': "Riga"
        })
        self.assertEqual(test_data.get_year_of_birth(), 2000)

    def test_get_email_no_at(self):
        """Update incomplete email data."""
        test_data = core.Employee({
            'name': "Maris",
            'surname': "Svirksts",
            'year_of_birth': 1901,
            'email': "maris.svirksts",
            'mobile': "+371 29611111",
            'address': "Riga"
        })
        self.assertEqual(test_data.get_email(), "maris.svirksts@gmail.com")

    def test_get_mobile(self):
        """lear mobile data so it contains only numbers."""
        test_data = core.Employee({
            'name': "Maris",
            'surname': "Svirksts",
            'year_of_birth': 1901,
            'email': "maris.svirksts@gmail.com",
            'mobile': "+371 29611111a",
            'address': "Riga"
        })
        self.assertEqual(test_data.get_mobile(), 37129611111)

    def test_get_base64_image(self):
        """Generate base64 code from image."""
        test_data = core.Employee({
            'name': "Maris",
            'surname': "Svirksts",
            'year_of_birth': 1901,
            'email': "maris.svirksts@gmail.com",
            'mobile': "+371 29611111",
            'address': "Riga",
            'photo': "images/cbimage.png"
        })
        self.assertEqual(
            test_data.get_base64_image(),
            b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1H' +
            b'AwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII='
        )

    def test_set_forbidden_photo_extension(self):
        """Check for forbidden file extensions.
        Requirements say to allow only jpg.
        I'm allowing jpeg, jpg and png instead, testing for others."""
        with self.assertRaises(ValueError):
            core.Employee({
                'name': "Maris",
                'surname': "Svirksts",
                'year_of_birth': 1901,
                'email': "maris.svirksts@gmail.com",
                'mobile': "+371 29611111",
                'address': "Riga",
                'photo': "images/cbimage.txt"
            })

    def test_set_admin_flag(self):
        """Confirm if admin flag is set."""
        with self.assertRaises(ValueError):
            core.Admin({
                'name': "Maris",
                'surname': "Svirksts",
                'year_of_birth': 1901,
                'email': "maris.svirksts@gmail.com",
                'mobile': "+371 29611111",
                'address': "Riga"
            }, False)

    def test_write_base64_image_to_file(self):
        """Export a base64 encoded image to file."""
        source_image  = 'images/cbimage.png'
        result_image  = 'images/test.png'

        test_data = core.Employee({
            'name': "Maris",
            'surname': "Svirksts",
            'year_of_birth': 1901,
            'email': "maris.svirksts@gmail.com",
            'mobile': "+371 29611111",
            'address': "Riga",
            'photo': source_image
        })
        test_data.export_photo(result_image)

        self.assertEqual(test_data.get_base64_image(), helpers.base64_encode_photo(result_image))

    def test_garbage_type(self):
        """Allow to add only certain types of garbage."""
        test_data = core.Volunteer({
            'name': "Maris",
            'surname': "Svirksts",
            'year_of_birth': 1901,
            'email': "maris.svirksts@gmail.com",
            'mobile': "+371 29611111",
            'address': "Riga"
        })

        with self.assertRaises(ValueError):
            test_data.add_collected_garbage('gl', 100, 5, '2023-01-03')

    @unittest.mock.patch('sys.stdout', new_callable = io.StringIO)
    def test_collected_garbage(self, mock_stdout):
        """Add and print to console all of the data about the garbage collected by the volunteer."""
        test_data = core.Volunteer({
            'name': "Maris",
            'surname': "Svirksts",
            'year_of_birth': 1901,
            'email': "maris.svirksts@gmail.com",
            'mobile': "+371 29611111",
            'address': "Riga"
        })

        test_data.add_collected_garbage('glass', 100, 5, '2023-01-03')
        test_data.add_collected_garbage('paper', 100, 2)
        test_data.print_collected_garbage()

        self.assertEqual(
            mock_stdout.getvalue(),
            '2023-01-03: garbage type - glass, garbage weight - 100.0,' +
            ' garbage volume - 5.0, garbage density - 20.0' +
            f'\n{date.today()}' +
            ': garbage type - paper, garbage weight - 100.0,' +
            ' garbage volume - 2.0, garbage density - 50.0\n'
        )

    def test_filter_garbage(self):
        """Get part of values, sum them."""
        test_data = core.Volunteer({
            'name': "Maris",
            'surname': "Svirksts",
            'year_of_birth': 1901,
            'email': "maris.svirksts@gmail.com",
            'mobile': "+371 29611111",
            'address': "Riga"
        })

        test_data.add_collected_garbage('glass', 100, 5, '2023-01-03')
        test_data.add_collected_garbage('plastic', 100, 10, '2023-01-04')
        test_data.add_collected_garbage('glass', 10, 5, '2023-01-05')
        test_data.add_collected_garbage('glass', 200, 5, '2023-01-06')
        test_data.add_collected_garbage('glass', 150, 5, '2023-01-07')
        test_data.add_collected_garbage('paper', 100, 2)

        self.assertEqual(
            test_data.calculate_sums(
                'glass',
                'weight',
                '2023-01-04',
                '2023-01-06'
            ),
            float(210)
        )

    @unittest.mock.patch('sys.stdout', new_callable = io.StringIO)
    def test_total_sums(self, mock_stdout):
        """Get all sums.
        Summing density is of dubious usage, still: was described so in the requirements.
        In real life would ask for confirmation."""
        test_data = core.Volunteer({
            'name': "Maris",
            'surname': "Svirksts",
            'year_of_birth': 1901,
            'email': "maris.svirksts@gmail.com",
            'mobile': "+371 29611111",
            'address': "Riga"
        })

        test_data.add_collected_garbage('glass', 100, 5, '2023-01-03')
        test_data.add_collected_garbage('plastic', 100, 10, '2023-01-04')
        test_data.add_collected_garbage('glass', 10, 5, '2023-01-05')
        test_data.add_collected_garbage('glass', 200, 5, '2023-01-06')
        test_data.add_collected_garbage('glass', 150, 5, '2023-01-07')
        test_data.add_collected_garbage('paper', 100, 2)

        test_data.total_sums()

        self.assertEqual(
            mock_stdout.getvalue(),
            '460.0: glass weight\n20.0: glass volume\n92.0: glass density\n' +
            '100.0: paper weight\n2.0: paper volume\n50.0: paper density\n' +
            '100.0: plastic weight\n10.0: plastic volume\n10.0: plastic density\n'
        )

if __name__ == '__main__':
    unittest.main()
