import setuptools

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name='parstdex',
    version="1.0.9",
    description="Persian time and date marker extractor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/kargaranamir/parstdex',
    packages=setuptools.find_packages(),
    package_data={
        'parstdex.utils': ['pattern/*.txt',
                           'annotation/ax/*.txt',
                           'annotation/adv/*.txt',
                           'annotation/date/*.txt',
                           'annotation/time/*.txt',
                           'special_words/*.txt'],
        'tests': ['data.json']
    },
    include_package_data=True,
    classifiers=[
        'Topic :: Text Processing',
        'Natural Language :: Persian',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License'
    ],
    install_requires=required,
    author='Amir Hossein Kargaran, Sajad Mirzababaei',
    author_email='kargaranamir@gmail.com, ss.mirzababaei@gmail.com'
)
