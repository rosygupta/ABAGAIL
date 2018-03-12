# traveling salesman algorithm implementation in jython
# This also prints the index of the points of the shortest route.
# To make a plot of the route, write the points at these indexes 
# to a file and plot them in your favorite tool.
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
import dist.DiscretePermutationDistribution as DiscretePermutationDistribution
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
import opt.example.TravelingSalesmanEvaluationFunction as TravelingSalesmanEvaluationFunction
import opt.example.TravelingSalesmanRouteEvaluationFunction as TravelingSalesmanRouteEvaluationFunction
import opt.SwapNeighbor as SwapNeighbor
import opt.ga.SwapMutation as SwapMutation
import opt.example.TravelingSalesmanCrossOver as TravelingSalesmanCrossOver
import opt.example.TravelingSalesmanSortEvaluationFunction as TravelingSalesmanSortEvaluationFunction
import shared.Instance as Instance
import util.ABAGAILArrays as ABAGAILArrays

from array import array
import csv





"""
Commandline parameter(s):
    none
"""


optalgs = ['GA']

OA = {
    'RHC': RandomizedHillClimbing,
    'GA': StandardGeneticAlgorithm,
    'SA': SimulatedAnnealing
}

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
    output_filename = 'TSP %s-%s.csv' % ('GA', identifier['GA'](param))
    csv_file = open(output_filename, 'w')
    fields = ['num_iterations', 'value', 'time']
    writer = csv.DictWriter(csv_file, fieldnames=fields)
    writer.writeheader()
    for num_iterations in iterations:

        N = 50
        random = Random()

        points = [[0 for x in xrange(2)] for x in xrange(N)]
        for i in range(0, len(points)):
            points[i][0] = random.nextDouble()
            points[i][1] = random.nextDouble()


        ef = TravelingSalesmanRouteEvaluationFunction(points)
        odd = DiscretePermutationDistribution(N)
        nf = SwapNeighbor()
        mf = SwapMutation()
        cf = TravelingSalesmanCrossOver(ef)
        hcp = GenericHillClimbingProblem(ef, odd, nf)
        gap = GenericGeneticAlgorithmProblem(ef, odd, mf, cf)

        start = time.time()
        ga = StandardGeneticAlgorithm(param[0], param[1], param[2], gap)
        fit = FixedIterationTrainer(ga, num_iterations)
        fit.train()
        value = str(ef.value(ga.getOptimal()))
        print "GA Inverse of Distance: " + value
        end = time.time()
        print "Route:"
        path = []
        for x in range(0, N):
            path.append(ga.getOptimal().getDiscrete(x))
        print path
        print "Time -->", end - start

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

# start = time.time()
# sa = SimulatedAnnealing(1E12, .999, hcp)
# fit = FixedIterationTrainer(sa, 200000)
# fit.train()
# print "SA Inverse of Distance: " + str(ef.value(sa.getOptimal()))
# end = time.time()
# print "Route:"
# path = []
# for x in range(0,N):
#     path.append(sa.getOptimal().getDiscrete(x))
# print path
# print "Time -->", end - start
#
# start = time.time()
# ga = StandardGeneticAlgorithm(2000, 1500, 250, gap)
# fit = FixedIterationTrainer(ga, 1000)
# fit.train()
# print "GA Inverse of Distance: " + str(ef.value(ga.getOptimal()))
# end = time.time()
# print "Route:"
# path = []
# for x in range(0,N):
#     path.append(ga.getOptimal().getDiscrete(x))
# print path
# print "Time -->", end - start
#
# # for mimic we use a sort encoding
# ef = TravelingSalesmanSortEvaluationFunction(points);
# fill = [N] * N
# ranges = array('i', fill)
# odd = DiscreteUniformDistribution(ranges);
# df = DiscreteDependencyTree(.1, ranges);
# pop = GenericProbabilisticOptimizationProblem(ef, odd, df);
#
# start = time.time()
# mimic = MIMIC(500, 100, pop)
# fit = FixedIterationTrainer(mimic, 1000)
# fit.train()
# print "MIMIC Inverse of Distance: " + str(ef.value(mimic.getOptimal()))
# end = time.time()
# print "Route:"
# path = []
# optimal = mimic.getOptimal()
# fill = [0] * optimal.size()
# ddata = array('d', fill)
# for i in range(0,len(ddata)):
#     ddata[i] = optimal.getContinuous(i)
# order = ABAGAILArrays.indices(optimal.size())
# ABAGAILArrays.quicksort(ddata, order)
# print order
# print "Time -->", end - start
