import setuptools


setuptools.setup(
    name='onelogin_aws_cli',
    packages=['onelogin_aws_cli'],
    version='0.1.7',

    description='Onelogin assume AWS role through CLI',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Security'
    ],
    keywords='onelogin aws cli',
    author='Cameron Marlow',
    author_email='cameron@physera.com',
    url='https://github.com/physera/onelogin-aws-cli',
    download_url='https://github.com/physera/onelogin-aws-cli/archive/0.1.7.tar.gz',  # noqa: E501
    py_modules=['onelogin_aws_cli'],
    install_requires=[
        'boto3',
        'requests'
    ],
    license='MIT License',
    entry_points={
        "console_scripts": ["onelogin-aws-login = onelogin_aws_cli.main:main"]
    },
    test_suite='nose.collector',
    tests_require=['nose', 'nose-cover3'],
    zip_safe=False,
)
