# Copyright (c) 2026, jymnastiar and contributors
# For license information, please see license.txt

import frappe
import random
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, cint
from frappe.model.naming import make_autoname
from frappe.utils.telemetry.pulse.app_heartbeat_event import capture_app_heartbeat


class AirplaneTicket(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from airplane_mode.airplane_mode.doctype.airplane_ticket_add_on_item.airplane_ticket_add_on_item import (
			AirplaneTicketAddonItem,
		)
		from frappe.types import DF

		add_ons: DF.Table[AirplaneTicketAddonItem]
		amended_from: DF.Link | None
		departure_date: DF.Date
		departure_time: DF.Time
		destination_airport_code: DF.Data
		duration_of_flight: DF.Duration
		flight: DF.Link
		flight_price: DF.Currency
		passenger: DF.Link
		seat: DF.Data | None
		source_airport_code: DF.Data
		status: DF.Literal["Booked", "Checked-In", "Boarded"]
		total_amount: DF.Currency
	# end: auto-generated types

	def autoname(self):
		self.name = make_autoname(
			f"{self.flight}-{self.source_airport_code}-to-{self.destination_airport_code}-.###"
		)

	def remove_dup_add_on(self):
		dupp_item = set()
		unique_item = []
		for row in self.add_ons:
			if row.item not in dupp_item:
				dupp_item.add(row.item)
				unique_item.append(row)
		self.set("add_ons", unique_item)

	def before_insert(self):
		airplanes = frappe.db.get_value("Airplane Flight", self.flight, "airplane_flight")

		capacity = 100
		if airplanes:
			capacity = cint(frappe.db.get_value("Airplane", airplanes, "capacity")) or 100

		random_num = random.randint(0, int(capacity))
		random_string = "ABCDE"
		self.seat = f"{random_num}{random.choice(random_string)}"

	def before_validate(self):
		self.remove_dup_add_on()
		self.total_amount = flt(self.flight_price) + sum(flt(row.amount) for row in self.add_ons)

	def before_submit(self):
		if self.status != "Boarded":
			frappe.throw("Ticket can be submitted in boarded status")
