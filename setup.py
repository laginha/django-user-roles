from setuptools import setup, find_packages

setup(
    name             = 'custom-user-roles',
    version          = '1.1.0',
    # original author = 'Tom Christie'
    # original author_email  = 'tom@tomchristie.com'
    author           = "Diogo Laginha",
    author_email     = "diogo.laginha.machado@gmail.com",
    url              = 'https://github.com/laginha/django-user-roles',
    description      = "Simple role-based user permissions for Django.",
    packages         = find_packages(where='src'),
    package_dir      = {'': 'src'},
    install_requires = ['django', 'milkman'],
    extras_require   = {},
    zip_safe         = False,
    license          = 'MIT',
    classifiers      = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Intended Audience :: Developers',
    ]
)

