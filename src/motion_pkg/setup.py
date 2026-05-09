from setuptools import setup

package_name = 'motion_pkg'
setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    install_requires=['setuptools'],
    entry_points={
        'console_scripts': [
            'moveit_node = motion_pkg.moveit_node:main',
        ],
    },
)
