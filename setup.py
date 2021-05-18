from setuptools import setup, find_packages

setup(
    name='django_neomodel',
    version='0.0.7',
    description='Use Neo4j with Django!',
    long_description=open('README.rst').read(),
    author='Robin Edwards',
    author_email='robin.ge@gmail.com',
    zip_safe=True,
    url='http://github.com/robinedwards/django-neomodel',
    license='MIT',
    packages=find_packages(exclude=('tests',)),
    keywords='neo4j django plugin neomodel',
    install_requires=['neomodel>=4.0.3', 'pytz>=2020.1', 'django>=2.2'],
    tests_require=['pytest-django>=3.10.0'],
    classifiers=[
        "Development Status :: 4 - Beta",
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        # With (3.9) warnings on Shapely install on neobolt repo
        "Programming Language :: Python :: 3.9",
        "Topic :: Database",
    ])
