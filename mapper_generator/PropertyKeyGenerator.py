class PropertyKeyGenerator():
	propertykeys_map = None

	@classmethod
	def __init__(cls, propertykeys_map):
		cls.propertykeys_map = propertykeys_map

	def generate_propertykeys(self, propertykey):
		string = None
		prop_type = self.propertykey_map[propertykey]["type"]
		if prop_type in ["String", "Text"]:
			string = "'{p}_'+it.toString()".format(p=propertykey)
		elif prop_type == "Double":
			string = "it.toDouble()"
		elif prop_type == "Float":
			string = "it.toFloat()"
		# TO DO: handle more exotic types (e.g. Date)
		# default type will be Integer
		else:
			string = "it"
		# handle multiple cardinality
		if self.propertykey_map[propertykey]["cardinality"] == "multiple":
			string = "[" + string + "]"
		# TO DO: need to handle metaproperties
		return string
