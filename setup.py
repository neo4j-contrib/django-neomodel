from setuptools import setup, find_packages

setup(
    name='django_neomodel',
    version='0.0.4',
    description='Use Neo4j with Django!',
    long_description=open('README.rst').read(),
    author='Robin Edwards',
    author_email='robin.ge@gmail.com',
    zip_safe=True,
    url='http://github.com/robinedwards/django-neomodel',
    license='MIT',
    packages=find_packages(exclude=('tests',)),
    keywords='neo4j django plugin neomodel',
    install_requires=['neomodel>=3.2.5', 'django>=1.9'],
    classifiers=[
        "Development Status :: 4 - Beta",
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Database",
    ])
