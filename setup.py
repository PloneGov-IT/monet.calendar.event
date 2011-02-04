from setuptools import setup, find_packages
import os

version = '0.2.0dev'

setup(name='monet.calendar.event',
      version=version,
      description="An advanced Event type for Plone with additional date fields and features for appointments",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        "Programming Language :: Python",
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      author='RedTurtle Technology',
      author_email='sviluppoplone@redturtle.net',
      url='http://plone.comune.modena.it/svn/monet/monet.calendar.event',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['monet', 'monet.calendar'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'monet.recurring_event',
          'rt.calendarinandout',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
