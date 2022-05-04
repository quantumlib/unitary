Unitary
======

The Unitary library's API intends to provide common operations that enable a programmer to add behavior to their game mechanic, or game objects, based on the core principles of Quantum Information Science (QIS): Superposition, Entanglement, Interference, and Measurement.

While the library can be used for other purposes, the Unitary library is designed for game developers. The library is an extension of Google's Cirq library, which enables people to specify circuits for quantum computing.

This repository also contains several reference applications, such as Quantum Chess, which can be
found in the `quantum_chess` directory.


## Installation and Documentation

Unitary is not available as a PyPI package. Please clone this repository and
install from source:

    cd unitary/
    pip install .

Documentation is available at https://quantumai.google/cirq/experiments.

## Checking out for development

Note: before committing, you will need to sign a [Contributor License
Agreement (CLA)](https://opensource.google/documentation/reference/cla/github).

Please fork the repository (for instance, by using the button in the
upper right corner).  

You can then clone the repository into your development environment by
using (substitute USER with your github username)

git clone https://github.com/USER/unitary.git
git remote add upstream https://github.com/quantumlib/unitary.git

This will clone your fork so that you can work on it, while marking the
name 'upstream' as the original repository.

You can then pull from the original and update your fork, for instance,
by doing this:

git pull upstream main
git push origin main

In order to push changes to unitary, create a branch in your fork:

git checkout -b BRANCH_NAME

Perform your changes, then commit (i.e. `git commit -a`) then push to your
fork:

git push origin BRANCH_NAME

This will give you a link to create a PR (pull request).  Create this pull request
and pick some reviewers.  Once approved, it will be merged into the original repository.

Thanks for contributing!


## See Also

This code leverages [Cirq](https://github.com/quantumlib/Cirq) as a
quantum programming language and SDK.

Unitary is not an official Google product. Copyright 2022 Google.

