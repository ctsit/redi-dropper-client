"""
RediDropperClient
"""

import setuptools

setuptools.setup(
    name='redi-dropper-client',
    version='0.0.2',
    description='Flask web application for uploading MRI images',
    # long_description=open('README.md').read(),
    author='CTS-IT at University of Florida',
    author_email='ctsit@ctsi.ufl.edu',
    url='https://github.com/ctsit/redi-deopper-client',
    license='BSD 3 ',
    keywords=[
        "image storage"
        "flask",
        "mri",
        "ehr",
        "emr",
        "medical",
    ],
    setup_requires=[
        "SQLAlchemy         >= 1.0.0",
        "Flask              >= 0.10.1",
        "Flask-Login        >= 0.2.11",
        "Flask-Mail         >= 0.9.1",
        "Flask-Principal    >= 0.4.0",
        "Flask-SQLAlchemy   >= 2.0",
        "Flask-WTF          >= 0.10.2",
        "MySQL-python       >= 1.2.5",
        "WTForms            >= 2.0.2",
        "pytz               >= 2015.4",
    ],
)
