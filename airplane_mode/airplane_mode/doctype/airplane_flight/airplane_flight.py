# Copyright (c) 2026, jymnastiar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class AirplaneFlight(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		airplane_flight: DF.Link
		amended_from: DF.Link | None
		date_of_departure: DF.Date
		destination_airport: DF.Link
		destination_airport_code: DF.Data | None
		duration: DF.Duration
		source_airport: DF.Link
		source_airport_code: DF.Data | None
		status: DF.Literal["Scheduled", "Completed", "Cancelled"]
		time_of_departure: DF.Time
	# end: auto-generated types

	def validate(self):
		if self.source_airport == self.destination_airport:
			frappe.throw(_("Source and Destination Airport cannot be the same"), title=_("Invalid Airports"))

	def on_submit(self):
		self.db_set("status", "Completed")
