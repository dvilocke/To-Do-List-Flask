from flask_login import UserMixin


class User(UserMixin):
    def __init__(self,name, email, password, id = None) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.password = password


    def check_password(self, password):
        return password == self.password

    def save(self, con):
        cur = con.connection.cursor()
        cur.execute(f'INSERT INTO users (name, email, password) VALUES (%s,%s,%s)',(self.name, self.email, self.password))
        con.connection.commit()

    def __str__(self) -> str:
        return f'id:{self.id},name:{self.name},email:{self.email},password:{self.password}'

    @staticmethod
    def get_email(user_email, con= None):
        cur = con.connection.cursor()
        cur.execute('SELECT * FROM users WHERE email = (%s)',(user_email,))
        try: 
            data = cur.fetchall()[0]
        except:
            data = None
        if data:
            return User(data[1], data[2], data[3], id=data[0])
        return None

    @staticmethod
    def get(user_id, con=None):
        cur = con.connection.cursor()
        cur.execute(f'SELECT * FROM users WHERE id = {user_id}')
        try:
            data = cur.fetchall()[0]
        except:
            data = None
        if data:
            return User(data[1], data[2], data[3], id=data[0])
        return None

class Task:
    def __init__(self,id_user, name, description, state , id = None) -> None:
        self.id_user = id_user
        self.name = name
        self.description = description
        self.state = state
        self.id = id

    @staticmethod
    def update_task(name, description, state, new_name, new_description, new_state, con):
        cur = con.connection.cursor()
        cur.execute('UPDATE task SET name = %s, description = %s, state = %s WHERE name = %s and description = %s and state = %s', 
        (new_name, new_description, new_state, name, description, state))
        con.connection.commit()

    @staticmethod
    def update_state(name, description, old_state, new_state, con):
        cur = con.connection.cursor()
        cur.execute('UPDATE task SET state = %s WHERE name = %s and description = %s and state = %s', (new_state,name, description, old_state))
        con.connection.commit()

    @staticmethod
    def get_task(id_user, name, description, state, con):
        cur = con.connection.cursor()
        cur.execute('SELECT id_user, name, description, state FROM task WHERE id_user = %s and name = %s and description= %s and state= %s', (id_user, name, description, state))
        data = cur.fetchall()
        return data

    @staticmethod
    def delete_task(id_user, name, description, state , con):
        cur = con.connection.cursor()
        cur.execute('DELETE FROM task WHERE id_user = %s and name = %s and description = %s and state = %s', (id_user, name, description, int(state)))
        con.connection.commit()

    @staticmethod
    def bring_user_tasks(id_user, con):
        cur = con.connection.cursor()
        cur.execute(f'SELECT id_user, name, description, state FROM task WHERE id_user ={id_user}')
        data = cur.fetchall()
        return data


    def save_task(self, con):
        cur = con.connection.cursor()
        cur.execute('INSERT INTO task (id_user, name, description, state) VALUES (%s, %s, %s, %s)',(self.id_user, self.name, self.description, self.state))
        con.connection.commit()
            
    