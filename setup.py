# Setup file for the gsscrape package.

import setuptools

# setup details
setuptools.setup(
    name="gsscrape",
    version="0.1",
    author="Carlos Sánchez Muñoz",
    description="A package to scrape your papers from Google Scholar",
    packages=setuptools.find_packages(where='src'),
    install_requires=[
        "pandas",
        "jupyter",      
        "selenium===4.27.1"
    ],
    python_requires=">=3.9",
)