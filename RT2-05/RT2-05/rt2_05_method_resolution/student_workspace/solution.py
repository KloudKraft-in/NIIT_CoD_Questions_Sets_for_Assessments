import sys

class Parent1:
    def fun1(self):
        print("Parent1 fun1")
    def fun2(self):
        print("Parent1 fun2")

class Parent2:
    def fun1(self):
        print("Parent2 fun1")
    def fun2(self):
        print("Parent2 fun2")

class Child(Parent1, Parent2):
    # Complete the class Child below
    def fun1(self):
        # Implementation here
        pass

    def fun2(self):
        # Implementation here
        pass

def main():
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
    
    try:
        n = int(input_data[0].strip())
        c = Child()
        
        for i in range(1, n + 1):
            if i >= len(input_data): break
            cmd = int(input_data[i].strip())
            if cmd == 1:
                c.fun1()
            elif cmd == 2:
                c.fun2()
    except Exception as e:
        raise e

if __name__ == "__main__":
    main()
