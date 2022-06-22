import requests
import json

ROLES = {
	"Admin" : ["total_access"],
	"HelpDesk" : [
		"incidents_create", 
		"incidents_update"
	],
	"ProblemsManager" : [
		"problems_create",
		"problems_update", 
		"changes_create"
	],
	"ChangesManager" : [
		"changes_create",
		"changes_edit"
	]
}


def make_request(data, url):
	headers = {
 		'Content-Type': 'application/json'
	}
	payload = json.dumps(data)
	return requests.request("POST", url, headers=headers, data=payload)

def create_roles():
	roles_ids = {}
	for role in ROLES.keys():
		permissions = ROLES[role]
		data = {
			"name": role,
			"permissions": permissions
		}
		response = make_request(data, "http://127.0.0.1:5000/roles")
		response = json.loads(response.text)
		roles_ids[role] = response["id"]
		print(f"Role: {role} created")
	return roles_ids

def create_users(roles_ids):
	for role in ROLES.keys():
		email = f"{role}@gmail.com"
		password = "1234"
		data = {
			"email": email,
			"password": password,
			"username": role,
			"name": role,
			"lastname": "Fernández",
			"role_id": roles_ids[role]
		}
		make_request(data, "http://127.0.0.1:5000/users")
		print(f"User with email: {email} and password {password} created")

def main():
	print("Role creation starting")
	roles_ids = create_roles()
	print("Role creation finished")
	print("User creation starting")
	create_users(roles_ids)
	print("User creation finished")

main()