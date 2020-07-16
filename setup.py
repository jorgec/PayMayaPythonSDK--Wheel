import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='PayMayaPythonSDK',
    version='0.3',
    scripts=[],
    author="Jorge Cosgayon",
    author_email="jorge.cosgayon@gmail.com",
    description="A Python port of the PHP PayMaya SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jorgec/PayMayaPythonSDK--Wheel",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
