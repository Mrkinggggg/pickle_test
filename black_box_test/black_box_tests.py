# 用例来源参考...(废案)
# import hashlib
# import pickle
# import os
#
# def hash_pickle(data):
#     pickled_data = pickle.dumps(data)
#     return hashlib.sha256(pickled_data).hexdigest()
#
# if __name__ == "__main__":
#
#     # case 1
#     print('\ncase 1:')
#     set1 = {'banana','apple','pear'}
#     set2 = {'apple','pear','banana'}
#     print(hash_pickle(set1))
#     print(hash_pickle({'banana'}))
    # print(hash_pickle(set2))

    # # case 2
    # print('\ncase 2:')
    # dict1 = {'province':'Zhejiang'}
    # print(hash_pickle(dict1))
    # dict1['city'] = 'hangzhou'
    # print(hash_pickle(dict1))
    # del dict1['city']
    # print(hash_pickle(dict1))
    # dict2 = {'city':'hangzhou','province':'Zhejiang'}
    # print(hash_pickle(dict2))
    # # print({'p':'1','c':'2'} == {'c':'2','p':'1'})
    # # print(hashlib.sha256(pickle.dumps({'p':'1','c':'2'})).hexdigest() == hashlib.sha256(pickle.dumps({'c':'2','p':'1'})).hexdigest())
    #
    # # case 3
    # print('\ncase 3:')
    # a = []
    # a.append(a)
    # b = []
    # b.append(b)
    # print(hash_pickle(a))
    # print(hash_pickle(b))
    #
    # # case 4
    # print('\ncase 4:')
    # f1 = 0.1
    # f2 = 0.2
    # f3 = 0.3
    # f4 = f1 + f2
    # print(f4)
    # print(f4 == 0.3)
    # print(f4 == f3)
    # print(hash_pickle(f1))
    # print(hash_pickle(f2))
    # print(hash_pickle(f3))
    # print(hash_pickle(f4))
    # print(hash_pickle(f1+f2))
    #
    # # case 5
    # print('\ncase 5:')
    # maxNum = 1e323
    # maxNum2 = 1e322
    # print(hash_pickle(maxNum))
    # print(hash_pickle(maxNum2))
    #
    # # case 6
    # print('\ncase 6:')
    # f1 = 1.20
    # f2 = 1.2
    # print(hash_pickle(f1))
    # print(hash_pickle(f2))
    #
    # # case 7
    # print('\ncase 7:')
    #
    # def n1():
    #     print('hello')
    #
    # def n2():
    #     print('helloa')
    #     qa =6
    #     print(qa)
    #
    # print(n1() == n2())
    # print(hash(n1()) == hash(n2()))
    # print(hash_pickle(n1()))
    # print(hash_pickle(n2()))
    #
    # # case 8
    # print('\ncase 8:')
    # path1 = os.path.join('home', 'study', 'python')
    # path2 = r'home/study/python'
    # path3 = r'home\study\python'
    # print(hash_pickle(path1))
    # print(hash_pickle(path2))
    # print(hash_pickle(path3))
    #
    # # case 9
    # print('\ncase 9:')
    # lf1 = 1.0000000000000001
    # lf2 = 1.0
    # print(lf1)
    # print(lf2)
    # print(lf1 == lf2)
    # print(hash_pickle(lf1))
    # print(hash_pickle(lf2))
    #
    # # case 10
    # print('\ncase 10:')
    # class Person:
    #     pass
    # student = Person()
    # # student.x = 1
    # # student.y = 2
    # teacher = Person()
    # # teacher.y = 2
    # # teacher.x = 1
    # print(hash_pickle(student))
    # print(hash_pickle(teacher))
    #
    # # case 11
    # print('\ncase 11:')
    # class Student(Person):
    #     def __init__(self, name):
    #         self.name = name
    # class Teacher(Person):
    #     def __init__(self, name):
    #         self.name = name
    # student = Student('Alice')
    # teacher = Teacher('Alice')
    # print(hash_pickle(student))
    # print(hash_pickle(teacher))
    # student2 = Student('Bob')
    # print(hash_pickle(student2))
    # student.age = 20
    # print(hash_pickle(student))
    #
    # # case 12
    # print('\ncase 12:')
    # print(hash_pickle())