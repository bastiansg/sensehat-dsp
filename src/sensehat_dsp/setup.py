from setuptools import find_packages, setup

setup(
    name="sensehat_dsp",
    packages=find_packages(),
    version="1.0.0",
    install_requires=[
        "requests==2.28.2",
        "rich==13.3.3",
        "more-itertools==9.1.0",
        "Pillow==9.5.0",
        "opencv-contrib-python-headless==4.7.0.72",
    ],
    package_data={"": ["*.yml", "*.yaml"]},
    include_package_data=True,
    classifiers=["Programming Language :: Python :: 3"],
)
