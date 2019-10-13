import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='tagazoo',
    version='1.0',
    author="Tagazoo-dev",
    author_email="dev@tagazoo.com",
    description="Client to use the Tagazoo API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tagazoo/py-tagazoo",
    packages=setuptools.find_packages(exclude=("tests",)),
    classifiers=[
        "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests'
    ],
)
