from setuptools import find_packages, setup

package_name = 'ros_serial_input'

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
    maintainer='jasper',
    maintainer_email='jasper@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "serial_publisher = ros_serial_input.serial_publisher:main",
            "serial_subscriber = ros_serial_input.serial_subscriber:main"
        ],
    },
)
