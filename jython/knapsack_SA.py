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
        [10, 5, 20], [10, 5, 30], [10, 5, 50], [10, 100, 20], [10, 100, 30], [10, 300, 50], [10, 300, 20], [10, 300, 30],
        [200, 5, 20], [200, 5, 30], [200, 5, 50], [200, 100, 20], [200, 100, 30], [200, 300, 50], [200, 300, 20], [200, 300, 30],
        [500, 5, 20], [500, 5, 30], [500, 5, 50], [500, 100, 20], [500, 100, 30], [500, 300, 50], [500, 300, 20], [500, 300, 30]
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
    'SA': lambda p: (str(p[0]) + "-"+(str(p[1]))).replace('.', '_')
}

iterations = [10, 100, 500, 1000, 2500, 3000, 3500, 4000, 4500, 5000, 6000]

for param in params['SA']:
    # set N value.  This is the number of points

    output_filename = 'Knapsack %s-%s.csv' % ('SA', identifier['SA'](param))
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


        # rhc = RandomizedHillClimbing(hcp)
        # fit = FixedIterationTrainer(rhc, num_iterations)
        # fit.train()


        start = time.time()
        sa = SimulatedAnnealing(param[0], param[1], hcp)
        fit = FixedIterationTrainer(sa, num_iterations)
        fit.train()
        end = time.time()
        value = str(ef.value(sa.getOptimal()))
        results = {
            'num_iterations': num_iterations,
            'value': value,
            'time': end - start

        }
        print 'SA', param, results
        writer.writerow(results)

        # ga = StandardGeneticAlgorithm(param[0], param[1], param[2], gap)
        # fit = FixedIterationTrainer(ga, num_iterations)
        # fit.train()
        # print "GA: " + str(ef.value(ga.getOptimal()))
        #
        # mimic = MIMIC(200, 100, pop)
        # fit = FixedIterationTrainer(mimic, 1000)
        # fit.train()
        # print "MIMIC: " + str(ef.value(mimic.getOptimal()))

    csv_file.close()
    print '------'
print '***** ***** ***** ***** *****'



