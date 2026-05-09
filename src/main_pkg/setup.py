from setuptools import setup

package_name = 'main_pkg'
setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    install_requires=['setuptools'],
    entry_points={
        'console_scripts': [
            'main_node = main_pkg.main_node:main',
        ],
    },
)
