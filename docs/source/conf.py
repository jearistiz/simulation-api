# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

import sphinx_rtd_theme

sys.path.insert(0, os.path.abspath('../../'))


# -- Project information -----------------------------------------------------

project = 'Simulation FastAPI'
copyright = '2020, Juan E. Aristizabal'
author = 'Juan E. Aristizabal'

# The full version, including alpha/beta/rc tags
release = '0.0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

autodoc_default_options = {
    'members': True,
    'private-members': '_api_simulation_request, '
                       '_create_pickle_path_disk, '
                       '_create_plot_path_disk, '
                       '_pickle, _plot_solution, '
                       '_run_simulation, '
                       '_sim_form_to_sim_request, '
                       '_create_user, '
                       '_get_username, '
                       '_create_simulation, '
                       '_get_simulation, '
                       '_get_all_simulations, '
                       '_create_plot_query_values, '
                       '_get_plot_query_values, '
                       '_create_parameters, '
                       '_get_parameters',
    'special-members': '__init__',
    'inherited-members': False,
    'show-inheritance': False,
}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme =  "sphinx_rtd_theme"  # 'classic' # 'sphinx_material'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']