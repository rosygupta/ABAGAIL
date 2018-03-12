import sys
import os
import time

sys.path.append("../../../bin")

import java.io.FileReader as FileReader
import java.io.File as File
import java.lang.String as String
import java.lang.StringBuffer as StringBuffer
import java.lang.Boolean as Boolean
import java.util.Random as Random

import dist.DiscreteDependencyTree as DiscreteDependencyTree
import dist.DiscreteUniformDistribution as DiscreteUniformDistribution
import dist.Distribution as Distribution
import opt.DiscreteChangeOneNeighbor as DiscreteChangeOneNeighbor
import opt.EvaluationFunction as EvaluationFunction
import opt.GenericHillClimbingProblem as GenericHillClimbingProblem
import opt.HillClimbingProblem as HillClimbingProblem
import opt.NeighborFunction as NeighborFunction
import opt.RandomizedHillClimbing as RandomizedHillClimbing
import opt.SimulatedAnnealing as SimulatedAnnealing
import opt.example.FourPeaksEvaluationFunction as FourPeaksEvaluationFunction
import opt.ga.CrossoverFunction as CrossoverFunction
import opt.ga.SingleCrossOver as SingleCrossOver
import opt.ga.DiscreteChangeOneMutation as DiscreteChangeOneMutation
import opt.ga.GenericGeneticAlgorithmProblem as GenericGeneticAlgorithmProblem
import opt.ga.GeneticAlgorithmProblem as GeneticAlgorithmProblem
import opt.ga.MutationFunction as MutationFunction
import opt.ga.StandardGeneticAlgorithm as StandardGeneticAlgorithm
import opt.ga.UniformCrossOver as UniformCrossOver
import opt.prob.GenericProbabilisticOptimizationProblem as GenericProbabilisticOptimizationProblem
import opt.prob.MIMIC as MIMIC
import opt.prob.ProbabilisticOptimizationProblem as ProbabilisticOptimizationProblem
import shared.FixedIterationTrainer as FixedIterationTrainer
import opt.example.KnapsackEvaluationFunction as KnapsackEvaluationFunction
from array import array

import csv


"""
Commandline parameter(s):
    none
"""

params = {
    'RHC': [[]],
    'GA': [
        [10, 5, 2], [10, 5, 7],[10, 7, 2], [10, 7, 7],
        [20, 10, 5], [20, 10, 8], [20, 15, 5], [20, 15, 8],
        [50, 25, 10], [50, 25, 15], [50, 40, 10], [50, 40, 15],
        [100, 50, 10], [100, 50, 20], [100, 80, 10], [100, 80, 20],
        [200, 100, 20], [200, 100, 50], [200, 150, 20], [200, 150, 50],
        [500, 350, 50], [500, 350, 100],[500, 450, 50], [500, 450, 100]
    ],
    'SA': [
        [1e11, 0.15], [1e11, 0.25], [1e11, 0.35], [1e11, 0.45], [1e11, 0.55],
        [1e11, 0.65], [1e11, 0.75], [1e11, 0.85], [1e11, 0.95],
        [1e5, 0.15], [1e5, 0.25], [1e5, 0.35], [1e5, 0.45], [1e5, 0.55],
        [1e5, 0.65], [1e5, 0.75], [1e5, 0.85], [1e5, 0.95]
    ]
}

identifier = {
    'RHC': lambda p: 'noparams',
    'GA': lambda p: '_'.join([str(v) for v in p]),
    'SA': lambda p: str(p[1]).replace('.', '_')
}

iterations = [10, 100, 500, 1000, 2500, 3000, 3500, 4000, 4500, 5000, 6000]

for param in params['GA']:
    # set N value.  This is the number of points

    output_filename = 'Knapsack %s-%s.csv' % ('GA', identifier['GA'](param))
    csv_file = open(output_filename, 'w')
    fields = ['num_iterations', 'value', 'time']
    writer = csv.DictWriter(csv_file, fieldnames=fields)
    writer.writeheader()
    for num_iterations in iterations:
        # Random number generator */
        random = Random()
        # The number of items
        NUM_ITEMS = 40
        # The number of copies each
        COPIES_EACH = 4
        # The maximum weight for a single element
        MAX_WEIGHT = 50
        # The maximum volume for a single element
        MAX_VOLUME = 50
        # The volume of the knapsack
        KNAPSACK_VOLUME = MAX_VOLUME * NUM_ITEMS * COPIES_EACH * .4

        # create copies
        fill = [COPIES_EACH] * NUM_ITEMS
        copies = array('i', fill)

        # create weights and volumes
        fill = [0] * NUM_ITEMS
        weights = array('d', fill)
        volumes = array('d', fill)
        for i in range(0, NUM_ITEMS):
            weights[i] = random.nextDouble() * MAX_WEIGHT
            volumes[i] = random.nextDouble() * MAX_VOLUME

        # create range
        fill = [COPIES_EACH + 1] * NUM_ITEMS
        ranges = array('i', fill)

        ef = KnapsackEvaluationFunction(weights, volumes, KNAPSACK_VOLUME, copies)
        odd = DiscreteUniformDistribution(ranges)
        nf = DiscreteChangeOneNeighbor(ranges)
        mf = DiscreteChangeOneMutation(ranges)
        cf = UniformCrossOver()
        df = DiscreteDependencyTree(.1, ranges)
        hcp = GenericHillClimbingProblem(ef, odd, nf)
        gap = GenericGeneticAlgorithmProblem(ef, odd, mf, cf)
        pop = GenericProbabilisticOptimizationProblem(ef, odd, df)

        start = time.time()
        ga = StandardGeneticAlgorithm(200, 150, 25, gap)
        fit = FixedIterationTrainer(ga, 1000)
        fit.train()
        end = time.time()
        value = str(ef.value(ga.getOptimal()))
        # print "GA: " + value
        # print "Time -->", end - start

        results = {
            'num_iterations': num_iterations,
            'value': value,
            'time': end - start

        }

        print 'GA', param, results
        writer.writerow(results)

    csv_file.close()
    print '------'
print '***** ***** ***** ***** *****'



