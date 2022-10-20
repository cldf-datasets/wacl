from setuptools import setup
import json


with open("metadata.json", encoding="utf-8") as fp:
    metadata = json.load(fp)


setup(
    name='cldfbench_wacl',
    description=metadata["title"],
    license=metadata.get("license", ""),
    url=metadata.get("url", ""),
    py_modules=['cldfbench_wacl'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'cldfbench>=1.2.2',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
