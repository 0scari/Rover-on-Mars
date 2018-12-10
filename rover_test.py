#!/usr/bin/env python3
import subprocess


def runTest(source):
    newSource = ""

    # strip out existing FACTS with rock positions
    for line in source:
        if not line.lstrip().startswith("FACT ROCK "):
            newSource += line.lstrip()

    # FACTS that will be injected in test file
    testRocks = [
        'FACT ROCK 2 6 "False";\n',
        'FACT ROCK 3 1 "False";\n',
        'FACT ROCK 6 1 "False";\n',
        'FACT ROCK 5 3 "False";\n',
        'FACT ROCK 7 5 "True";\n',
        'FACT ROCK 3 2 "True";\n',
        'FACT ROCK 2 2 "True";\n',
        'FACT ROCK 3 3 "True";\n'
    ]
    testRocks = ''.join(testRocks)

    # inject test facts and create file
    pos = newSource.find('FACTS:\n')
    newSource = newSource[:pos + len('FACTS:\n')] + testRocks + newSource[pos + len('FACTS:\n'):]
    open('agent_test.jam', 'w').write(newSource)

    # get output from jamagent execution with test facts
    output = subprocess.check_output(['jamagent agent_test.jam'],
                          shell=True,
                          universal_newlines=True)  # transform STDOUT to str

    # define expected strings to be present in the outpt
    expectedOutputs = [
        'Total moves were made: 111',
        'Rock with no water at: 2 | 6',
        'Rock with no water at: 3 | 1',
        'Rock with no water at: 5 | 3',
        'Rock with no water at: 6 | 1',
        'Rock with water at: 2 | 2',
        'Rock with water at: 3 | 3',
        'Rock with water at: 3 | 2',
        'Rock with water at: 7 | 5',
    ]

    # test!
    for test in expectedOutputs:
        if output.find(test) == -1:
            return False

    return True

if __name__ == '__main__':
    source = open("rover.jam", "r")
    if runTest(source):
        print('Testing successful')
    else:
        print('Testing failed')
    source.close()


