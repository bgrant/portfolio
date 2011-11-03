function labels = hw5TestB(testImages, nnet)
% HW5TESTB uses a backpropagation-based neural net to classify handwritten
% digit images
%
% Parameters:
% * `testImages` is a [YxXx1xN2] matrix of images
% * `nnet` is the neural network returned by hw5TrainB
%
% Return Values:
% * `labels` is a [1xN2] array of generated labels for the `testImages`

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

%% Condition the data
rsImages = hw5ReshapeImages(testImages);

Y = sim(nnet, rsImages);
labels = uint8(hw5UnvectorizeLabelsB(Y));

end
