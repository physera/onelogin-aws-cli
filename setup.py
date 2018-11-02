import setuptools

PACKAGE_NAME = 'onelogin_aws_cli'
VERSION = '0.1.16'

setuptools.setup(
    name=PACKAGE_NAME,
    packages=[PACKAGE_NAME],
    version=VERSION,
    python_requires='>=3',
    description='Onelogin assume AWS role through CLI',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Security',
        'Topic :: System :: Systems Administration :: Authentication/Directory'
    ],
    keywords='onelogin aws cli',
    author='Cameron Marlow',
    author_email='cameron@physera.com',
    url='https://github.com/physera/onelogin-aws-cli',
    download_url=(
            'https://github.com/physera/onelogin-aws-cli/archive/' +
            VERSION +
            '.tar.gz'
    ),
    py_modules=[PACKAGE_NAME],
    install_requires=[
        'boto3',
        'onelogin',
        'keyring',
        'ipify',
    ],
    setup_requires=['nose>=1.0'],
    entry_points={
        "console_scripts": [
            "onelogin-aws-login = {pkg}.cli:login".format(pkg=PACKAGE_NAME)
        ]
    },
    license='MIT License',
    test_suite='nose.collector',
    tests_require=['coverage', 'nose', 'nose-cover3'],
    zip_safe=False,
)
