from sys import argv

class Unique_Set():
    
    def unique_filter(self, this_list):
        newset=set()
        for i in this_list:
            newset.add(i)
        return newset

if __name__ == '__main__':
    u=Unique_Set()
    filename=argv[1]
    with open(filename, 'r+') as file:
        file_list=[]
        for line in file:
            file_list.append(line)
        print(len(file_list))
        newset=u.unique_filter(file_list)
        file_list=list(newset)
        print (len(file_list))
        file.seek(0)
        for i in file_list:
            file.write(i)
        file.truncate()
