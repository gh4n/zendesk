import json

with open("data/users.json", 'r') as f:
    users = json.load(f)
with open("data/organizations.json", 'r') as f:
    orgs = json.load(f)
with open("data/tickets.json", 'r') as f:
    tickets = json.load(f)


if __name__ == "__main__":
    print(users)
    print(orgs)
    print(tickets)
    