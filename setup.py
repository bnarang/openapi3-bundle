from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()
setup(
    name="openapi3-bundle",
    version="0.1.0",
    author="Bhupinder S Narang",
    author_email="narang.bhupinder@gmail.com",
    license="GNU GPLv3",
    description="Combines multi-openAPI Spec and produce a single API Spec with internal references",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bnarang/openapi3-bundle",
    packages=find_packages(),
    install_requires=[requirements],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    entry_points="""
        [console_scripts]
        openapi3-bundle=main:main
    """,
)
