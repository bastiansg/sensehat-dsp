from setuptools import find_packages, setup

setup(
    name="sensehat_dsp",
    packages=find_packages(),
    version="1.0.0",
    install_requires=[
        "rich==13.3.5",
        "pydantic==1.10.7",
    ],
    package_data={"": ["*.yml", "*.yaml"]},
    include_package_data=True,
    classifiers=["Programming Language :: Python :: 3"],
)
