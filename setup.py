import setuptools

setuptools.setup(name='algebraic_moments',
      version='0.1',
      description='',
      author='Allen Wang',
      author_email='allenw@mit.edu',
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires=[
          'sympy', 'numpy', 'networkx'
      ]
      )