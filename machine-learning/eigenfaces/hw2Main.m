% This script runs experiments by varying different parameters involving
% classifying faces using Principal Component Analysis.  This script calls
% the functions hw2LoadPictureFiles and hw2ClassifyEigenfaces to load and
% then classify these pictures.

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

% Homework #2
% Robert Grant
% 2009-09-13

clear; clc;

%% Load Data
data = hw2LoadPictureFiles();

%% Use first train_factor% of data to train, rest to test
train_factors = 0.1:0.1:0.9; 

% test algorithm, compare against human labels and return error rates
error_rates_1 = zeros(length(data), length(train_factors));
for i  = 1:length(train_factors),  
    error_rates_1(:,i) = hw2ClassifyEigenfaces(data{1}, train_factors(i));
end

error_rates_2 = zeros(length(data), length(train_factors));
for i  = 1:length(train_factors),  
   error_rates_2(:,i) = hw2ClassifyEigenfaces(data{2}, train_factors(i));
end

error_rates_3 = zeros(length(data), length(train_factors));
for i  = 1:length(train_factors),  
    error_rates_3(:,i) = hw2ClassifyEigenfaces(data{3}, train_factors(i));
end


%% Plot mean eigenfaces
[m1,V1] = hw2FindEigenfaces(data{1}.gallery);
figure; imshow(uint8(reshape(m1, data{1}.height, [])));
figure; imshow(uint8(reshape(V1(:,1)+m1, data{1}.height, [])));

[m2,V2] = hw2FindEigenfaces(data{2}.gallery);
figure; imshow(uint8(reshape(m2, data{2}.height, [])));
figure; imshow(uint8(reshape(V2(:,1)+m2, data{2}.height, [])));

[m3,V3] = hw2FindEigenfaces(data{3}.gallery);
figure; imshow(uint8(reshape(m3, data{3}.height, [])));
figure; imshow(uint8(reshape(V3(:,1)+m3, data{3}.height, [])));


%% Plot error rates
figure; plot(train_factors, error_rates_1'); 
title('Error rates for class08 dataset');
xlabel('Fraction training');
ylabel('Error rate');
legend('Smiling', 'Glasses', 'Male');

figure; plot(train_factors, error_rates_2'); 
title('Error rates for class09 dataset');
xlabel('Fraction training');
ylabel('Error rate');
legend('Smiling', 'Glasses', 'Male');

figure; plot(train_factors, error_rates_3'); 
title('Error rates for yale dataset'); 
xlabel('Fraction training');
ylabel('Error rate');
legend('Smiling', 'Glasses', 'Male');

% [EOF]
