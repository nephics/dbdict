from distutils.core import setup

setup(name='dbdict',
      description='A dictionary-like object with SQLite backend',
      author='Jacob Svensson',
      author_email='jacob@nephics.com',
      url='https://github.com/nephics/dbdict',
      version='2.0',
      py_modules=['dbdict'],
      long_description=open('README.md').read(),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Database'])
