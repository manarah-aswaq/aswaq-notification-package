from setuptools import setup

setup(name='aswaq_notifications',
      version='0.1.2',
      description='A python wrapper around aswaq notifications layer handler API',
      url='',
      author='AHMADIGA',
      author_email='abazadough@aswaq.com',
      license='MIT',
      packages=['aswaq_notifications'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
