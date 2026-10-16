from setuptools import find_packages, setup

package_name = 'vehicle_speed_monitor'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    package_data={'': ['py.typed']},
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='vamsi',
    maintainer_email='vamsi@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    
entry_points={
    'console_scripts': [
        'speed_sensor = vehicle_speed_monitor.speed_sensor:main',
        'speed_monitor = vehicle_speed_monitor.speed_monitor:main',
        'vehicle_model = vehicle_speed_monitor.vehicle_model:main',
        'speed_controller = vehicle_speed_monitor.speed_controller:main',
    ],
},
)
