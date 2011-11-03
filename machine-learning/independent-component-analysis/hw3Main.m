% Homework #3
% Robert Grant
% 2009-09-20

% This script runs experiments with the Independent Component Analysis
% (ICA) algorithm implemented in the function file hw3ICA.

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

%% %%% First test %%% %%
clear;

%% Choose Data
icaTest = './icaTest.mat';

%% Load, Format, and Mix Data
data = load(icaTest);
A = data.A;
U = data.U;
X = A*U; % linearly mix data
[n,t] = size(U);
[m,t] = size(X);

%% Independent Component Analysis
rand('twister', 1234); % seed random number generator
W = rand(n,m); % initial guess
eta = 0.01; % learning rate
maxiter = 1e6;
[Y,W,R] = hw3ICA(X,W,eta,maxiter);

%% Reproduce Example Plot %%
t = max(size(U));
figure; hold on; 
title('Sets of Signals');
xlabel('t');
ylabel('U, X, Y');

plot(U(1,:)+0,'b'); 
plot(U(2,:)+1,'g');
plot(U(3,:)+2,'r');

plot(zeros(t,1)+3);

plot(X(1,:)+3,'b'); 
plot(X(2,:)+3.5,'g');
plot(X(3,:)+5,'r');

plot(zeros(t,1)+6);

plot(Y(1,:)+6.2,'b'); 
plot(Y(2,:)+7.2,'g');
plot(Y(3,:)+8.2,'r');


%% %%% Second test %%% %%
clear;

%% Choose and Load Data
soundfile = './sounds.mat';
sounds = load(soundfile);
allsounds = sounds.sounds;

%% Mix Data
U = allsounds([1,3,4],:); % mix Homer, clapping, laughing
[n,t] = size(U);
rand('twister', 1234); % seed random number generator
A = rand(n); % nsources == nreceivers
X = A*U; % linearly mix data
[m,t] = size(X);

%% Independent Component Analysis
W = rand(n,m); % initial guess
eta = 0.0001; % learning rate
maxiter = 100000;
[Y,W,R] = hw3ICA(X,W,eta,maxiter);

%% Like Example Plot %%
range = 1000:2000;
figure; hold on; 
title('Sets of Signals');
xlabel('t');
ylabel('U, X, Y');

plot(U(1,range)+0,'b'); 
plot(U(2,range)+1,'g');
plot(U(3,range)+2,'r');

%plot(zeros(t,1)+3);

plot(X(1,range)+3,'b'); 
plot(X(2,range)+4,'g');
plot(X(3,range)+5,'r');

%plot(zeros(t,1)+6);

plot(10*Y(1,range)+6,'b'); 
plot(10*Y(2,range)+7,'g');
plot(10*Y(3,range)+8,'r');

% [EOF]
