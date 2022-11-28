class TargetValueMapping:
    def __init__(self):
        self.neg :int = 0
        self.pos :int = 1

    def to_dict(self):
        return self.__dict__
    
    def reverse_mapping(self):
        map_reponse =  self.to_dict()
        return dict(zip(map_reponse.values(),map_reponse.keys()))
        