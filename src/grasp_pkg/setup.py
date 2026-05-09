from setuptools import setup

package_name = 'grasp_pkg'
setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    install_requires=['setuptools'],
    entry_points={
        'console_scripts': [
            'hardness_node = grasp_pkg.hardness_node:main',
        ],
    },
)
