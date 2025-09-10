from setuptools import setup, find_packages

setup(
    name="smart-retry",
    version="0.1.0",
    description="A simple retry decorator with backoff, conditions, and logging",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
