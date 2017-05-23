.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/zmitchell/realms/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
and "help wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

realms could always use more documentation, whether as part of the
official realms docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/zmitchell/realms/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Development Environment
-----------------------

There are issues using Anaconda Python distributions with tox, a popular testing package used to develop this package, so you will need to install Python 3 some other way. This project requires Python 3.6 or later. The repositories included with most Linux distributions will be out of date, so it's likely that you'll have to obtain Python some other way. If you're running Windows, just download Python from the Python website.

Get Started!
------------

Ready to contribute? Here's how to set up ``realms`` for local development.

1. Fork the ``realms`` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/realms.git

3. Install your local copy into a virtualenv. If you haven't already done so, install virtualenvwrapper, as it makes dealing with Python virtualenv's much easier. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv realms
    $ cd realms/
    $ pip install -r requirements_dev.txt

4. Make changes to your code.
5. When you're done making changes, check that your changes pass flake8 and the tests. Both flake8 and tox are installed as dependencies in the previous step. Running ``tox`` will run the tests and flake8 against your changes::

    $ tox

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated.
3. Check https://travis-ci.org/zmitchell/realms/pull_requests to make sure that your pull request builds successfully.

Documentation
-------------

Any new code that you submit should include documentation in the form of docstrings. The docstrings used here follow the NumPy format, which you can read about in `this guide <https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt>`_. Type annotations in function declarations are preferred to indicating types in the docstring.

Tips
----

To run a subset of tests::

$ pytest tests/file_containing_tests.py

To run the application::

$ python -m realms

