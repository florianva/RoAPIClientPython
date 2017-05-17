from __future__ import print_function

import grpc

from protoClassClient import hcfi_pb2_grpc
from protoClassClient import hcfi_pb2

from Eval import Optimisation
import matplotlib.pyplot as plt

Iterations = []
Fitness = []

def PrintGraph():
    plt.plot(Iterations, Fitness, label='Fitness en fonction du nombre d\ iterations')
    plt.xlabel('Iterations')
    plt.ylabel('Fitness')
    plt.show()


def run(fileInName):
  channel = grpc.insecure_channel('127.0.0.1:50051')
  stub = hcfi_pb2_grpc.HillClimberServiceStub(channel)

  r = Optimisation(fileInName)
  firstEval = r.eval()
  #print(str(r))
  print(firstEval)

  Iterations.append(1)
  Fitness.append(firstEval)

  #Initialisation de la transaction
  #print("Init the transaction : ")
  response = stub.InitTransaction(hcfi_pb2.InitTransactionRequest(customer='Florian', algorithm="hillclimber_first_improvement", solutionSize=r.n, fitness=firstEval, solution=str(r)))
  #print("Client received Id : " + response.id)
  #print("Client received Solution : " + response.solution)


  Optimisation.newSolution(r, response.solution)
  newEval = r.eval()
  print(newEval)

  Iterations.append(2)
  Fitness.append(newEval)


  for i in range(2,1000):

    #print("Send fitness for the solution received : ")
    response = stub.SendFitness(hcfi_pb2.FitnessRequest(id=response.id, fitness=newEval, solution=response.solution))
    #print("Client received Id : " + response.id)
    #print("Client received Solution : " + response.solution)

    Optimisation.newSolution(r, response.solution)
    newEval = r.eval()
    print(newEval)

    Iterations.append(i)
    Fitness.append(newEval)

  stop = stub.StopTransaction(hcfi_pb2.StopRequest(id=response.id, message='done'))
  print("fin : ")
  print(stop.fitness)
  print(stop.solution)

if __name__ == '__main__':
  run(fileInName="coeff.txt")
  PrintGraph()
