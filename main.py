from integration.api_gateway import ApiGateway

gateway = ApiGateway()
gateway.setup()

# one normal user and one user from the city
gateway.register("anna", "anna123", "citizen", "Dortmund")
gateway.register("city", "city123", "municipality", "Dortmund")

token = gateway.login("anna", "anna123")

photos = ["plastic_bottle.jpg", "metal_can.png", "biological_peel.jpg", "blurry_photo.jpg", "notes.txt"]
for photo in photos:
    print("Scanning", photo)
    recommendation = gateway.scan(token, photo, 2)
    if recommendation is not None:
        recommendation.show()
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
print("Dashboard for anna:", gateway.dashboard(token))

gateway.logout(token)
