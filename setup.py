from setuptools import setup, find_packages

install_requires = []
description = ''

for file_ in ('README', 'CHANGELOG'):
    with open('%s.md' % file_) as f:
        description += f.read() + '\n\n'


classifiers = [
            'Environment :: Web Environment',
            'Framework :: Django',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Software Development :: Libraries :: Python Modules']


setup(name='django-multiple-auth',
      version="1.0",
      url='https://github.com/EngageSports/django-multiple-auth',
      packages=find_packages(),
      long_description=description.strip(),
      description=("Multiple login users at the same time"),
      author="Martyn CLEMENT",
      author_email="martyn@engage-sports.com",
      include_package_data=True,
      zip_safe=False,
      classifiers=classifiers,
      install_requires=install_requires,
      )