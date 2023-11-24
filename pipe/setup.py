from setuptools import find_packages, setup

setup(
    name="lotr_data_pipe",
    packages=find_packages(exclude=["lotr_data_pipe_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
