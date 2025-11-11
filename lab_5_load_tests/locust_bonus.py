import random
from locust import HttpUser, task, between

class TodoUser(HttpUser):
    # Simulate a wait time between 1 and 2.5 seconds after each task
    wait_time = between(1, 2.5)
    
    # Lista az ezen felhasználó által létrehozott feladatok ID-jainak tárolására
    created_task_ids = []
    
    def on_start(self):
        """
        Ez a metódus minden virtuális felhasználó indításakor lefut.
        Inicializáljuk az általuk létrehozott feladatok listáját.
        """
        self.created_task_ids = []
        # Az alapértelmezett, fix ID-k, amiket szintén tesztelhetünk
        self.static_task_ids = [1, 2]


    @task(3)
    def get_all_todos(self):
        """
        Simulates a user fetching the list of all todos.
        """
        self.client.get("/todos", name="/todos (GET)")

    @task(2)
    def get_single_todo(self):
        """
        Simulates a user fetching a single todo item.
        It randomly picks from the static IDs or an ID this user has created.
        """
        # Egyesítjük a statikus és a dinamikusan létrehozott ID-kat
        available_ids = self.static_task_ids + self.created_task_ids
        if not available_ids:
            return # Ha valamiért üres a lista, nem csinálunk semmit

        todo_id = random.choice(available_ids)
        self.client.get(f"/todos/{todo_id}", name="/todos/{id} (GET)")

    @task(2) # Növeljük a súlyt, hogy legyen mit törölni/módosítani
    def create_todo(self):
        """
        Simulates a user creating a new todo item and saving its ID.
        """
        new_task_name = f"New task from user {random.randint(1, 1000)}"
        
        with self.client.post("/todos", json={"task": new_task_name}, name="/todos (POST)", catch_response=True) as response:
            if response.status_code == 201:
                # Sikeres létrehozás esetén elmentjük az új ID-t
                try:
                    response_json = response.json()
                    new_id = response_json.get("id")
                    if new_id:
                        self.created_task_ids.append(new_id)
                except Exception as e:
                    response.failure(f"Failed to parse JSON or get ID: {e}")
            else:
                response.failure(f"Failed to create task, status code: {response.status_code}")


    @task(1)
    def update_todo(self):
        """
        Simulates a user updating an existing todo item.
        It randomly picks from the static IDs or an ID this user has created.
        """
        available_ids = self.static_task_ids + self.created_task_ids
        if not available_ids:
            return

        todo_id_to_update = random.choice(available_ids)
        new_done_status = random.choice([True, False])
        
        self.client.put(
            f"/todos/{todo_id_to_update}",
            json={"done": new_done_status},
            name="/todos/{id} (PUT)"
        )

    @task(1)
    def delete_todo(self):
        """
        Simulates a user DELETING a todo item.
        It only deletes items that this specific user has created.
        """
        # Csak akkor próbálunk törölni, ha van mit
        if not self.created_task_ids:
            return # Nincs még létrehozott elem, kihagyjuk a törlést

        # Választunk egyet a listából
        todo_id_to_delete = random.choice(self.created_task_ids)
        
        with self.client.delete(f"/todos/{todo_id_to_delete}", name="/todos/{id} (DELETE)", catch_response=True) as response:
            if response.status_code == 204:
                # Sikeres törlés esetén eltávolítjuk a listából,
                # hogy ne próbáljuk újra törölni
                self.created_task_ids.remove(todo_id_to_delete)
            else:
                # Ha hiba történik (pl. 404), attól még eltávolítjuk, hogy ne próbálkozzunk vele újra
                if todo_id_to_delete in self.created_task_ids:
                    self.created_task_ids.remove(todo_id_to_delete)
                response.failure(f"Failed to delete task {todo_id_to_delete}, status: {response.status_code}")


    @task(1)
    def get_root(self):
        """
        Simulates a user hitting the welcome page.
        """
        self.client.get("/", name="/ (GET)")

