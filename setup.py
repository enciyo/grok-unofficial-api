from setuptools import setup, find_packages

setup(
    name='grok_unoffical_api',
    version='0.1.1',
    description='Unofficial Grok API',
    author='Mustafa K',
    author_email='ben@mustafakilic.dev',
    url= "https://github.com/enciyo/grok-unofficial-api",
    packages=find_packages(),
    install_requires=[
        'requests',
        'python-dotenv'
    ],
)
