from setuptools import setup, find_packages

setup(
    name='graphier',
    version='0.0.0.1',
    description="This library aims to visualize relationships among a large amount of variables via graph-based approach",
    author='Keonho Kim',
    author_email='keonhok0315@gmail.com',
    url='https://github.com/keonho-kim/graphy',
    install_requires=['pandas', 'numpy', 'networkx', 'scipy', 'scikit-learn', 'matplotlib'],
    packages=find_packages(exclude=[]),
    python_requires='>=3.7',
    zip_safe=False,
    entry_points={
        "console_scripts":
            [
             "graphy = graphy.main:main"   
            ]
    },
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    package_data={},
    include_package_data=True
)

