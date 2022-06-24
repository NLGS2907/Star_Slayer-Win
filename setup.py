"""
Setup the package.
"""

from setuptools import setup, find_packages

with open("README.md", mode='r', encoding="utf-8") as readme:

    project_description = readme.read()

setup(

    name="star-slayer",

    packages=find_packages(),

    package_data={

        "starslayer" : ["json/actions/*.json",
                        "json/profiles/*.json",
                        "json/scores/*.json",

                        "textures/icon/*.gif",
                        "textures/player/star_slayer/*.customppm",
                        "textures/player/star_slayer_damaged/*.customppm",
                        "textures/player/bilby_tanka/*.customppm",
                        "textures/player/bilby_tanka_damaged/*.customppm",
                        "textures/player/viper_dodger/*.customppm",
                        "textures/player/viper_dodger_damaged/*.customppm",

                        "textures/player/shield/*.customppm",
                        "textures/player/cannon/*.customppm",

                        "textures/drops/med_kit/*.customppm",
                        "textures/drops/radial_bomb/*.customppm",
                        "textures/drops/spiral_bomb/*.customppm",

                        "textures/enemies/common_a/*.customppm",
                        "textures/enemies/common_b/*.customppm",
                        "textures/enemies/swift/*.customppm",

                        "sfx/time/*.wav",
                        "sfx/cheats/*.wav",
                        "sfx/settings/*.wav",
                        "sfx/gameplay/*.wav"]
    },

    version="0.2.1-alpha",

    url="https://github.com/NLGS2907/star-slayer",

    author="NLGS",

    author_email="flighterman@fi.uba.ar",

    license="MIT",

    description="Little game made with Gamelib",

    long_description=project_description,

    long_description_content_type="text/markdown",

    classifiers=[

        "Development Status :: 3 - Alpha",

        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python :: 3.10"
    ]
)
