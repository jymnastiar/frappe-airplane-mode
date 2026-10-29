import frappe


@frappe.whitelist()
def get_plane_ticket():
	return frappe.get_all(
		"Airplane Ticket",
		fields=[
			"name",
			"passenger",
			"source_airport",
			"destination_airport",
			"source_airport_code",
			"flight",
			"departure_date",
			"departure_time",
			"duration_of_flight",
			"destination_airport_code",
			"status",
		],
		group_by="",
		# filters={"status": "Booked"},
	)
