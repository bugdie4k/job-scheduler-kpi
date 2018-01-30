from queue import Queue
from random import randint
import munkres as mnk
from math import ceil

_max_complexity = 12  # works
_max_productivity = 4 # works/time
# to find time do complexity/productivity
_q_sz = 40
_n = 10
_state_history = []

# queue
class Q:
    def __init__(self, size):
        self.q = Queue(size)
        for i in range(size):
            self.q.put(T(i, randint(1, _max_complexity)))

    def get(self):
        return self.q.get()

    def task_done(self):
        return self.q.task_done()

    def prn(self):
        print("Queue")
        print("       ^^^")
        for i, t in enumerate(list(self.q.queue)):
            print("el# {:<3d} : ".format(i), end='')
            t.prn()
        print("       ^^^")

# processor
class P:
    def __init__(self, id, prod):
        self.id = id
        self.prod = prod
        self.taken_by = None
        self.time_left = 0

    def prn(self, end='\n'):
        print('prid {:<3d} : tid {:<3d} : time left {:<3d}'.format(self.id, -1 if self.taken_by is None else self.taken_by.id, self.time_left), end=end)

# task
class T:
    def __init__(self, id, complexity):
        self.id = id
        self.complexity = complexity

    def prn(self, end='\n'):
        print('tid {:<3d} : {:<3d}'.format(self.id, self.complexity), end=end)

class State:
    def __init__(self):
        self.timer = None
        self.q = None
        self.N = None
        self.procs = None
        self.done = None

    @staticmethod
    def cpy(self):
        obj = State()
        obj.timer = self.timer
        obj.q = self.q
        obj.N = self.N
        obj.procs = self.procs
        obj.done = self.done
        obj.first_iter = self.first_iter
        return obj

    def new(self, q_size, N):
        global _state_history
        self.timer = 0
        self.q = Q(q_size)
        self.N = N
        self.procs = list(map(lambda p: P(p[0], p[1]), enumerate([randint(1, _max_productivity) for i in range(N)])))
        self.done = []
        self.first_iter = True
        _state_history.append(self.cpy(self))
        return self

    @staticmethod
    def prn_procs(procs):
        print("Processors")
        for p in procs:
            p.prn()

    def dump(self):
        print("STATE on ", self.timer)
        self.q.prn()
        self.prn_procs(self.procs)

    def procs_free(self):
        free_procs = []
        for p in self.procs:
            if p.taken_by is None:
                free_procs.append(p)
        return free_procs

    def make_matrix(self):
        def get_tsk():
            if (len(self.q.q.queue) > 0):
                val = self.q.get()
                self.q.task_done()
                return val
            else:
                return None

        free_procs = self.procs_free()
        self.tasks = [ get_tsk() for i in range(len(free_procs))]

        matr_i_p_map = {}
        matr_j_t_map = {}
        
        matr = []
        for i, p in enumerate(free_procs):
            matr_i_p_map.update({i: p.id})
            row = []
            for j, t in enumerate(self.tasks):
                if t is not None:
                    matr_j_t_map.update({j: t.id})
                    row.append(t.complexity / p.prod)
            matr.append(row)

        return matr, matr_i_p_map, matr_j_t_map

    def get_p_by_id(self, id):
        for p in self.procs:
            if p.id == id:
                return p

    def get_t_by_id(self, id):
        for t in self.tasks:
            if t is not None:
                if t.id == id:
                    return t

    @staticmethod
    def pmatr(matr, matr_i_p_map, matr_j_t_map):
        print('   - MATRIX')
        print('     tasks   ', end='')
        for j in (range(len(matr[0]))):
            print(j, ' ', end='')
        print()
        print('     procs  +', end='')
        for j in (range(len(matr[0]))):
            print('---', end='')
        print()
        for i, row in enumerate(matr):
            print('         ', i, '|', end='')
            for el in row:
                print('{:<3d}'.format(int(el)), end='')
            print()
                
            
    def plan(self):
        matr, matr_i_p_map, matr_j_t_map = self.make_matrix()

        self.pmatr(matr, matr_i_p_map, matr_j_t_map)
        
        indexes = mnk.Munkres().compute(matr)
        # print(indexes)
        print("   - HOW IT WAS SOLVED")
        for row, col in indexes:
            self.get_p_by_id(matr_i_p_map[row]).taken_by = self.get_t_by_id(matr_j_t_map[col])
            self.get_p_by_id(matr_i_p_map[row]).time_left = ceil(matr[row][col])
            print("     (", row, ",", col, ") --> ", ceil(matr[row][col]), " : ( prid=", matr_i_p_map[row], ", tid=", matr_j_t_map[col], ")")

    def do(self):
        empty = True
        for p in self.procs:
            if p.taken_by is not None:
                empty = False
                if p.time_left == 0:
                    self.done.append(p.taken_by)
                    p.taken_by = None
                else:
                    p.time_left -= 1
        return empty

    def iter(self, num=1):
        for i in range(num):
            self.timer += 1
            print("ITERATING ", self.timer - 1, " -> ", self.timer)
            empty = self.do()
            if empty and not self.first_iter:
                print("SORRY, HAVE NOTHING TO DO")
            else:
                print(" - DOING")
                if len(list(self.q.q.queue)) > 0:
                    if len(self.procs_free()) > 0:
                        print(" - PLANNING")
                        self.plan()
                    else:
                        print(" - WANTED TO PLAN, BUT NO FREE PROCESSORS")
                else:
                    print(" - WANTED TO PLAN, BUT QUEUE IS EMPTY")
            

s = State().new(_q_sz, _n)
# print(s)

def new():
    global s
    s = State().new(_q_sz, _n)
    return s

def dump():
    global s
    s.dump()

def iter(num=1):
    global s
    s.iter(num)
    return s

def iterdump(num=1):
    iter(num)
    dump()

def newdumpiter(num=1):
    new()
    dump()
    iter(num)
    
def newdumpiterdump(num=1):
    new()
    dump()
    iter(num)
    dump()
        
# def main():
    # s.dump()
    # s.dump()

# if __name__ == "__main__":
#     main();

# exec(open("lab4.py").read())

