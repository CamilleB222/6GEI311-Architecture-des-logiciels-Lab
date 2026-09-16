class Admin:
    _admin_id : int
    _name : str
    _email : str


    def __init__(self, admin_id : int, name : str, email : str):
        self._admin_id = admin_id
        self._name = name
        self._email = email


    @property
    def admin_id(self):
        return self._admin_id

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email
    