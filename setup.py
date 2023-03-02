from setuptools import setup, find_packages

setup(
    name="graphy",
    version="0.0.1",
    description="This library aims to visualize relationships among a large amount of variables with graph-based approach",
    author="Keonho Kim",
    author_email="keonhok0315@gmail.com",
    url='https://github.com/keonho-kim/graphy',
    python_requires=">=3.8",
    packages=find_packages(),
    install_requires=['pandas', 'numpy', 'networkx', 'scipy', 'matplotlib'],
    zip_safe=False,
    entry_points={
        "console_scripts":
            [
             "graphy = graphy.main:main"   
            ]
    },
    package_data={},
    include_package_data=True
)