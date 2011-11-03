function nnet = hw5TrainL(trainImages, trainLabels, passes)
% HW5TRAINL trains a single-layer perceptron to classify handwritten digit
% images
%
% Parameters:
% * `trainImages` is a [YxXx1xN1] matrix of images
% * `trainLabels` is a [1xN1] matrix of labels
% * `passes` is the number of training passes to use (default=10)
% between 0 and 1. (default=1)
%
% Return Values:
% * `nnet` is the trained perceptron

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

if nargin == 2,
    passes = 10;
end

%% Condition the input data
rsImages = hw5ReshapeImages(trainImages);
vecLabels = hw5VectorizeLabels(trainLabels);

%nnet = newp(repmat([0,255], [R, 1]), S, 'hardlim', 'learnp');
nnet = newp(rsImages, vecLabels, 'hardlim', 'learnp');

%% Train the network
nnet.adaptParam.passes = passes;
nnet = adapt(nnet, rsImages, vecLabels);

end
