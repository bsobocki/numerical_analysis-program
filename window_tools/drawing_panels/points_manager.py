class Points_Manager():
    def __init__(self):
        self._visibility = True
        self._objects = [[]]

    def objects(self):
        return self._objects

    def are_visible(self):
        return self._visibility


    def new_object(self):
        self._objects.append([])

    def add_objects(self, objects):
        self._objects += objects
    
    def add_point(self, x, y, color):
        index = len(self._objects)-1
        self._objects[index].append([x,y,color])


    def reset(self):
        for obj in self._objects:
            for i in range(0, len(obj)):
                del obj[-1]

    def switch_visibility(self):
        self._visibility = not self._visibility

    def delete_last_point(self):
        if len(self._objects) > 0 and len(self._objects[0]) > 0:
            if len(self._objects[-1]) >0 : del self._objects[-1][-1]
            if len(self._objects) > 1 and len(self._objects[-1]) == 0 :  del self._objects[-1]
