from distutils.core import setup
setup(
    name = 'voxgenerator',
    packages = ['voxgenerator',
                'voxgenerator.core',
                'voxgenerator.plugin',
                'voxgenerator.pipeline',
                'voxgenerator.generator',
                'voxgenerator.service'],
    version = '1.0.2',
    description = 'Vox generator',
    url = 'https://github.com/benoitfragit/VOXGenerator/tree/master/voxgenerator',
    author = 'Benoit Franquet',
    author_email = 'benoitfraubuntu@gmail.com',
    scripts = ['run_voxgenerator.py', 'run_voxgenerator'],
    keywords = ['voice', 'control', 'pocketsphinx'],
    classifiers     = ["Programming Language :: Python",
                     "Development Status :: 4 - Beta",
                     "Environment :: Other Environment",
                     "Intended Audience :: Developers",
                    "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
                    "Operating System :: OS Independent",
                    "Topic :: Software Development :: Libraries :: Python Modules"]
)
