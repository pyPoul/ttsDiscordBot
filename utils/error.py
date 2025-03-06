
class _Null(Exception) :
    pass


NULL: _Null = _Null()


class NonAuthorizedException(Exception) :

    def __init__(self, s: str) -> None :
        super().__init__(s)


class AlreadyConnectedException(Exception) :

    def __init__(self, s: str) :
        super().__init__(s)


class UserNotConnectedException(Exception) :

    def __init__(self, s: str) :
        super().__init__(s)
