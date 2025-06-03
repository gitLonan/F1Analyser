


# class Session:
#     def __init__(self, session_key, meeting_key):
#         self.session_key = session_key
#         self.meeting_key = meeting_key






class SetParam:
    session_key = 0
    meeting_key = 0

    meeting_key_attr = ''
    session_key_attr = ''

    call_again = False

    list_meeting_key = []
    list_session_key = []
    
    list_driver_numbers = []
    index_for_selecting_drivers = []
    drivers = []

    @classmethod
    def set_session_key(cls, key: str):
        cls.session_key = key

    @classmethod
    def set_meeting_key(cls, key: str):
        cls.session_key = key

    @classmethod
    def set_meeting_key_list(cls, key_list: list[str]):
        cls.list_meeting_key = key_list
    
    @classmethod
    def set_session_key_list(cls, key_list: list[str]):
        cls.list_session_key = key_list

#Ako mislim da naapravim da je svaki vozac svoj objekat, mogao bih to preko ovih classmethod funckija. Tako sto se objekat kreira kad se
#pozove funkcija i to je to, sa svim parametrima, da li to znaci da mi treba linked list ? ce vidimo 



    
    

    
