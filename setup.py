from setuptools import setup, find_packages
dev_requires = ['pytest == 4.0.1']
requires = [
    'flask-jwt-extended == 3.13.1',
    'flask-marshmallow == 0.9.0',
    'flask == 2.3.2',
    'flask-restful == 0.3.6',
    'marshmallow == 2.16.3',
    'passlib == 1.7.1',
    'Flask-Migrate==2.3.1',
    'Flask-SQLAlchemy==2.3.2',
    'marshmallow-sqlalchemy == 0.15.0',
    'psycopg2-binary == 2.7.6.1'
]


setup(
    name="contacts",
    version="0.1",
    author='Sreenadh TC',
    author_email="kesav.tc8@gmail.com",
    description="Contacts",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    tests_require=dev_requires,
    # run `make requirements.txt` after editing
    install_requires=requires,
    extras_require={
        'dev': dev_requires
    }
)
