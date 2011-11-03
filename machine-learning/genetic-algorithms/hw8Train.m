function best_net = hw8Train()
% best_net = hw8GA()
% Use a genetic algorithm to evolve a network capable of sorting an
% unsorted matrix of doubles.
% 
% :Parameters:
% `unsorted_matrix`: an unsorted 1x8 matrix of doubles
% 
% :Return Values:
% `sorted_matrix`: a sorted 1x8 matrix of doubles

RUN_TESTS = 0;
RUN_EVOLUTION = 1;
SHOW_PROGRESS = 1;
NITERATIONS = 50; % number of iterations to run in unit tests

MUTATION_RATE = 0.001;
POP_SIZE = 50; % population size
SELECTION_FRAC = 0.1; % percentage of top performers to select
NGENERATIONS = 1000;
MIN_INITIAL_CSIZE = 8;
MAX_INITIAL_CSIZE = 50; % maximum initial chromosome size
NALLELES = 8;

if RUN_TESTS
    display(sprintf('Running All Tests...\n'));
    test(@test_rand_gene, NITERATIONS);
    test(@test_rand_chrom, NITERATIONS);
    test(@test_rand_pop, NITERATIONS);
    test(@test_mutate, NITERATIONS);
    test(@test_hw8Test, NITERATIONS);
    test(@test_fitness, NITERATIONS);
    test(@test_selection, NITERATIONS);
    test(@test_crossover, NITERATIONS);
    test(@test_breed, NITERATIONS);
end

if RUN_EVOLUTION
    if SHOW_PROGRESS
        display(sprintf('Initializing...\n'));
    end
    best_solutions = cell(1,NGENERATIONS);
    max_fitnesses = zeros(1,NGENERATIONS);
    
    if SHOW_PROGRESS
        display(sprintf('Starting Generation 1...'));
        tic;
    end
    pop = rand_pop(POP_SIZE, MIN_INITIAL_CSIZE, MAX_INITIAL_CSIZE, NALLELES);

    for i=1:NGENERATIONS
        fitnesses = cellfun(@fitness, pop);
        [max_fitness, index] = max(fitnesses);
        best_solutions{i} = pop{index};
        max_fitnesses(i) = max_fitness;
        if SHOW_PROGRESS
            t = toc;
            display(sprintf('  took %d seconds.\n', t));
        end

        if i < NGENERATIONS
            if SHOW_PROGRESS
                display(sprintf('Starting Generation %d...', i+1));
                tic;
            end
            top_performers = selection(pop, fitnesses, round(POP_SIZE*SELECTION_FRAC));
            pop = breed(top_performers, POP_SIZE);
            pop = mutate(pop, MUTATION_RATE, NALLELES); 
        end
    end
    
    solution_lengths = zeros(1,length(best_solutions));
    for i=1:length(best_solutions)
        [solution_lengths(i), ncols] = size(best_solutions{i}); 
    end
    
    figure;
    plot(max_fitnesses, 'o-');
    title('Fitness of best individual vs. Generation');
    ylabel('Fitness');
    xlabel('Generation');
    
    figure;
    plot(solution_lengths, 'o-');
    title('Length of best individual vs. Generation');
    ylabel('Length');
    xlabel('Generation');

    [overall_best_fitness, overall_best_solution] = max(max_fitnesses);
    best_net = best_solutions{overall_best_solution};
end
end


function new_pop = breed(pop, new_popsize)
% new_pop = breed(pop, new_popsize)
% Using crossover, breed members of population up to a new size
%
% :Parameters:
% `pop`: a population (probably output from the selection function)
% `new_popsize`: a new population size generate via crossover.
%
% :Return Value:
% `new_pop`: a population of size `new_popsize` created by breeding members
% of pop using crossover

    new_pop = cell(1,new_popsize);
    for i = 1:new_popsize
        pair = randsample(1:length(pop), 2, true);
        new_pop{i} = crossover(pop{pair(1)}, pop{pair(2)});       
    end
end

function test_breed(niterations)
% test_breed(niterations)
% Test function for breed(pop, new_popsize)

    pop = {[1,2]};
    new_pop = breed(pop, 2);
    assert(length(new_pop) == 2);
    
    POP_SIZE = 30;
    MIN_INITIAL_CSIZE = 2;
    MAX_INITIAL_CSIZE = 10;
    NALLELES = 8;
    pop = rand_pop(POP_SIZE, MIN_INITIAL_CSIZE, MAX_INITIAL_CSIZE, NALLELES);

    for i=1:niterations,
        new_pop = breed(pop, POP_SIZE);
        assert(length(new_pop) == POP_SIZE);
    end
end


function new_chrom = crossover(chrom1, chrom2)
% new_chrom = crossover(chrom1, chrom2)
% Form an offspring using single point crossover.
%
% :Parameters:
% `chrom1`: the first chromosome to use (Nx2 matrix)
% `chrom2`: the second chromosome to use (Nx2 matrix)
%
% :Return Values:
% `new_chrom`: a new chromosome formed by randomly choosing a crossover
% point in each of the two chromosomes, and using the first half of chrom1
% and the second half of chrom2.

    [c1rows, c1cols] = size(chrom1);
    [c2rows, c2cols] = size(chrom2);
    chrom1_locus = randsample(0:c1rows, 1);
    chrom2_locus = randsample(0:c2rows, 1);
    
    if chrom1_locus == 0
        new_chrom = chrom2;
    elseif chrom2_locus == 0
        new_chrom = chrom1;
    else
        new_chrom = [chrom1(1:chrom1_locus, :); ...
                     chrom2(chrom2_locus:end, :)];
    end
end

function test_crossover(niterations)
% test_crossover(niterations)
% Test function for crossover(chrom1, chrom2)

    min_size = 2;
    max_size = 50;
    nalleles = 8;
    for i=1:niterations
        chrom1 = rand_chrom(min_size, max_size, nalleles);
        chrom2 = rand_chrom(min_size, max_size, nalleles);
        xover = crossover(chrom1, chrom2);
    end

end


function selected_pop = selection(pop, fitnesses, selection_size)
% selected_pop = selection(pop, fitnesses, new_popsize)
% Select most fit in population using roulette wheel selection.
%
% :Parameters:
% `pop`: population from which to select
% `fitnesses`: 1xlength(pop) vector of fitnesses for population
% `selection_size`: number of individuals to select (must be <=
% length(pop))
%
% :Return Values:
% `selected_pop`: `selection_size` individuals selected from `pop` using
% roulette wheel selection

    assert(selection_size <= length(pop));
%    fitnesses = cellfun(@fitness, pop);
    
    selected_pop = cell(1,selection_size);
    for i=1:selection_size
        popsize = length(pop);
        selected_index = randsample(1:popsize, 1, true, fitnesses);
        selected_pop{i} = pop{selected_index};
        pop(i) = [];
        fitnesses(i) = [];
    end
end

function test_selection(niterations)
% test_selection(niterations)
% Test function for selection(pop, selection_size)
    POP_SIZE = 30;
    MIN_INITIAL_CSIZE = 2;
    MAX_INITIAL_CSIZE = 10;
    NALLELES = 8;
    pop = rand_pop(POP_SIZE, MIN_INITIAL_CSIZE, MAX_INITIAL_CSIZE, NALLELES);

    % Commented out lines are for visual inspection of results
%    sort(cellfun(@fitness, pop))
    fitnesses = cellfun(@fitness, pop);
    for i=1:niterations
        new_pop = selection(pop, fitnesses, 5);
        assert(length(new_pop) == 5);
%       sort(cellfun(@fitness, new_pop))
    end
end


function score = fitness(chrom)
% score = fitness(chrom)
% Compute a fitness score for a chromosome.
% 
% :Parameters:
% `chrom`: an evolved sorting network from the population (Nx2 matrix)
% 
% :Return Values:
% `score`: is a ranking of the `chrom`'s sorting ability.  Currently
% computed as one minus the average hamming distance between the an unsorted matrix
% after appling the `gene` and it's true sorted form.

    NTESTS = 50;
    NALLELES = 8;
    test_matrices = rand(NTESTS, NALLELES);
    gene_sorted = zeros(NTESTS, NALLELES);
    for row=1:NTESTS
        gene_sorted(row,:) = hw8Test(test_matrices(row,:), chrom);
    end
    real_sorted = sort(test_matrices, 2);

    score = 1 - sum(sum((real_sorted == gene_sorted))) / numel(test_matrices);
end

function test_fitness(niterations)
% test_fitness()
% Test function for fitness(gene)
    NALLELES = 8;

    for i=1:niterations
        score = fitness(rand_chrom(2,50, NALLELES));
        assert(numel(score) == 1);
        assert(0 <= score <= 1);
    end
    
end


function pop = mutate(pop, rate, nalleles)
% new_pop = mutate(population, rate, nalleles)
% Randomly replace a fraction of a population's genes.
%
% :Parameters:
% `pop`: cell array of chromosomes to mutate
% `rate`: fraction of a population's genes to mutate
% `nalleles`: number of possible alleles
%
% :Return Values:
% `new_pop`: `population` with a fraction of its genes randomly replaced

    chrom_sizes = zeros(1, length(pop));
    for i=1:length(pop)
        chrom_sizes(i) = length(pop{i});
    end
    
    ngenes = sum(chrom_sizes);
    nmutations = ceil(rate * ngenes);
    target_genes = sort(randsample(1:ngenes, nmutations));
    
    next_mutation = 1;
    chrom_index = 1;
    while next_mutation <= nmutations 
        if chrom_sizes(chrom_index) < target_genes(next_mutation)
            offsets = repmat(chrom_sizes(chrom_index), 1, nmutations);
            chrom_index = chrom_index + 1;
            target_genes = target_genes - offsets;
        else 
            assert(chrom_sizes(chrom_index) >= target_genes(next_mutation));
            pop{chrom_index}(target_genes(next_mutation),:) = rand_gene(nalleles);
            next_mutation = next_mutation + 1;
        end
    end
    
end

function test_mutate(niterations)
% test_mutate(niterations)
% Test function for mutate(population, rate, nalleles)
    population = {[1 2; 3 4], [5 6; 7 8]};
    rate = 1/4;
    nalleles = 8;
    
    new_pop = mutate(population, rate, nalleles);
    % `new_pop` is same size but probabilistically different from
    % `population`
    assert(all(size(population) == size(new_pop)));
    
    for i = 1:niterations
        popsize = randsample(2:10, 1);
        min_csize = 2;
        max_csize = 50;
        nalleles = 8;
        population = rand_pop(popsize, min_csize, max_csize, nalleles);
        rate = 0.01;
        new_pop = mutate(population, rate, nalleles);
        assert(all(size(population) == size(new_pop)));
    end
end


function population = rand_pop(popsize, min_csize, max_csize, nalleles)
% population = rand_pop(popsize, min_csize, max_csize, nalleles)
% Generate a random population of chromosomes
%
% :Parameters:
% `popsize`: number of chromosomes in population
% `min_size`: minimum number of alleles in a chromosome
% `max_size`: maximumum number of alleles in a chromosome
% `nalleles`: size of input to be sorted
%
% :Return Values:
% `population`: a 1 x popsize cell array containing chromosomes
    population = cell(1, popsize);
    for i=1:popsize
        population{i} = rand_chrom(min_csize, max_csize, nalleles);
    end
end

function test_rand_pop(niterations)
% test_rand_pop(niterations)
% Test function for rand_pop(popsize, min_csize, max_csize, nalleles).
    for i=1:niterations,
        popsize = randsample(2:50, 1);
        min_csize = randsample(2:10, 1);
        max_csize = randsample(11:50, 1);
        nalleles = 8;
        
        population = rand_pop(popsize, min_csize, max_csize, nalleles);
        [nrows, ncols] = size(population);
        assert(nrows == 1);
        assert(ncols == popsize);
    end
end


function chrom = rand_chrom(min_size, max_size, nalleles)
% rand_chromosome(max_size, nalleles)
% Generate a random chromosome of random length
%
% :Parameters:
% `min_size`: minimum number of alleles in a chromosome
% `max_size`: maximumum number of alleles in a chromosome
% `nalleles`: size of input to be sorted
%
% :Return Value:
% `chrom`: an Nx2 array of digits, where each row is a gene (in this
% case a possible swap pair)
    csize = randsample(min_size:max_size, 1);
    chrom = zeros(csize, 2);
    for i = 1:csize
        chrom(i, :) = rand_gene(nalleles);
    end
end

function test_rand_chrom(niterations)
% test_rand_chrom(niterations)
% Test function for rand_chrom(min_size, max_size, nalleles)
    for i = 1:niterations
        min_size = randsample(2:10, 1);
        max_size = randsample(11:50, 1);
        nalleles = 8;
        
        chrom = rand_chrom(min_size, max_size, nalleles);
        [nrows, ncols] = size(chrom);
        assert(nrows <= max_size);
        assert(nrows >= min_size);
        assert(ncols == 2);
    end
end


function pruned_chrom = prune_chrom(chrom)
% chrom = prune_chrom(chrom)
% Prune a chromosome of obviously bad genes.
%
% :Parameters:
% `chrom`: a chromosome (an Nx2 matrix), where each row is a gene
%
% :Return Values:
% `pruned_chrom`: `chrom` with all instances of two adjacent cancelling
% genes removed
    
% UNIMPLEMENTED

end

function allele = rand_gene(nalleles)
% allele = rand_gene(nalleles)
% Generate a random pair of integers
%
% :Parameters:
% `nalleles`: size of input to be sorted
%
% :Return Values:
% `allele`: a 1x2 array of integers representing possible positions to swap
% in the input array
    allele = randsample(nalleles, 2)';
end

function test_rand_gene(niterations)
% test_rand_gene(niterations)
% Unit test for functions rand_gene(nalleles).
    for i=1:niterations
        nalleles = randsample(2:10, 1);
        allele = rand_gene(nalleles);
        assert(length(allele) == 2);
        assert(all( ismember(allele, 1:nalleles) ));
    end
end


function test(fn, niterations, varargin)
% test(fn, varargin)
% Helper function to run tests and display error messages
    disp(sprintf('Running %s...', func2str(fn)));
    
    passed = 1;
    try
        fn(niterations, varargin{:});
    catch
        passed = 0;
        msg = lasterror();
        disp(sprintf('Failed: %s', msg.message));
    end
    if passed,
        disp('Passed');
    end
    disp(' ');
end


function test_hw8Test(niterations)
% test_hw8Test()
% Test function for hw8Test(unsorted_matrix, chrom)
% (Implemented in another file, hw8Test.m)
    
    unsorted_matrix = [8 7 6 5 4 3 2 1];
    chrom = [1 1];
    sorted_matrix = hw8Test(unsorted_matrix, chrom);
    assert(all(sorted_matrix == unsorted_matrix));
    
    unsorted_matrix = [8 7 6 5 4 3 2 1];
    chrom = [1 1; 2 2; 3 3; 4 4; 5 5; 6 6; 7 7; 8 8];
    sorted_matrix = hw8Test(unsorted_matrix, chrom);
    assert(all(sorted_matrix == unsorted_matrix));
    
    unsorted_matrix = [8 7 6 5 4 3 2 1];
    chrom = [8 1];
    sorted_matrix = hw8Test(unsorted_matrix, chrom);
    assert(all(unsorted_matrix(2:7) == sorted_matrix(2:7)));
    assert(unsorted_matrix(1) == sorted_matrix(8));
    assert(unsorted_matrix(8) == sorted_matrix(1));
    
    unsorted_matrix = [8 7 6 5 4 3 2 1];
    chrom = [8 1];
    sorted_matrix = hw8Test(unsorted_matrix, chrom);
    sorted_matrix = hw8Test(sorted_matrix, chrom);
    sorted_matrix = hw8Test(sorted_matrix, chrom);
    sorted_matrix = hw8Test(sorted_matrix, chrom);
    assert(all(unsorted_matrix(2:7) == sorted_matrix(2:7)));
    assert(unsorted_matrix(1) == sorted_matrix(8));
    assert(unsorted_matrix(8) == sorted_matrix(1));

    unsorted_matrix = [8 7 6 5 4 3 2 1];
    chrom = [8 1; 7 2; 6 3; 5 4];
    sorted_matrix = hw8Test(unsorted_matrix, chrom);
    assert(all(sorted_matrix == 1:8));
    sorted_matrix = hw8Test(sorted_matrix, chrom);
    assert(all(sorted_matrix == 1:8));
    
    unsorted_matrix = [2 1];
    chrom = [1 2];
    sorted_matrix = hw8Test(unsorted_matrix, chrom);
    assert(all(sorted_matrix == [1 2]));
    sorted_matrix = hw8Test(sorted_matrix, chrom);
    assert(all(sorted_matrix == [1 2]));
end