from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name

        self._members = []

    def _generateId(self):
        return randint(0, 99999999)

    def add_member(self, member):
        if "id" not in member or member["id"] is None:
            member["id"] = self._generateId()
        member["last_name"] = self.last_name
        self._members.append(member)
        return member

    def delete_member(self, id):
        for index, member in enumerate(self._members):
            if member["id"] == id:
                del self._members[index]
                return True
        return False

    def update_member(self, member):
        for index, current_member in enumerate(self._members):
            if current_member["id"] == member.get("id"):
                self._members[index].update(member)
                self._members[index]["last_name"] = self.last_name
                return self._members[index]
        return None

    def get_member(self, id):
        for member in self._members:
            if member["id"] == id:
                return member
        return None

    def get_all_members(self):
        return self._members
