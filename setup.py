from setuptools import setup

setup(
    name='realms',
    version='0.0.0',
    license='MIT',
    author='Zach Mitchell',
    author_email='zmitchell@fastmail.com',
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'realms = realms.__main__:main'
        ]
    }
)
