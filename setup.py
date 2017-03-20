import setuptools


setuptools.setup(
    name='onelogin-aws-cli',
    version='1.0.0',
    description='Onelogin assume AWS role through CLI',
    long_description=open('README.md').read().strip(),
    author='Cameron Marlow',
    author_email='cameron@healthcoda.com',
    url='https://github.com/healthcoda/onelogin-aws-cli',
    py_modules=['onelogin-aws-cli'],
    install_requires=['requests', 'boto3'],
    license='MIT License',
    zip_safe=False,
    keywords='onelogin aws cli',
    classifiers=['Packages', 'Boilerplate']
)
