from setuptools import setup, find_packages

setup(
    name="got-adventure",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    package_data={
        'project_code': ['location_events/*.json', 'travel_events/*.json'],
    },
    entry_points={
        'console_scripts': [
            'got-adventure=project_code.src.main:start_game',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A text-based adventure game with Game of Thrones themes",
    keywords="game, adventure, text-based, game-of-thrones",
    url="https://github.com/yourusername/got-adventure",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment",
    ],
    python_requires='>=3.12.6',
)
