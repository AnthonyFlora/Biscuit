import math

class RunningAverage:
  def __init__(self, window_size):
    self.window_size = window_size
    self.samples_cartesian_x = [0 for i in range(window_size)]
    self.samples_cartesian_y = [0 for i in range(window_size)]
    self.sample_index = 0

  def clear(self):
    self.samples_cartesian_x = [0 for i in range(self.window_size)]
    self.samples_cartesian_y = [0 for i in range(self.window_size)]
    self.sample_index = 0

  def update(self, sample_degrees):
    sample_radians = math.radians(sample_degrees)
    sample_cartesian_x = math.cos(sample_radians)
    sample_cartesian_y = math.sin(sample_radians)
    self.samples_cartesian_x[self.sample_index] = sample_cartesian_x
    self.samples_cartesian_y[self.sample_index] = sample_cartesian_y
    sum_cartesian_x = sum(self.samples_cartesian_x)
    sum_cartesian_y = sum(self.samples_cartesian_y)
    average_radians = math.atan2(sum_cartesian_y, sum_cartesian_x)
    average_degrees = math.degrees(average_radians)
    self.sample_index = (self.sample_index + 1) % self.window_size
    print('Input: %0.6f, Average After: %0.6f' % (sample_degrees, average_degrees))
    return average_degrees

if __name__ == '__main__':

    print('Test trivial case..')
    ra = RunningAverage(3)
    ra.update(20.0)
    ra.update(20.0)
    ra.update(20.0)
    ra.update(20.0)

    print('Test growing case..')
    ra = RunningAverage(3)
    ra.update(20.0)
    ra.update(40.0)
    ra.update(60.0)
    ra.update(80.0)

    print('Test opposite case..')
    ra = RunningAverage(3)
    ra.update(90.0)
    ra.update(270.0)
    ra.update(90.0)
    ra.update(270.0)

    print('Test wraparound case..')
    ra = RunningAverage(3)
    ra.update(20.0)
    ra.update(340.0)
    ra.update(20.0)
    ra.update(340.0)