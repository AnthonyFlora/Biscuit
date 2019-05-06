class Observable():
    def __init__(self, data=None):
        self.data = data
        self.observers = []

    def observe(self, observer):
        self.observers.append(observer)
        if self.data:
            observer(self.data)

    def update(self, data):
        self.data = data
        self.notify()

    def notify(self):
        [observer(self.data) for observer in self.observers]