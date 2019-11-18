## Target365 SDK for Python
[![License](https://img.shields.io/github/license/Target365/sdk-for-python.svg?style=flat)](https://opensource.org/licenses/MIT)

### Getting started
To get started please send us an email at <support@target365.no> containing your EC public key in DER(ANS.1) format.
If you want, you can generate your EC public/private key-pair here: <https://8gwifi.org/sshfunctions.jsp>.

Check out our [Python User Guide](USERGUIDE.md)

### PIP
```
pip install target365-sdk
```
[![pypi version](https://img.shields.io/pypi/v/target365_sdk.svg)](https://pypi.org/project/target365-sdk/)
[![python_platform](https://img.shields.io/pypi/pyversions/target365_sdk.svg)](https://pypi.org/project/target365-sdk/)

### Test Environment
Our test-environment acts as a sandbox that simulates the real API as closely as possible. This can be used to get familiar with the service before going to production. Please be ware that the simulation isn't perfect and must not be taken to have 100% fidelity.

#### Url: https://test.target365.io/

### Production Environment
Our production environment is a mix of per-tenant isolated environments and a shared common environment. Contact <support@target365.no> if you're interested in an isolated per-tenant environment.

#### Url: https://shared.target365.io/

### Authors and maintainers
Target365 (<support@target365.no>)

### Issues / Bugs / Questions
Please feel free to raise an issue against this repository if you have any questions or problems.

### Contributing
New contributors to this project are welcome. If you are interested in contributing please
send an email to support@target365.no.

### License
This library is released under the MIT license.
