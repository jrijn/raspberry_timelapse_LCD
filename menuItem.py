class MenuItem(object):

    items = {}

    def __init__(self, name, parent=None):
        self.name = (name, parent)
        self.parent = parent 
        self.children
        self.childNames
        self.siblings
        self.siblingNames
        self.allowedValues = [0]
        self.value = 0
        MenuItem.items[self._name] = self

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: tuple):
        name, parent = value  
        if isinstance(name, str):
            self._name = name
        elif isinstance(name, list):
            for i, j in enumerate(name):
                assert isinstance(j, str), "Not all list items are strings"
                if i == len(name)-1: self._name = j
                else: MenuItem(j, parent)

    @property
    def parent(self):
        if self._parent != None:
            return MenuItem.items[self._parent]
        else:
            return None

    @parent.setter
    def parent(self, value: str):
        self._parent = value

    @property
    def children(self):
        children = []
        for i in MenuItem.items.values():
            if i._parent == self.name:
                children.append(i)
        if len(children) > 0:
            return children
        else: 
            return None

    @property
    def childNames(self):
        if self.children != None:
            return [child.name for child in self.children]

    @property
    def siblings(self):
        siblings = []
        for i in MenuItem.items.values():
            if i._parent == self._parent:
                siblings.append(i)
        return siblings

    @property
    def siblingNames(self):
        return [sibling.name for sibling in self.siblings]

    @property
    def allowedValues(self):
        return self._allowedValues

    @allowedValues.setter
    def allowedValues(self, value: list):
        self._allowedValues = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: int):
        if value in self.allowedValues:
            self._value = value
        else:
            print("MenuItem.value = '{}' was not found in MenuItem.allowedValues.\n"
                  "MenuItem.value remains '{}'".format(value, self.value))

 
def newMenuItems(name, parent='root'):
    if isinstance(name, str):
        MenuItem(name, parent)
    elif isinstance(name, list):
        for i in name:
            assert isinstance(i, str), "Not all list items are strings"
            MenuItem(i, parent)
    else: 
        raise Exception("Parameter 'name' must be a string or a list of strings")


def main():
    MenuItem('timelapse settings')
    MenuItem('duration', 'timelapse settings')
    MenuItem('raspberry info')
    # newMenuItems(['# frames', 'frame interval'], 'timelapse settings')
    MenuItem(['IP address', 'camera status'], 'raspberry info')

    menu = MenuItem.items
    # print(menu[None].parent.name)
    print(menu.keys())
    # print(menu['timelapse settings'].children)
    print(menu['raspberry info'].childNames)
    # print(menu['duration'].siblings)
    print(menu['duration'].siblingNames)
    menu['duration'].value = 4
    print(menu['duration'].value)
    print(menu['duration'].allowedValues)
    menu['duration'].allowedValues = [0,1,2,3,4]
    print(menu['duration'].allowedValues)
    menu['duration'].value = 4
    print(menu['duration'].value)
    

if __name__ == "__main__":
    main()