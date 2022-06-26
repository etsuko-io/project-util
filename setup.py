from setuptools import find_packages, setup

setup(
    name="project-util",
    version="0.0.15",
    packages=find_packages(
        where="src",
    ),
    package_dir={"": "src"},
    package_data={"": ["ml-models", "ml-models/*"]},
    include_package_data=True,
    install_requires=[
        "numpy==1.22.4",
        "opencv-contrib-python==4.5.5.64",
        "Pillow==9.1.1",
        "black==22.3.0",
        "vidutil @ git+https://github.com/etsuko-io/vidutil.git#egg=vidutil-0.0.3",
        "loguru==0.6.0",
    ],
)
