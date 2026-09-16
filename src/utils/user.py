from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    teamname: str
    token: str

    # Override equality operator to only check username and teamname
    def __eq__(self, other):
        if not isinstance(other, User):
            return NotImplemented

        return self.username == other.username and self.teamname == other.teamname