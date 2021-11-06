from .responses import missing_parameter

class ParamParser:

    def __init__(self, required_params, request):

        self.params = {}

        for param in required_params:
            if not request.get(param):
                self.correct = False
                self.response = missing_parameter(param)
                return
            else:
                self.correct = True
                self.params[param] = request.get(param)
        
    def get(self, param):
        return self.params[param]