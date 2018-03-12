import sys
import os
import time
sys.path.append("../bin")

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
import opt.example.ContinuousPeaksEvaluationFunction as ContinuousPeaksEvaluationFunction
from array import array


import csv


"""
Commandline parameter(s):
   none
"""
# set N value.  This is the number of points
optalgs = ['RHC']

OA = {
    'RHC': RandomizedHillClimbing,
    'GA': StandardGeneticAlgorithm,
    'SA': SimulatedAnnealing
}

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
    'SA': lambda p: str(p[1]).replace('.', '_')
}
identifier = {
    'RHC': lambda p: 'noparams',
    'GA': lambda p: '_'.join([str(v) for v in p]),
    'SA': lambda p: str(p[1]).replace('.', '_')
}

iterations = [10, 100, 500, 1000, 2500, 3000, 3500, 4000, 4500, 5000, 6000, 7000, 8000, 9000, 10000]

for param in params['RHC']:

    output_filename = 'CP %s-%s.csv' % ('RHC', identifier['RHC'](param))
    csv_file = open(output_filename, 'w')
    fields = ['num_iterations', 'value', 'time']
    writer = csv.DictWriter(csv_file, fieldnames=fields)
    writer.writeheader()

    for it_count in iterations:
        N = 60
        T = N / 10
        fill = [2] * N
        ranges = array('i', fill)

        ef = ContinuousPeaksEvaluationFunction(T)
        odd = DiscreteUniformDistribution(ranges)
        nf = DiscreteChangeOneNeighbor(ranges)
        mf = DiscreteChangeOneMutation(ranges)
        cf = SingleCrossOver()
        df = DiscreteDependencyTree(.1, ranges)
        hcp = GenericHillClimbingProblem(ef, odd, nf)
        gap = GenericGeneticAlgorithmProblem(ef, odd, mf, cf)
        pop = GenericProbabilisticOptimizationProblem(ef, odd, df)

        start = time.time()
        rhc = RandomizedHillClimbing(hcp)
        fit = FixedIterationTrainer(rhc, it_count)
        fit.train()
        end = time.time()
        # print "Time -->", end - start
        value = ef.value(rhc.getOptimal())
        # print "RHC: " + str(value)

        results = {
            'num_iterations': it_count,
            'value': value,
            'time' : end - start
        }

        print 'RHC', param, results
        writer.writerow(results)

        # sa = SimulatedAnnealing(1E11, .95, hcp)
        # fit = FixedIterationTrainer(sa, it_count)
        # fit.train()
        # print "SA: " + str(ef.value(sa.getOptimal()))
        #
        # ga = StandardGeneticAlgorithm(200, 100, 10, gap)
        # fit = FixedIterationTrainer(ga, it_count)
        # fit.train()
        # print "GA: " + str(ef.value(ga.getOptimal()))
        #
        # mimic = MIMIC(200, 20, pop)
        # fit = FixedIterationTrainer(mimic, it_count)
        # fit.train()
        # print "MIMIC: " + str(ef.value(mimic.getOptimal()))
