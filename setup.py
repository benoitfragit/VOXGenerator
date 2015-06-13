from distutils.core import setup
setup(
    name = 'voxgenerator',
    packages = ['voxgenerator',
                'voxgenerator.core',
                'voxgenerator.plugin',
                'voxgenerator.pipeline',
                'voxgenerator.generator',
                'voxgenerator.service'],
    version = '1.0.1',
    description = 'Vox generator',
    author = 'Benoit Franquet',
    author_email = 'benoitfraubuntu@gmail.com',
    scripts = ['run_voxgenerator.py', 'run_voxgenerator']
)
