
class Person:
    
    def __init__(self, name, job=None, pay=0): # Конструктор принимает 3 аргумента
        self.name = name # Заполняет поля при создании
        self.job = job # self – новый экземпляр класса
        self.pay = pay
        
    def lastName(self): # Методы, реализующие поведение экземпляров
        return self.name.split()[-1] # self – подразумеваемый экземпляр
    
    def giveRaise(self, percent):
        self.pay = int(self.pay * (1 + percent))
        
    def __str__(self): # Добавленный метод
        return '[Person: %s, %s]' % (self.name, self.pay) # Строка для вывода


class Manager(Person):
    
    def __init__(self, name, pay): # Переопределенный конструктор
        Person.__init__(self, name, 'mgr', pay)
    
    def giveRaise(self, percent, bonus=.10):
        Person.giveRaise(self, percent + bonus)


        
if __name__ == '__main__': # Только когда файл запускается для тестирования
    # реализация самотестирования
    bob = Person('Bob Smith')
    sue = Person('Sue Jones', job='dev', pay=100000)
    print(bob)
    print(sue)
    # print(bob.name.split()[-1]) # Извлечь фамилию
    # sue.pay *= 1.10 # Повысить зарплату
    # print(sue.pay)
    print(bob.lastName(), sue.lastName())
    sue.giveRaise(.10) # операций используются методы
    print(sue.pay)
    # print(sue)
    tom = Manager('Tom Jones', 50000)
    tom.giveRaise(.10) # Вызов адаптированной версии
    print(tom.lastName()) # Вызов унаследованного метода
    print(tom.job) 
    
    print('--All three--')
    for object in (bob, sue, tom): # Обработка объектов обобщенным способом
        object.giveRaise(.10) # Вызовет метод giveRaise этого объекта
        print(object) 
        

        