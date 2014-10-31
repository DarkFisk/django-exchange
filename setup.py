from setuptools import setup, find_packages

setup(
    name='django-exchange',
    packages=find_packages(),
    version='0.1.3',
    description='currency, historical exchange rates and conversions support for django',
    author='DarkFisk',
    author_email='darkfisk@gmail.com',
    url='https://github.com/DarkFisk/django-exchange',
    install_requires=['setuptools',
                      'py-moneyed > 0.4']
)
