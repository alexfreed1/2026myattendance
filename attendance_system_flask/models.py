from database import get_supabase_client

class BaseModel:
    def __init__(self, table_name):
        self.table_name = table_name
        self.supabase = get_supabase_client()

    def get_all(self):
        response = self.supabase.from_(self.table_name).select("*").execute()
        return response.data

    def get_by_id(self, id):
        response = self.supabase.from_(self.table_name).select("*").eq("id", id).execute()
        return response.data[0] if response.data else None

    def create(self, data):
        response = self.supabase.from_(self.table_name).insert(data).execute()
        return response.data[0] if response.data else None

    def update(self, id, data):
        response = self.supabase.from_(self.table_name).update(data).eq("id", id).execute()
        return response.data[0] if response.data else None

    def delete(self, id):
        response = self.supabase.from_(self.table_name).delete().eq("id", id).execute()
        return response.data

class Department(BaseModel):
    def __init__(self):
        super().__init__("departments")

class Class(BaseModel):
    def __init__(self):
        super().__init__("classes")

class Student(BaseModel):
    def __init__(self):
        super().__init__("students")

class Unit(BaseModel):
    def __init__(self):
        super().__init__("units")

class Trainer(BaseModel):
    def __init__(self):
        super().__init__("trainers")

class ClassUnit(BaseModel):
    def __init__(self):
        super().__init__("class_units")

class Attendance(BaseModel):
    def __init__(self):
        super().__init__("attendance")

class Admin(BaseModel):
    def __init__(self):
        super().__init__("admins")
