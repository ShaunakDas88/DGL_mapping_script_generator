class PropertyKeyGenerator():
	propertykey_map = None
	propertykey_type_map = None

	@classmethod
	def __init__(cls, propertykey_map):
		cls.propertykey_map = propertykey_map
		cls.propertykey_type_map = {	"Text" : "toString()", 
						"Int" : "toInteger()", 
						"Double" : "toDouble()", 
						"Float" : "toFloat()",
						"Timestamp" : "toInteger()"}	# need to figure something out for this

	def generate_propertykey(self, propertykey, prefix="it"):
		groovy = None
		prop_type = self.propertykey_map[propertykey]["type"]
		groovy = "{p}.{c}".format(p=prefix, c=self.propertykey_type_map[prop_type])
		# TO DO: handle more exotic types (e.g. Date)
		# handle multiple cardinality
		if self.propertykey_map[propertykey]["cardinality"] == "multiple":
			groovy += ".toArray()"
		#  TO DO: need to handle metaproperties
		return groovy

	def form_propertykey_groovy_map(self, label, edge_or_vertexlabel_map):
		# handle custom id first (if used)
		if edge_or_vertexlabel_map[label]["custom_id_key"]:
			custom_id = True
			# start the propertyKey map 
			groovy = "\n\t["
			propertykey = edge_or_vertexlabel_map[label]["custom_id_key"]
			groovy += "\n\t\t{k} : {v},".format(k=propertykey, v=self.generate_propertykey(propertykey))
		# handle remaining propertyKeys
		if edge_or_vertexlabel_map[label]["propertykeys"]:
			# if no custom ids, need to start propertyKey map 
			if not custom_id:
				groovy = "\n\t["
			for propertykey in edge_or_vertexlabel_map[label]["propertykeys"]:
				# generate propertyKeys for the given edge/vertex we are dealing with
				groovy += "\n\t\t{k} : {v},".format(k=propertykey, v=self.generate_propertykey(propertykey))
		# remove lagging comma, close out propertyKey map in these two cases
		if custom_id or self.vertexlabel_map[vertexlabel]["propertykeys"]:
			groovy = groovy[:-1]+"\n\t]"
		return groovy
