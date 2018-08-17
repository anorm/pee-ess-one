#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import colorama
import git           # REQUIRES: sudo apt-get install python-git
import os
import re
import sys

data = {
    'red':       '\001' + colorama.Fore.RED + '\002',
    'green':     '\001' + colorama.Fore.GREEN + '\002',
    'blue':      '\001' + colorama.Fore.BLUE + colorama.Style.NORMAL + '\002',
    'lightblue': '\001' + colorama.Fore.BLUE + colorama.Style.BRIGHT + '\002',
    'white':     '\001' + colorama.Fore.WHITE + '\002',
    'n':         '\n' + '\001' + colorama.Style.RESET_ALL + '\002'}

def replace_format_string(s):
    wanted_keys = set(re.findall('{([a-z-]*)}', s))
    for key in wanted_keys - set(data.iterkeys()):
        if key == 'git':
            try:
                # ✔
                repo = git.Repo(os.getcwd(), search_parent_directories=True)
                status = '\001' + colorama.Back.WHITE + colorama.Style.NORMAL + colorama.Fore.BLACK + '\002' + '▏ '
                status += os.path.basename(repo.working_dir) + ' ▕'
                status += '\001' + colorama.Back.WHITE + colorama.Style.NORMAL + '\002'
                status += '\001' + colorama.Fore.BLACK + '\002' + '  '
                status += '\001' + colorama.Fore.RED   + '\002' + '?' if repo.is_dirty(index=False, working_tree=False, untracked_files=True,  submodules=False) else '\001' + colorama.Fore.BLACK + '\002' + ' ' # ?
                status += '\001' + colorama.Fore.BLACK + '\002' + ' '
                status += '\001' + colorama.Fore.RED   + '\002' + '⏺' if repo.is_dirty(index=False, working_tree=True,  untracked_files=False, submodules=False) else '\001' + colorama.Fore.BLACK + '\002' + ' ' # ⏺ 🖉
                status += '\001' + colorama.Fore.BLACK + '\002' + ' '
                status += '\001' + colorama.Fore.BLACK + '\002' + '🞣' if repo.is_dirty(index=True,  working_tree=False, untracked_files=False, submodules=False) else '\001' + colorama.Fore.BLACK + '\002' + ' '
                status += '\001' + colorama.Fore.BLACK + '\002' + '  '
                status += '▕'
                dirty = repo.is_dirty(index=True, working_tree=True,  untracked_files=True, submodules=False)
                if dirty:
                    status += '\001' + colorama.Style.BRIGHT + colorama.Fore.WHITE + colorama.Back.RED + '\002'
                else:
                    status += '\001' + colorama.Style.BRIGHT + colorama.Fore.WHITE + colorama.Back.GREEN + '\002'
                status += '  '
                if repo.head.is_detached:
                    status += '(detached)'
                else:
                    status += '('
                    status += repo.active_branch.name.encode('utf-8')
                    tracking_branch = repo.active_branch.tracking_branch()
                    if tracking_branch:
                        status += ' 🗘 '
                        status += tracking_branch.remote_name.encode('utf-8')
                        if tracking_branch.remote_head != repo.active_branch.name:
                            status += '/' + tracking_branch.remote_head.encode('utf-8')
                        status += ')'
                        behind = sum(1 for c in repo.iter_commits(u'{}..{}/{}'.format(repo.active_branch, tracking_branch.remote_name, tracking_branch.remote_head)))
                        ahead  = sum(1 for c in repo.iter_commits(u'{}/{}..{}'.format(tracking_branch.remote_name, tracking_branch.remote_head, repo.active_branch)))
                        if ahead:
                            status += ' {}▲'.format(ahead)
                        if behind:
                            status += ' {}▼'.format(behind)
                    else:
                        status += ')'

                status += '  ' + '\001' + colorama.Style.RESET_ALL + '\002'

                data['git'] = status
            except TypeError as err:
                data['git'] = err
            except git.InvalidGitRepositoryError:
                data['git'] = ''
        elif key == 'pwd':
            pwd = os.getcwd()
            data['pwd'] = re.sub('^' + os.path.expanduser('~'), '~', pwd)
        else:
            data[key] = key
    return s.replace('\\n', '{n}').format(**data) + '\001' + colorama.Style.RESET_ALL + '\002'

def main():
    colorama.init(strip=False)
    p = argparse.ArgumentParser()
    p.add_argument("format")

    args = p.parse_args()

    sys.stdout.write(replace_format_string(args.format))

    return 0

if __name__ == '__main__':
    sys.exit(main())