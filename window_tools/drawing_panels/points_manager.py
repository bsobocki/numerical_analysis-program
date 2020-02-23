from window_tools.drawing_panels.point import Point

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
    
    def add_point(self, x, y):
        index = len(self._objects)-1
        self._objects[index].append((x,y))


    def reset(self):
        self._objects = [[]]

    def switch_visibility(self):
        self._visibility = not self._visibility

    def delete_last_point(self):
        if len(self._objects) > 0 and len(self._objects[0]) > 0:
            if len(self._objects[-1]) >0 : del self._objects[-1][-1]
            if len(self._objects) > 1 and len(self._objects[-1]) == 0 :  del self._objects[-1]
