#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

class LegacyInfoMixin(object):
    def __init__(self, info):
        self._info = info

    def __getitem__(self, obj):
        return self._info[obj]

    def __contains__(self, obj):
        return obj in self._info

    def get(self, obj, default=None):
        if default:
            return self._info.get(obj, default)
        return self._info.get(obj)

class Container(LegacyInfoMixin):
    def __init__(self, docker, container_info):
        self._docker = docker
        super(Container, self).__init__(container_info)

    def run(self):
        self._docker.start(self._info.get('Id'))
        return self

    def destroy(self):
        try:
            self._docker.kill(self._info['Id'])
        except docker.errors.APIError:
            pass
        self._docker.remove_container(self._info['Id'])

    def __enter__(self):
        return self.run()

    def __exit__(self, type, value, traceback):
        self.destroy()

    def exec_create(self, cmd, **kwargs):
        exec_info = self._docker.exec_create(self._info['Id'], cmd, **kwargs)
        return Exec(self._docker, exec_info)

class Exec(LegacyInfoMixin):
    def __init__(self, docker, exec_info):
        self._docker = docker
        super(Exec, self).__init__(exec_info)

    def start(self, **kwargs):
        return self._docker.exec_start(self._info.get('Id'), **kwargs)
