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
