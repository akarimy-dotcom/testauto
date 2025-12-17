from setuptools import setup, find_packages

setup(
    name='pymtstestlib',
    version='00.00.06',
    packages=find_packages(include=['pymtstestlib', 'pymtstestlib.*']),
    description='Python MTSTestLib library porting',
    author='Luca Santini Phoenix S.c.p.a',
    author_email='luca.santini@phonenix-factory.it',
    install_requires=[
        'pyserial>=3.0',
    ],
    package_data={
        "pymtstestlib": [
            "Env Galileo/*",
            "Env Evo/*",
            "Env EvoIII/*"
        ]
    }
)
