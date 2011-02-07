from distutils.core import setup


setup(name="django-mcms",
      version="1.0",
      description="A simple CMS!",
      author="sree",
      author_email="sree@mahiti.org",
      packages=["mcms"],
      package_dir={"mcms": "mcms"},
      package_data = {"mcms": ["locale/*/LC_MESSAGES/django.*", "templates/project/*.html"]},
      classifiers=["Development Status :: 5 - Production/Stable",
                   "Environment :: Web Environment",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: GPL License",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Framework :: Django",])
