class IdCannotChengedError(Exception):
    pass

class AgentNotActiveError(Exception):
    pass

class AgentCannotHaveThreeOpentasksError(Exception):
    pass

class MissionOnlyForCommanderError(Exception):
    pass

class MissionStatusError(Exception):
    pass