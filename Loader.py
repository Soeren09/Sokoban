import io    


with open(r"C:\Users\Soeren\Documents\GitHub\Sokoban\2019_Solution.txt", 'r') as f:
    with open(r"C:\Users\Soeren\Documents\GitHub\Sokoban\2019_Solution2.txt", 'w') as f1:

        new = []
        c0 = f.read(1)

        while True:
            c1 = f.read(1)
            if not c0:
                print("End of file")
                break
            
            if ( (ord(c0) >= 65 and ord(c0) <= 90) and (ord(c1) >= 65 and ord(c1) <= 90) ):   # If Both are upp case letters
                new.append(c0.lower())

                
            elif ( (ord(c0) >= 65 and ord(c0) <= 90) and not(ord(c1) >= 65 and ord(c1) <= 90) ):   # If current letter is upeprcase and the next now
                new.append(c0.lower())
                new.append('x')
                

            else:   # Current letter is lowercase
                new.append(c0)

            c0 = c1


        f1.write(''.join(new))

        print(str(new))

# class CreateMap:
#     def __init__(self, name):
#         self.name = name

#         with open(self.name, 'r') as file:
#             for line in file:   
#                 if (line[0] == 'X'):
#                     size = len(line)

#                     for char in line:
#                         print(char)

#                     print(line[0], size)




# p = CreateMap("/home/soeren/Git/Sokoban/2018-competation-map_2018.txt")

