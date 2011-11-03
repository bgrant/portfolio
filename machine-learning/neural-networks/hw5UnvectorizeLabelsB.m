function labels = hw5UnvectorizeLabels(vecLabels)
% HW5UNVECTORIZELABELS  Transform binary vector labels back into integers
%
%        0 1 2 3 4 5 6 7 8 9
% e.g., [0 0 0 0 0 1 0 0 0 0] -> 5

% :author: Robert David Grant <robert.david.grant@gmail.com>
%
% :date: 2009-10-13
%
% :copyright:
%    Copyright 2011 Robert David Grant
%
%    Licensed under the Apache License, Version 2.0 (the "License"); you
%    may not use this file except in compliance with the License.  You
%    may obtain a copy of the License at
%
%       http://www.apache.org/licenses/LICENSE-2.0
%
%    Unless required by applicable law or agreed to in writing, software
%    distributed under the License is distributed on an "AS IS" BASIS,
%    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
%    implied.  See the License for the specific language governing
%    permissions and limitations under the License.

% if no neurons fired, pick one randomly
[maxes, indices] = max(vecLabels);
labels = indices - 1;

end

