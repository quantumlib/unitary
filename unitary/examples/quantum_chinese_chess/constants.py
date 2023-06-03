# Copyright 2023 The Unitary Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
PIECES = {
 0: '.',
 1: 'S',
 -1: 's',
 2: 'H',
 -2: 'h',
 3: 'E',
 -3: 'e',
 4: 'R',
 -4: 'r',
 5: 'A',
 -5: 'a',
 6: 'G',
 -6: 'g',
 7: 'C',
 -7: 'c'}

REV_PIECES = {
 ' ': '0',
 '.': '0',
 'S': '1',
 's': '-1',
 'H': '2',
 'h': '-2',
 'E': '3',
 'e': '-3',
 'R': '4',
 'r': '-4',
 'A': '5',
 'a': '-5',
 'G': '6',
 'g': '-6',
 'C': '7',
 'c': '-7'}

EMPTY = 0
SOLDIER = 1
HORSE = 2
ELEPHANT = 3
ROOK = 4
ADVISOR = 5
GENERAL = 6
CANNON = 7
