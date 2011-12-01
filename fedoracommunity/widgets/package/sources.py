import os
import git
import subprocess
import tw2.core as twc
import logging

from tg import config
from mako.template import Template
from collections import OrderedDict

from package import TabWidget

log = logging.getLogger(__name__)

class FedoraGitRepo(object):

    def __init__(self, package, branch='master'):
        self.package = package
        self.repo_path = os.path.join(config.get('git_repo_path'),
                                      package, branch)
        if not os.path.isdir(self.repo_path):
            top_repo = os.path.dirname(self.repo_path)
            if not os.path.isdir(top_repo):
                os.makedirs(top_repo)
            self.clone_repo()
        self.repo = git.Repo(self.repo_path)

    def _run(self, cmd, **kw):
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, **kw)
        out, err = p.communicate()
        if out: log.debug(out)
        if err: log.error(err)
        return p.returncode

    def clone_repo(self):
        self._run('fedpkg clone --anonymous --branches ' + self.package,
                  cwd=config.get('git_repo_path'))

    def get_spec(self):
        spec = self.repo.tree()[self.package + '.spec']
        return spec.data_stream.read()


class Sources(TabWidget):
    tabs = OrderedDict([('Spec', 'package.sources.spec')])
    base_url = Template(text='/${kwds["package_name"]}/sources/')
    default_tab = 'Spec'


class Spec(twc.Widget):
    kwds = twc.Param(default=None)
    text = twc.Param('The text of the specfile')
    template = 'mako:fedoracommunity/widgets/package/templates/package_spec.mak'
    def prepare(self):
        super(Spec, self).prepare()
        repo = FedoraGitRepo(self.kwds['package_name'])
        self.text = repo.get_spec()


class Patches(twc.Widget):
    def prepare(self):
        super(Patches, self).prepare()


class Diffs(twc.Widget):
    def prepare(self):
        super(Diffs, self).prepare()


class Tarballs(twc.Widget):
    def prepare(self):
        super(Tarballs, self).prepare()


class GitRepo(twc.Widget):
    def prepare(self):
        super(GitRepo, self).prepare()


class UpstreamSources(twc.Widget):
    def prepare(self):
        super(UpstreamSources, self).prepare()
