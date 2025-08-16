from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyfastmem",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A fast and secure memory storage library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pyfastmem",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.7",
    install_requires=[
        'cryptography>=3.4.7',
        'click>=8.0.1',
    ],
    entry_points={
        'console_scripts': [
            'pyfastmem=pyfastmem.cli:main',
        ],
    },
    keywords='memory storage security encryption',
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/pyfastmem/issues',
        'Source': 'https://github.com/yourusername/pyfastmem',
    },
)
