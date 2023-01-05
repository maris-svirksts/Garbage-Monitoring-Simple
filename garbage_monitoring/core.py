from . import helpers
import time
import re

class Employee:
    # Long list of input variables, switch to array?
    def __init__(self, name, surname, year_of_birth, email, mobile, address, photo = ''):
        self.__created     = int(time.time()) 
        self.name          = name
        self.surname       = surname
        self.year_of_birth = year_of_birth
        self.email         = email
        self.mobile        = mobile
        self.address       = address
        self.photo         = photo

    @property
    def created(self):
        return self.__created

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = helpers.check_word(value)

    @property
    def surname(self):
        return self._name

    @surname.setter
    def surname(self, value):
        self._surname = helpers.check_word(value)

    @property
    def year_of_birth(self):
        return self._year_of_birth

    @year_of_birth.setter
    def year_of_birth(self, value):
        default_value = 2000

        try:
            if(int(value)) > 0:
                self._year_of_birth = int(value)
            else:
                self._year_of_birth = default_value
        except:
            self._year_of_birth = default_value

    @property
    def email(self):
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
        return self._mobile

    @mobile.setter
    def mobile(self, value):
        regex   = r"[0-9]+"
        numbers = re.findall(regex, value)

        self._mobile = int("".join(numbers))

    @property
    def photo(self):
        return self._photo

    @photo.setter
    def photo(self, value):
        if value:
            helpers.validate_extension(value)
            self._photo = helpers.base64_encode_photo(value)

    def get_full_name(self):
        return f"<{self._name} {self._surname}> {self._email}"

    def get_year_of_birth(self):
        return self._year_of_birth

    def get_email(self):
        return self._email
    
    def get_mobile(self):
        return self._mobile

    def get_base64_image(self):
        return self._photo

    def export_photo(self, result_image):
        helpers.base64_photo_to_file(self._photo, result_image)

class Admin(Employee):
    def __init__(self, name, surname, year_of_birth, email, mobile, address, photo = '', is_admin = False):
        Employee.__init__(self, name, surname, year_of_birth, email, mobile, address, photo)
        self.is_admin = is_admin # I'd set it automatically and forget about it, but, the task has this as a requirement

    @property
    def is_admin(self):
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        self._is_admin = helpers.check_if_true(value)

class Volunteer(Employee):
    pass