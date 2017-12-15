from EdgeDistributionUtility import EdgeDistributionUtility

class MapperGenerator():
	mapper_file = None
	vertexlabel_map = None
	edgelabel_map = None
	propertykey_map = None
	
	@classmethod
	def __init__(cls, mapper_file, vertexlabel_map, edgelabel_map, propertykey_map):
		cls.mapper_file = open(mapper_file, "w")
		cls.vertexlabel_map = vertexlabel_map
		cls.edgelabel_map = edgelabel_map
		cls.propertykey_map = propertykey_map

	def create_count_variables(self):
		self.mapper_file.write("// Define vertex count variables\n")
		for vertexlabel in self.vertexlabel_map:
			self.mapper_file.write("num_{u}_vertices = Integer.valueOf(num_{l}_vertices)\n".format(u=vertexlabel, l=vertexlabel.lower()))
		# write count variables to mapping script
		self.mapper_file.write("\n")

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

	def create_vertex_data_generators(self):
		self.mapper_file.write("// Data generation for different vertices\n")
		for vertexlabel in self.vertexlabel_map:
			custom_id = False
			n = "num_" + vertexlabel + "_vertices"
			# start the string for data generation
			string = vertexlabel + "_v = Generator.of {"
			# check if we are dealing with custom ids
			if self.vertexlabel_map[vertexlabel]["custom_id_key"]:
				custom_id = True
				propertykey= self.vertexlabel_map[vertexlabel]["custom_id_key"]
				string += "\n\t["
				string += "\n\t\t{k}:{v},".format(k=propertykey, v=self.generate_propertykeys(propertykey))
			# check if we are dealing with any propertyKeys
			if self.vertexlabel_map[vertexlabel]["propertykeys"]:
				# start propertyKey map if we do not have custom id
				if not custom_id:
					string += "\n\t["
				for propertykey in self.vertexlabel_map[vertexlabel]["propertykeys"]:
					# generate propertyKeys for the given vertex we are dealing with
					string += "\n\t\t{k}:{v},".format(k=propertykey, v=self.generate_propertykeys(propertykey))
			# remove lagging comma, close out propertyKey map in these two cases
			if custom_id or self.vertexlabel_map[vertexlabel]["propertykeys"]:
				string = string[:-1]+"\n\t]"
			# close out the data generator
			string += "\n}.count(" + n + ")"
			# write the data generator to our mapping script
			self.mapper_file.write(string + "\n\n")

	def create_vertex_loaders(self):
		self.mapper_file.write("// Loading of vertex data\n")
		for vertexlabel in self.vertexlabel_map:
			string = "load(" + vertexlabel + "_v).asVertices {"
			string += '\n\tlabel "' + vertexlabel + '"'
			string += '\n\tkey "id"'
			# want to ignore propertyKey that corresponds to a custom id key
			if self.vertexlabel_map[vertexlabel]["custom_id_key"]:
				string += '\n\tignore "{k}"'.format(k=self.vertexlabel_map[vertexlabel]["custom_id_key"])
			string += "\n}"
			self.mapper_file.write(string + "\n\n")

	def create_edge_data_generators(self):
		self.mapper_file.write("// Data generation for different edges\n")
		for edgelabel in self.edgelabel_map:
			mapper_string = EdgeDistributionUtility().create_point_mass_distribution(edgelabel, self.edgelabel_map)
			self.mapper_file.write(mapper_string + "\n\n")
	
	def create_edge_loaders(self):
		self.mapper_file.write("// Loading of edge data\n")
		for edgelabel in self.edgelabel_map:
			string = 'load(' + edgelabel + '_e).asEdges {'
			string += '\n\tlabel "' + edgelabel + '"'
			string += '\n\toutV "out", {'
			string += '\n\t\tlabel "{l}"'.format(l=self.edgelabel_map[edgelabel]["from"])
			string += '\n\t\tkey "{i}"'.format(i="identifier")
			string += '\n\t}'
			string += '\n\tinV "in", {'
			string += '\n\t\tlabel "{l}"'.format(l=self.edgelabel_map[edgelabel]["to"])
			string += '\n\t\tkey "{i}"'.format(i="identifier")
			string += "\n\t}"
			string += "\n}"
			self.mapper_file.write(string + "\n\n")

	def generate_mapping_script(self):
		self.create_count_variables()
		self.create_vertex_data_generators()
		self.create_vertex_loaders()
		#self.create_edge_data_generators()
		#self.create_edge_loaders()
		self.mapper_file.close()
