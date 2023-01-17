"""Main functionality file."""

import re
from datetime import date, datetime
from garbage_monitoring import helpers

class Employee:
    """Parent class. Contains functionality used by both Admin and Volunteer classes."""

    # pylint: disable=too-many-instance-attributes
    # Eight is reasonable in this case.

    def __init__(self, parameters):
        self.__created     = int(datetime.now().timestamp())
        self.name          = parameters.get('name')
        self.surname       = parameters.get('surname')
        self.year_of_birth = parameters.get('year_of_birth')
        self.email         = parameters.get('email')
        self.mobile        = parameters.get('mobile')
        self.address       = parameters.get('address')
        self.photo         = parameters.get('photo', '')

    @property
    def created(self):
        """A variable getter function."""
        return self.__created

    @property
    def name(self):
        """A variable getter function."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = helpers.check_word(value)

    @property
    def surname(self):
        """A variable getter function."""
        return self._name

    @surname.setter
    def surname(self, value):
        self._surname = helpers.check_word(value)

    @property
    def year_of_birth(self):
        """A variable getter function."""
        return self._year_of_birth

    @year_of_birth.setter
    def year_of_birth(self, value):
        default_value = 2000

        try:
            if(int(value)) > 0:
                self._year_of_birth = int(value)
            else:
                self._year_of_birth = default_value
        except ValueError:
            self._year_of_birth = default_value

    @property
    def email(self):
        """A variable getter function."""
        return self._email

    @email.setter
    def email(self, value):
        regex = r"^\S+@\S+\.\S+$"
        if not re.match(regex, value): # As per task instructions, overall: sloppy.
            self._email = value + "@gmail.com"
        else:
            self._email = value

    @property
    def mobile(self):
        """A variable getter function."""
        return self._mobile

    @mobile.setter
    def mobile(self, value):
        regex   = r"[0-9]+"
        numbers = re.findall(regex, value)

        self._mobile = int("".join(numbers))

    @property
    def photo(self):
        """A variable getter function."""
        return self._photo

    @photo.setter
    def photo(self, value):
        if value:
            helpers.validate_extension(value)
            self._photo = helpers.base64_encode_photo(value)

    def get_full_name(self):
        """Return name, surname and email as preformated string."""
        return f"<{self._name} {self._surname}> {self._email}"

    def get_year_of_birth(self):
        """A variable getter function."""
        return self._year_of_birth

    def get_email(self):
        """A variable getter function."""
        return self._email

    def get_mobile(self):
        """A variable getter function."""
        return self._mobile

    def get_base64_image(self):
        """A variable getter function."""
        return self._photo

    def export_photo(self, result_image):
        """Save a photo from string to file."""
        helpers.base64_photo_to_file(self._photo, result_image)

class Admin(Employee):
    """Data about administrators."""
    def __init__(self, parameters, is_admin = False):
        Employee.__init__(self, parameters)
        self.is_admin = is_admin # I'd set it automatically, the task requires it.

    @property
    def is_admin(self):
        """A variable getter function."""
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        self._is_admin = helpers.check_if_true(value)

class Volunteer(Employee):
    """Garbage collected, timestamps and various functionality related to the actual work."""
    __date_format = '%Y-%M-%d'

    def __init__(self, parameters):
        Employee.__init__(self, parameters)
        self._collected_garbage = {}

    def add_collected_garbage(self, garbage_type, garbage_weight, garbage_volume, date_gathered = str(date.today())):
        """Check if the type of garbage is allowed, gather additional data about it."""
        allowed_types = ["glass", "paper", "plastic"]
        if garbage_type.lower() not in allowed_types:
            raise ValueError("Garbage Type Not Allowed: ", garbage_type)

        garbage_density = float(garbage_weight) / float(garbage_volume)
        unix_time       = int(datetime.timestamp(
                            datetime.strptime(date_gathered, self.__date_format))
                        )

        self._collected_garbage[unix_time] = (
            garbage_type.lower(),
            float(garbage_weight),
            float(garbage_volume),
            garbage_density
        )

    def print_collected_garbage(self):
        """Print overall garbage data."""
        for (key, values) in self._collected_garbage.items():
            print(
                f"{datetime.fromtimestamp(key).strftime(self.__date_format)}: "
                f"garbage type - {values[0]}, garbage weight - {values[1]}, "
                f"garbage volume - {values[2]}, garbage density - {values[3]}")

    def calculate_sums(self, parameters):
        """Total amount of various types of garbage."""
        if not parameters.get('start_date'):
            start_date = min(self._collected_garbage)
        else:
            start_date = int(datetime.timestamp(
                datetime.strptime(parameters.get('start_date'), self.__date_format)))

        if not parameters.get('end_date'):
            end_date = max(self._collected_garbage)
        else:
            end_date = int(datetime.timestamp(
                datetime.strptime(parameters.get('end_date'), self.__date_format)))

        if 'weight' == parameters.get('garbage_parameter'):
            parameter_to_get = 1
        elif 'volume' == parameters.get('garbage_parameter'):
            parameter_to_get = 2
        else:
            parameter_to_get = 3

        filtered_list = [
            values[parameter_to_get] for key, values in self._collected_garbage.items()
                if values[0] == parameters.get('type_of_garbage').lower()
                and start_date <= key <= end_date]

        return sum(filtered_list)

    def total_sums(self):
        """Print all sums for garbage types."""
        #TODO: move types and parameters to an outside location (everywhere).
        #TODO: Summing density is of dubious usage, still: was described so in the requirements.
        type_of_garbage   = ["glass", "paper", "plastic"]
        garbage_parameter = ['weight', 'volume', 'density']

        for current_element in type_of_garbage:
            for current_parameter in garbage_parameter:
                results = self.calculate_sums({
                    'type_of_garbage': current_element,
                    'garbage_parameter': current_parameter})
                print(
                    f"{results}: "
                    f"{current_element} {current_parameter}")
