Installing Django
- Set up a virtual env https://docs.djangoproject.com/en/4.2/howto/windows/#setting-up-a-virtual-environment

py -m venv project-name
project-name\Scripts\Activate.ps1
py -m pip install Django
py -m pip install colorama
django-admin startproject mysite


Cool points about Django...
- Opinionated about organization
- In a way that encourages bounded contexts
- Helps avoid ENTROPY!

Left of here...
- https://docs.djangoproject.com/en/4.2/intro/tutorial02/