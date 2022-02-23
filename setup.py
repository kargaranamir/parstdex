import setuptools

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open("README.md") as fh:
    long_description = fh.read()


setuptools.setup(
    name='parstdex',
    version="0.1.4",
    description="Pars Time Date Extractor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        'License :: OSI Approved :: Apache-2.0 License ',
        "Programming Language :: Python :: 3.8.8",
        "Topic :: Natural Language Processing :: Time Date Marker Extractor"
    ],
    install_requires=required,
    author='ASH Group',
    author_email='kargaran.amir@gmail.com'
 )
