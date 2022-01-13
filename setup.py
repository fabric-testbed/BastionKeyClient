import setuptools
from bastion_key_client import __VERSION__

with open("README.md", "r") as fh:
  long_description = fh.read()

with open("requirements.txt", "r") as fh:
  requirements = fh.read()

setuptools.setup(
  name="bastion_key_client",
  version=__VERSION__,
  author="Ilya Baldin, Mert Cevik, Michael Stealey",
  description="FABRIC Bastion host key rotation utility",
  url="https://github.com/fabric-testbed/BastionKeyClient",
  long_description="FABRIC Bastion host key rotation utility",
  long_description_content_type="text/plain",
  packages=setuptools.find_packages(),
  include_package_data=True,
  scripts=['utilities/update_bastion_keys.py'],
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires=">=3.6",
  install_requires=requirements,
  setup_requires=requirements,
)
