import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="monopoly_simulator-balloch", # Replace with your own username
    version="0.0.1",
    author="Mayank Kejriwal",
    author_email="kejriwal@isi.edu",
    description="A novelty-injection-capable implementation of Monopoly",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/balloch/GNOME-p3",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
