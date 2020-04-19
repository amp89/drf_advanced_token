from setuptools import (
    setup,
    find_packages,
)



setup(
    name='django-drf_advanced_token',
    version='2.0.0',
    url='https://github.com/amp89/drf_advanced_token',
    download_url="https://github.com/amp89/drf_advanced_token/archive/2.0.0.tar.gz",
    license='MIT',
    description='More advanced features for the Django Rest Framework rest_framework.authtoken app',
    long_description=open('README.rst', 'r', encoding='utf-8').read(),
    author='Alex Peterson',
    author_email='contact@alexpeterson.tech',
    install_requires=[
        'django',
        'djangorestframework',
    ],
    python_requires='>=3.6',
    
)