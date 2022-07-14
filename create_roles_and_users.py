from pprint import pp
import requests
import json
import random

NAMES = ["Andrés", "Manuel", "Carlos", "Juan", "Lucía", "Facundo", "Valentín"]
SURNAMES = ["González", "López", "García", "Martínez", "Pérez", "Sánchez", "Rodríguez"]
URL = "http://127.0.0.1:5000"
ROLES = {
	"Admin" : ["total_access"],
	"HelpDesk" : [
		"incidents_create", 
		"incidents_update",
		"errors_create",
		"errors_update"
	],
	"ProblemsManager" : [
		"problems_create",
		"problems_update", 
		"changes_create",
		"errors_create",
		"errors_update"
	],
	"ChangesManager" : [
		"changes_create",
		"changes_update",
		"items_update",
		"items_create",
		"errors_create",
		"errors_update"
	],
	"ErrorsManager": [
		"errors_create",
		"errors_update"
	]
}


def make_request(data, url):
	headers = {
 		'Content-Type': 'application/json'
	}
	payload = json.dumps(data)
	return requests.request("POST", url, headers=headers, data=payload)

def create_roles(roles_ids):
	for role in ROLES.keys():
		if role in roles_ids: continue

		permissions = ROLES[role]
		data = {
			"name": role,
			"permissions": permissions
		}
		response = make_request(data, URL + "/roles")
		response = json.loads(response.text)
		print(response)
		roles_ids[role] = response["id"]
		print(f"Role: {role} created")
	return roles_ids

def get_roles():
	roles_ids = {}
	response = requests.request("GET", URL+ "/roles")
	for role in json.loads(response.text):
		roles_ids[role["name"]] = role["id"]
	return roles_ids

def create_users(roles_ids, current_users):
	for role in ROLES.keys():
		email = f"{role}@gmail.com"
		if email in current_users: continue
		password = "1234"
		data = {
			"email": email,
			"password": password,
			"username": role,
			"name": role,
			"lastname": "Fernández",
			"role_id": roles_ids[role]
		}
		make_request(data, URL+ "/users")
		current_users.add(email)
		print(f"User with email: {email} and password {password} created")
	return current_users


def create_demo_users(roles_ids, current_users):
	for i in range(5):
		role_id = roles_ids["Admin"]
		name = random.choice(NAMES)
		surname = random.choice(SURNAMES)
		username = f"{name}_{surname}"
		email = f"{username}@gmail.com"
		if email in current_users: continue
		password = "1234"
		data = {
				"email": email,
				"password": password,
				"username": username,
				"name": name,
				"lastname": surname,
				"role_id": role_id
			}
		make_request(data, URL+ "/users")
		current_users.add(email)
		print(f"User with email: {email} and password {password} created")
	return current_users

def get_users():
	response = requests.request("GET", URL + "/users")
	users = json.loads(response.text)
	return set([user["email"] for user in users])

def main():
	print("Role creation starting")
	roles_ids = get_roles()
	roles_ids = create_roles(roles_ids)
	current_users = get_users()
	print("Role creation finished")
	print("User creation starting")
	current_users = create_users(roles_ids, current_users)
	create_demo_users(roles_ids, current_users)
	print("User creation finished")

main()