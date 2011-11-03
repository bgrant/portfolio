function rsImages = hw5ReshapeImages(trainImages)
% HW5RESHAPEIMAGES  Reshape the given image matrix into a simpler 2-D matrix
%
% uint8[Y x X x 1 x N1] -> double[(Y*X) x N1]

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

rsImages = squeeze(trainImages);
[Y, X, N1] = size(rsImages);
rsImages = double(reshape(rsImages, Y*X, N1));

end
