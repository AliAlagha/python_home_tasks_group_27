from integration.api_gateway import ApiGateway
from integration.errors import IntegrationError

gateway = ApiGateway()
gateway.setup()

# one normal user and one user from the city
gateway.register("anna", "anna123", "citizen", "Dortmund")
gateway.register("city", "city123", "municipality", "Dortmund")

token = gateway.login("anna", "anna123")

photos = ["plastic_bottle.jpg", "metal_can.png", "biological_peel.jpg", "blurry_photo.jpg", "notes.txt"]
for photo in photos:
    print("Scanning", photo)
    try:
        gateway.scan(token, photo, 2).show()
    except IntegrationError as error:
        print("Error", error.status_code, ":", error)
    print()

print("Scan history:")
gateway.get_statistics().show_history()
gateway.get_accounts()["anna"].show()
print("Recyclable items in the rules:", len(gateway.get_recommendations().find_rules_by_category("Recyclable")))
print(gateway.get_classification())
gateway.get_recommendations().get_schedule().show()
print()

city_token = gateway.login("city", "city123")
print("Dashboard:", gateway.dashboard(city_token))

# citizens are not allowed to see the dashboard
try:
    gateway.dashboard(token)
except IntegrationError as error:
    print("Error", error.status_code, ":", error)

gateway.logout(token)
