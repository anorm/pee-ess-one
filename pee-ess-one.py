#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import colorama
import git           # REQUIRES: sudo apt-get install python-git
import os
import re
import sys

data = {
    'red':       colorama.Fore.RED,
    'green':     colorama.Fore.GREEN,
    'blue':      colorama.Fore.BLUE + colorama.Style.NORMAL,
    'lightblue': colorama.Fore.BLUE + colorama.Style.BRIGHT,
    'white':     colorama.Fore.WHITE,
    'n':         '\n' + colorama.Style.RESET_ALL}

def replace_format_string(s):
    wanted_keys = set(re.findall('{([a-z-]*)}', s))
    for key in wanted_keys - set(data.iterkeys()):
        if key == 'git':
            try:
                # ✔
                repo = git.Repo(os.getcwd(), search_parent_directories=True)
                status = colorama.Back.WHITE + colorama.Style.NORMAL + colorama.Fore.BLACK + '▏ '
                status += os.path.basename(repo.working_dir) + ' ▕'
                status += colorama.Back.WHITE + colorama.Style.NORMAL
                status += colorama.Fore.BLACK + '  '
                status += colorama.Fore.RED   + '?' if repo.is_dirty(index=False, working_tree=False, untracked_files=True,  submodules=False) else colorama.Fore.BLACK + ' ' # ?
                status += colorama.Fore.BLACK + ' '
                status += colorama.Fore.RED   + '⏺' if repo.is_dirty(index=False, working_tree=True,  untracked_files=False, submodules=False) else colorama.Fore.BLACK + ' ' # ⏺ 🖉
                status += colorama.Fore.BLACK + ' '
                status += colorama.Fore.BLACK + '🞣' if repo.is_dirty(index=True,  working_tree=False, untracked_files=False, submodules=False) else colorama.Fore.BLACK + ' '
                status += colorama.Fore.BLACK + '  '
                status += '▕'
                dirty = repo.is_dirty(index=True, working_tree=True,  untracked_files=True, submodules=False)
                if dirty:
                    status += colorama.Style.BRIGHT + colorama.Fore.WHITE + colorama.Back.RED
                else:
                    status += colorama.Style.BRIGHT + colorama.Fore.WHITE + colorama.Back.GREEN
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
                        status += ')'
                        if tracking_branch.remote_head != repo.active_branch.name:
                            status += '/' + tracking_branch.remote_head.encode('utf-8')
                        behind = sum(1 for c in repo.iter_commits(u'{}..{}/{}'.format(repo.active_branch, tracking_branch.remote_name, tracking_branch.remote_head)))
                        ahead  = sum(1 for c in repo.iter_commits(u'{}/{}..{}'.format(tracking_branch.remote_name, tracking_branch.remote_head, repo.active_branch)))
                        if ahead:
                            status += ' {}▲'.format(ahead)
                        if behind:
                            status += ' {}▼'.format(behind)
                    else:
                        status += ')'

                status += '  ' + colorama.Style.RESET_ALL

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
    return s.replace('\\n', '{n}').format(**data) + colorama.Style.RESET_ALL

def main():
    colorama.init(strip=False)
    p = argparse.ArgumentParser()
    p.add_argument("format")

    args = p.parse_args()

    sys.stdout.write(replace_format_string(args.format))

    return 0

if __name__ == '__main__':
    sys.exit(main())