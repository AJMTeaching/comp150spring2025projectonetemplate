from setuptools import setup, find_packages

setup(
    name="adventure-game",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'adventure-game=adventure_game.src.main:start_game',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A text-based adventure game with Game of Thrones themes",
    keywords="game, adventure, text-based, game-of-thrones",
    url="https://github.com/yourusername/adventure-game",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment",
    ],
)
#!/usr/bin/env python3
\