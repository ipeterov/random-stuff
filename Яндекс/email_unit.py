import unittest
from email import *


class TestEmailCheck(unittest.TestCase):

    def test_normal(self):
        self.assertTrue(check_email('""ipet"!,:"ero._-;v1@g-m.a_.i.l.com'))

    def test_at(self):
        self.assertFalse(check_email('ipe@terov1@gmail.com'))
        self.assertFalse(check_email('ipeterov1gmail.com'))

    def test_domain(self):
        self.assertFalse(check_email('ipeterov1@gm'))
        self.assertFalse(check_email('ipeterov1@g.'))
        self.assertFalse(check_email('ipeterov1@gmailcom'))
        self.assertFalse(check_email('ipeterov1@{}longdomain.com'.format('very' * 61)))

    def test_domain_substrings(self):
        self.assertFalse(check_email('ipeterov1@gmail-.com'))
        self.assertFalse(check_email('ipeterov1@gmAil.com'))
        self.assertFalse(check_email('ipeterov1@gmail.c*m'))
        self.assertFalse(check_email('ipeterov1@gm&$il.com'))

    def test_name(self):
        self.assertFalse(check_email('ipe"terov1@gmail.com'))
        self.assertFalse(check_email('ipe"ter""ov1@gmail.com'))
        self.assertFalse(check_email('ipe""terov1!@gmail.com'))
        self.assertFalse(check_email('ipete...rov1@gmail.com'))
        self.assertFalse(check_email('{}longname@gmail.com'.format('very' * 31)))


if __name__ == '__main__':
    unittest.main()
