#! /usr/bin/env python

import pygame
import time
import yaml
import os
from Railway.RailwayElements import RailwayElements
from Railway.Rail import Rail
from Railway.TrainStop import TrainStop
from Train.Train import Train

trains = list()
rails = list()
inputFile = r"input_file.txt"

def readInput(trains, rails):
    f = open(inputFile, "r")
    lines = f.readlines()
    f.close()
    if len(lines)>2:
        lines.pop(0)
        lines.pop(0)
        parseInput(lines)
        aux = open(inputFile, "w")
        aux.write("To add a train type ADD train color rail number start stop end stop\n")
        aux.write("To set new path for train type MOVE train color start stop end stop\n")
        aux.close()


def parseInput(input):
    for command in input:
        commands = command.strip().split(" ")
        train_name = commands[1]
        if commands[0] == 'ADD':
            rail, start_index, end_index = rails[int(commands[2])], int(commands[3]), int(commands[4])
            if start_index>(len(rail.stops)-1) or end_index>(len(rail.stops)-1):
                print("ERROR NO SUCH PATH")
            else:
                train = Train(train_name, rail, rail.stops[start_index], rail.stops[end_index])
                trains.append(train)

        if commands[0] == 'MOVE':
            start_index, end_index = int(commands[2]), int(commands[3])
            train = checkIfExists(train_name)
            if train !=None:
                if train.current_stop.name != train.Rail.stops[start_index].name:
                    #print(train.x, train.y, train.current_stop.name, train.Rail.stops[start_index].name)
                    print("ERROR wrong entry")
                    break
                else:
                    trains.remove(train)
                    new_train = Train(train.name, train.Rail, train.Rail.stops[start_index], train.Rail.stops[end_index])
                    trains.append(new_train)

            else:
                print("Error no such train")
        if commands[0] == 'STOP':
            train = checkIfExists(train_name)
            if train !=None:
                print("STOPPED", train_name)
                train.start_stop = train.current_stop
                train.x, train.y = train.current_stop.Rect[0], train.current_stop.Rect[1]
                train.next_stop = None
                train.end_stop = None

def checkIfExists(target_train_name):
    for train in trains:
        if target_train_name == train.name:
            return train
    return None

def update():
    for train in trains:
        train.update()

def checkCollisions():
    occurences = dict()
    for train in trains:
        if train.current_stop!=None and train.next_stop !=None:
             aSegment = train.current_stop.name + " " + train.next_stop.name
             bSegment = train.next_stop.name + " " + train.current_stop.name
             if aSegment not in occurences and bSegment not in occurences :
                occurences[aSegment] = 1
             else:
                print("ERROR", aSegment, ' is already busy')
                #train.current_stop = train.start_stop
                train.start_stop = train.current_stop
                train.x, train.y = train.current_stop.Rect[0], train.current_stop.Rect[1]
                train.next_stop = None
                train.end_stop = None
                return True
    return False


def draw(screen):
    screen.fill((255, 255, 255))  # refreshes the screen
    for rail in rails:
        rail.draw()
    for train in trains:
        train.draw(screen)


# function for reading yaml file
def read_yaml1():
    list_of_rails = list()
    with open(r"routes/route_2.yaml") as stream:
        data_loaded = yaml.safe_load(stream)
        for rail in data_loaded['data']:
            rail_elements = RailwayElements()
            ordered_elements = dict() # will need it for calculating path
            allstops = list()
            # produces trainstops classes
            for stops in data_loaded['data'][rail]['stops']:
                stop = TrainStop(stops, data_loaded['data'][rail]['stops'][stops]['duration'], data_loaded['data'][rail]['stops'][stops]['part_of'], data_loaded['data'][rail]['stops'][stops]['angle'])
                # stop.setRect sets a Rect that will be used for visualising
                stop.setRect(data_loaded['data'][rail]['stops'][stops]['location'], data_loaded['data'][rail]['stops'][stops]['height'],
                         data_loaded['data'][rail]['stops'][stops]['width'])
                allstops.append(stop)
            # produces railwayElements class
            for elements in data_loaded['data'][rail]['elements']:
                if elements.startswith('arc'):
                    rail_elements.arcs.append(data_loaded['data'][rail]['elements'][elements])
                elif elements.startswith('line'):
                    rail_elements.lines.append(data_loaded['data'][rail]['elements'][elements])
                ordered_elements[elements] = data_loaded['data'][rail]['elements'][elements]
            color = data_loaded['data'][rail]['color']
            x = Rail(allstops, rail_elements.returnDict(), ordered_elements, screen, color)
            list_of_rails.append(x)
    return list_of_rails

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((600, 500))
    screen.fill((255, 255, 255))
    # makes stops and elements from yaml file
    rails = read_yaml1()

    #initializes input file
    f = open(inputFile, "w")
    f.write("To add a train type ADD train color rail number start stop end stop\n")
    f.write("To set new path for train type MOVE train color start stop end stop\n")
    f.close()

    done, tik = False, 0
    clock = pygame.time.Clock()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        #time.sleep(0.05)  # slows movement down so it can be visible
        dt = clock.tick(25)
        draw(screen)
        update()
        if checkCollisions() == True:
            print("collision")
        if tik%7 == 0:
            readInput(trains, rails)
        pygame.display.flip()
        tik = tik + 1
    pygame.quit()
