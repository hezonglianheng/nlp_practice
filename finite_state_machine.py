import itertools
import my_queue


class State:
    id_iter = itertools.count()

    def __init__(self, accept=False):
        self.accept = accept  # 是否为可结束状态
        self.transition = set()  # 转换条件和下一个状态
        self.id = next(self.id_iter)  # 编号

    def add_transition(self, trans):
        self.transition.add(trans)  # trans是Transition类对象

    def step(self, ch:int):
        for t in self.transition:
            if t.min <= ch <= t.max:
                return t.to
        return None

    def append_string(self,s:str):
        current_state = self
        for ch in s:
            to = State()
            code = ord(ch)
            ts = Transition(to,code,code)
            current_state.add_transition(ts)
            current_state = to
        current_state.accept = True

    def append_char_range_plus(self,min:int,max:int):
        s2 = State(True)
        t = Transition(s2,min,max)
        self.transition.add(t)
        s2.transition.add(t)

    def __str__(self):
        line = 'state_id：'+str(self.id)
        return line


class Transition:
    def __init__(self, to: State, min_ch: int, max_ch: int = None):
        if max_ch is None:
            self.min = self.max = min_ch
        else:
            self.min = min_ch  # 皆为字符编码
            self.max = max_ch
        self.to = to


class Automaton:  # 有限状态机类
    def __init__(self,initial:State):
        self.initial = initial
        self.deterministic = True

    def get_accept_state(self) -> set:
        """返回所有可接受状态"""
        accepts = set()
        visited = set()
        work_list = my_queue.Queue()
        work_list.enqueue(self.initial)
        while work_list.length() > 0:
            s = work_list.dequeue()
            if s.accept:
                accepts.add(s)
            for t in s.transition:
                if t.to not in visited:
                    visited.add(t.to)
                    work_list.enqueue(t.to)
        return accepts

    def append_string(self,input:str):
        accept = self.get_accept_state()
        for new_start in accept:
            new_start.accept = False
            new_start.append_string(input)

    def append_char_range_plus(self,min:str,max:str):
        accept = self.get_accept_state()
        for new_start in accept:
            new_start.accept = False
            new_start.append_char_range_plus(ord(min),ord(max))

    class BasicAutomata:  # 包含方便创建有限状态机的辅助方法
        @staticmethod
        def make_char_change(min: str, max: str):
            s1 = State()
            s2 = State()
            s1.transition.add(Transition(s2, ord(min), ord(max)))
            a = Automaton(s1)
            return a

        @staticmethod
        def make_char_range_plus(min: str, max: str):
            s1 = State()
            s2 = State(True)
            t = Transition(s2, ord(min), ord(max))
            s1.transition.add(t)
            s2.transition.add(t)
            a = Automaton(s1)
            return a

    class BasicOperations:
        @staticmethod
        def run(a, s: str):
            p = a.initial
            for c in s:
                code = ord(c)
                q = p.step(code)
                if q is None:
                    return False
                p = q
            return p.accept


if __name__ == '__main__':
    auto = Automaton.BasicAutomata.make_char_range_plus('0','9')
    auto.append_string('年')
    auto.append_char_range_plus('0','9')
    auto.append_string('月')
    text = '我在2020年11月'
    for i in range(len(text)):
        piece = text[i:]
        result = Automaton.BasicOperations.run(auto, piece)
        print(piece, result)
