from setuptools import setup, find_packages, Extension

module1 = Extension(
    name = 'foopackage.foomodule',
    sources = ['foopackage/foomodule.c']
)

setup (
    name = 'TemplatePackage',
    version = '1.8',
    description = 'This is a template package that uses a C extension',
    package_data = {
        'foopackage': ['data.txt']
    },
    packages = find_packages(),
    ext_modules = [module1],
)
