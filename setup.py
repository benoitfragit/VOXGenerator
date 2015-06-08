from distutils.core import setup
setup(
    name = 'voxgenerator',
    packages = ['pipeline', 'plugin', 'core', 'generator'],
    version = '1.0.0',
    description = 'Vox generator',
    author = 'Benoit Franquet',
    author_email = 'benoitfraubuntu@gmail.com',
    scripts = ['run_voxgenerator.py', 'run_voxgenerator']
)
