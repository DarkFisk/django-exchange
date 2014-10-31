from setuptools import setup, find_packages

setup(
    name='django-exchange',
    packages=find_packages(),
    version='0.1.2',
    description='currency, historical exchange rates and conversions support for django',
    author='DarkFisk',
    author_email='darkfisk@gmail.com',
    url='https://github.com/DarkFisk/django-exchange',
    requires=[
        "py-moneyed>0.4"
    ]
)
