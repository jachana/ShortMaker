from setuptools import setup, find_packages

setup(
    name="shortmaker",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'moviepy>=1.0.3',
        'Pillow>=9.0.0',
        'numpy>=1.21.0',
        'gTTS>=2.3.1',
    ],
)
