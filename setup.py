import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="target365-sdk",
    version="0.0.1",
    author="Target365",
    author_email="author@example.com",
    description="This client library enables working with the Target365 online services which includes address lookup, sending and receiving text messages and more.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/target365/target365-sdk-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)