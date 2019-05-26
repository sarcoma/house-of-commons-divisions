from setuptools import setup, find_packages

setup(
    name='commons_divisions',
    version='0.1.0',
    url='https://github.com/sarcoma/house-of-commons-divisions',
    author='Sarcoma',
    author_email='sean@orderandchaoscreative.com',
    description='API of House of Commons Divisions',
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4==4.7.1",
        "Flask==1.0.2",
        "Flask-Cors==3.0.7",
        "Flask-SQLAlchemy==2.4.0",
        "lxml==4.3.3",
        "requests==2.21.0",
        "soupsieve==1.9",
        "SQLAlchemy==1.3.2",
    ],
)
