import setuptools

from wagtail_opengraph_image_generator import get_version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wagtail-opengraph-image-generator",
    version=get_version(),
    author="Candylabs GmbH",
    author_email="info@candylabs.de",
    description="Wagtail addon to assist in creating Open Graph images for your pages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/candylabshq/wagtail-opengraph-image-generator",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Framework :: Wagtail",
    ],
    install_requires=[
        "wagtail>=4.0,<5.0",
        "CairoSVG==2.7.0",
        "Pillow==9.5.0",
    ],
    tests_require=[
        "pytest",
        "pytest-pythonpath",
        "pytest-django",
        "pytest-factoryboy",
        "psycopg2>=2.5.4",
    ],
    extras_require={"doc": ["mkdocs", "markdown-include"]},
    python_requires=">=3.7",
    include_package_data=True,
)
