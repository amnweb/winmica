import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="winmica",
    version="1.0.0",
    author="AmN",
    description="Windows 11 Mica backdrop effects using official Windows API",
    long_description="Windows Mica is a modern backdrop effect introduced in Windows 11, providing a translucent and blurred background for applications. This package allows developers to easily integrate Mica effects into their Python applications using the official Windows API.",
    long_description_content_type="text/markdown",
    url="https://github.com/amnweb/winmica",
    project_urls={
        "Bug Tracker": "https://github.com/amnweb/winmica/issues",
    },
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows :: Windows 11",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.12",
)
