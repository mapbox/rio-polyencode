from codecs import open as codecs_open
from setuptools import setup, find_packages


# Parse the version from the fiona module.
with open('rio_polyencode/__init__.py') as f:
    for line in f:
        if line.find("__version__") >= 0:
            version = line.split("=")[1].strip()
            version = version.strip('"')
            version = version.strip("'")
            break

# Get the long description from the relevant file
with codecs_open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(name='rio-polyencode',
      version=version,
      description=u"Encode / decode time series data into polynomials",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author=u"Damon Burgett",
      author_email='damon@mapbox.com',
      url='https://github.com/mapbox/rio-polyencode',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'click',
          'rasterio'
      ],
      extras_require={
          'test': ['pytest'],
      },
      entry_points="""
      [rasterio.rio_plugins]
      polyencode=rio_polyencode.scripts.cli:polyencode
      polydecode=rio_polyencode.scripts.cli:polydecode
      """ )
