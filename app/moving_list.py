# https://www.geeksforgeeks.org/python-find-most-frequent-element-in-a-list/

class MovingList:
    def __init__(self, window_len):
        self.values = []
        self.window_len = window_len

    def add(self, value):
        num_values = len(self.values)
        if num_values < self.window_len:
            self.values.append(value)
        else:
            self.values.pop(0)
            self.values.append(value)

    def get_most_common(self):
        dict = {}
        count, itm = 0, ''
        # for item in reversed(self.values):    # use oldest if a tie-breaker
        for item in self.values:                # use newest if a tie-breaker
            dict[item] = dict.get(item, 0) + 1
            if dict[item] >= count:
                count, itm = dict[item], item
        return (itm)

    def get_values(self):
        return self.values


# example usage
def main():
    values = ['rain', 'rain', 'sun', 'wind', 'wind', 'wind', 'wind', 'wind', 'hail']
    window_len = 5

    states = MovingList(window_len)

    for i in values:
        print('---')
        states.add(i)
        print(states.get_values())
        print(states.get_most_common())
        # moving_avg = s1.get_moving_average()
        # print('moving_average=' + moving_avg.__str__())


if __name__ == '__main__':
    main()

