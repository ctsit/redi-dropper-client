"""
Setup
"""

from setuptools import setup, find_packages

setup(
    name='redidropper',
    version='0.0.1',
    author='https://www.ctsi.ufl.edu/research/study-development/informatics-consulting/',
    author_email='ctsit@ctsi.ufl.edu',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    package_data={
    },
    url='https://github.com/ctsit/redi-dropper-client',
    download_url = 'https://github.com/ctsit/redi-dropper-client/releases/',
    keywords = ['MRI','Flask'],
    license='BSD 3-Clause',
    description='MRI File Uploader',
    long_description=open('README.rst').read(),
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'redidropper = run:main',
        ],
    },
    #test_suite='tests.testSuite',
    tests_require=[
        #"mock >= 1.0.1",
    ],
    setup_requires=[
        "nose >= 1.0",
        "nosexcover >= 1.0.10",
    ],
)
