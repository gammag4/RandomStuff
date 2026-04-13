from setuptools import find_packages, setup

package_name = 'pubsub_example_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='gabriel',
    maintainer_email='41156120+gammag4@users.noreply.github.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            # Added
            #'node_name = package_name.module_name:main_func',
            'pub_example = pubsub_example_py.pub_example:main',
            'sub_example = pubsub_example_py.sub_example:main'
            # End added
        ],
    },
)
