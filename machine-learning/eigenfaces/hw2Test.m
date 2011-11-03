function hw2FindEigenfaces_Test(A)
% HW2FINDEIGENFACES_TEST  Perform simple assertion tests on function.
% 
% When executed, this function will run a series of tests.  If a test
% fails, the function will end with an assertion error.

% :author: Robert David Grant <robert.david.grant@gmail.com>
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

% Robert Grant
% Homework #2
% 2009-09-13

%% Simple test
A = [1 0;
     0 1];

[m, V] = hw2FindEigenfaces(A);
matassert(m == [0.5, 0.5]');
matassert(V == [1 0; 0 1])

%%
A = [1 0;
     0 1];

[m, V] = hw2FindEigenfaces(A);
matassert(m == [0.5, 0.5]');
matassert(V == [1 0; 0 1])



end




%%
function matassert(cond)
% Generalized assert
    assert(all(reshape(cond,1,[])));
end
