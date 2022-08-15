from setuptools import find_packages, setup


setup(
    name="project-util",
    version="0.0.31",
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
        "vidutil @ git+https://github.com" "/etsuko-io/vidutil.git#egg=vidutil-0.0.6",
        "loguru==0.6.0",
        "boto3>=1.24.32,<2.0.0",
        "python-dotenv>=0.20.0,<1.0.0",
    ],
)
