import doctest
import os
import unittest


whitelist = [
    "p4.py",
    "p5.py",
    "p6.py",
    "p7.py",
    "p8.py",
    "p9.py",
    "p10.py",
    "p11.py",
    # "p12.py",  # too slow
    "p13.py",
    "p14.py",
    "p15.py",
    "p87.py",
    # "p71.py",  # too slow
]


if __name__ == "__main__":
    suite = unittest.TestSuite()
    current_dir = os.path.dirname(__file__)

    for filename in os.listdir(current_dir):
        if not filename.startswith("p") or not filename.endswith(".py"):
            continue

        if filename not in whitelist:
            continue

        module_name = filename[:-3]

        suite.addTest(doctest.DocTestSuite(module_name))

    unittest.TextTestRunner(verbosity=2).run(suite)
