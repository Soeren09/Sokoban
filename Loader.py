import io    



class CreateMap:
    def __init__(self, name):
        self.name = name

        with open(self.name, 'r') as file:
            for line in file:   
                if (line[0] == 'X'):
                    size = len(line)

                    for char in line:
                        print(char)

                    print(line[0], size)




p = CreateMap("/home/soeren/Git/Sokoban/2018-competation-map_2018.txt")

