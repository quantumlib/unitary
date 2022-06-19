# Copyright 2020 Google
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import re
import shutil
import subprocess

project = 'Unitary'
copyright = '2020, Google Quantum'
author = 'Google Quantum'

extensions = [
    'nbsphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'recommonmark',
]

nbsphinx_allow_errors = False
nbsphinx_timeout = -1  # no timeout
autosummary_generate = True

# Certain notebooks are saved pre-executed. Keeping this environment variable
# as "auto" prevents re-executing (which takes time!). The CI will
# not re-execute these notebooks.
# Set this to "always" to execute all notebooks.
# https://github.com/quantumlib/ReCirq/issues/15
nbsphinx_execute = os.environ.get(
    'NBSPHINX_EXECUTE_NOTEBOOKS', 'auto')  # can also be "always" or "never".

napoleon_google_docstring = True
napoleon_numpy_docstring = False

add_module_names = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store',
                    '**.ipynb_checkpoints', 'appengine']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_css_files = [
    'custom.css',
]

html_favicon = 'favicon.ico'
#html_logo = '_static/recirq_logo_notext.png'


def _rmtree_if_exists(dirname):
    if os.path.exists(dirname):
        shutil.rmtree(dirname)


def env_before_read_docs(app, env, docnames):
    """Re-order `docnames` to respect the execution-order dependency
    of notebooks.
    """
    print("The following documents will be built:")
    print(docnames)

    def _order(docname):
        if docname == 'tutorials/data_collection':
            # must come before others
            return -1
        return 0

    docnames.sort(key=_order)

    print("Since there are dependencies between them, they will be built in this order:")
    print(docnames)

    if ('tutorials/data_collection' in docnames
            and 'tutorials/data_analysis' not in docnames):
        print("Since tutorials/data_collection has changed, "
              "also re-running tutorials/data_analysis")
        docnames.append('tutorials/data_analysis')

    print(docnames)

REPO_DIR = subprocess.Popen(['git', 'rev-parse', '--show-toplevel'],
                            stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')


def source_read(app, docname, source):
    source[0] = re.sub(r'"##### (Copyright 20\d\d Google)"', r'"**\1**"', source[0])


def setup(app):
    FROM = f'{REPO_DIR}/docs/quantum_chess'
    TO = f'{REPO_DIR}/dev_tools/docs/sphinx'
    shutil.copy(f'{FROM}/images/*.png', f'{TO}/_static/')
    #shutil.copy(f'{FROM}/images/recirq_logo_notext.png', f'{TO}/_static/')

    app.connect('env-before-read-docs', env_before_read_docs)
    app.connect('source-read', source_read)
