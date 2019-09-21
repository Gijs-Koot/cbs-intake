import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

reqs = (HERE / "requirements.txt").read_text().splitlines()

setup(
    name="cbs_intake",
    version="0.0.1",
    description="Build a CBS catalog and download data directly into dataframes.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Gijs Koot",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["cbs_intake"],
    include_package_data=True,
    install_requires=reqs,
    entry_points={
        'intake.drivers': [
            'cbs_odata = cbs_intake.ds:CBSODataSource'
        ]
    },
)