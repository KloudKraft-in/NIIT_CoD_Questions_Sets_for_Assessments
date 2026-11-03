import sys
import json

def serializable(fields: list):
    def class_decorator(cls):
        # Implementation here: add to_dict(self) method to cls
        pass
        return cls
    return class_decorator

if __name__ == "__main__":
    # Command processor for standardized evaluation
    input_data = sys.stdin.read().splitlines()
    for line in input_data:
        parts = line.strip().split(maxsplit=2)
        if not parts: continue
        cmd = parts[0]
        if cmd == "SERIALIZE":
            cls_name, fields = parts[1], json.loads(parts[2])
            if cls_name == "User":
                @serializable(fields=fields)
                class User:
                    def __init__(self, **kwargs):
                        for k, v in kwargs.items(): setattr(self, k, v)
                @serializable(fields=["id", "users"])
                class Group:
                    def __init__(self, id, users): self.id = id; self.users = users
                u1 = User(id=1, name="Alice", email="a@b.com")
                u2 = User(id=2, name="Bob", email="b@b.com")
                g = Group(101, [u1, u2])
                if "users" in fields: print(json.dumps(g.to_dict(), sort_keys=True))
                else: print(json.dumps(u1.to_dict(), sort_keys=True))
