#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

class LegacyContainerMixin(object):
    def __getitem__(self, obj):
        return self._info[obj]

    def __contains__(self, obj):
        return obj in self._info
    def get(self, obj, default=None):
        if default:
            return self._info.get(obj, default)
        return self._info.get(obj)

class Container(LegacyContainerMixin, object):
    def __init__(self, docker, container_info):
        self._docker = docker
        self._info = container_info

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

    def ip(self):
        cont_info = self._docker.inspect_container(self._info)
        nets = cont_info['NetworkSettings']['Networks'].items()
        assert len(nets) == 1
        return nets[0]['IPAddress']

    def _exec(self, cmd, output=False, detach=False):
        exec_info = self._docker.exec_create(self._info['Id'], cmd)
        if output:
            stream = docker_sock.exec_start(exec_info.get('Id'), stream=True)
            for x in stream:
                print x,
        else:
            docker_sock.exec_start(exec_info.get('Id'), detach=detach)

        if not detach:
            return docker_sock.exec_inspect(exec_info['Id'])['ExitCode']

