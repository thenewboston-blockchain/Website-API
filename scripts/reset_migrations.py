import os

"""
python3 scripts/reset_migrations.py

Running this script will delete all migration files
"""


def main():
    for root, dirs, files in os.walk('v1'):
        if root[-10:] == 'migrations':
            for f in [file for file in files if file[:2] == '00']:
                os.remove(os.path.normpath(os.path.join(root, f)))
            create_init_file(root)


def create_init_file(root):
    init_file = os.path.normpath(os.path.join(root, '__init__.py'))
    if not os.path.exists(init_file):
        with open(init_file, 'wt') as f:
            f.write('')


if __name__ == '__main__':
    main()
