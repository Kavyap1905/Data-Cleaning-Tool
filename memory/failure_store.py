from phi.storage.local import LocalStorage
from phi.memory import Memory

storage = LocalStorage(path="memory/db")
memory = Memory(storage=storage)

def store_failure(issue, fix):
    memory.add({
        "issue": issue,
        "fix": fix
    })
