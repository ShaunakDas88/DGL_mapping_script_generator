from EdgeDistributionUtility import EdgeDistributionUtility

class MapperGenerator():
	mapper_file = None
	vertexlabel_map = None
	edgelabel_map = None
	
	@classmethod
	def __init__(cls, mapper_file, vertexlabel_map, edgelabel_map):
		cls.mapper_file = open(mapper_file, "w")
		cls.vertexlabel_map = vertexlabel_map
		cls.edgelabel_map = edgelabel_map

	def create_count_variables(self):
		self.mapper_file.write("// Define vertex count variables\n")
		# first handle numbers for vertices
		for vertexlabel in self.vertexlabel_map:
			self.mapper_file.write("num_{u}_vertices = Integer.valueOf(num_{l}_vertices)\n".format(u=vertexlabel, l=vertexlabel.lower()))
		# now handle number of edges
#		for edgelabel in self.edgelabel_map:
#			self.mapper_file.write("num_{u}_edges = Integer.valueOf(num_{l}_edges)\n".format(u=edgelabel, l=edgelabel.lower())
		self.mapper_file.write("\n")

	def create_vertex_data_generators(self):
		self.mapper_file.write("// Data generation for different vertices\n")
		for vertexlabel in self.vertexlabel_map:
			# start the string for data generation
			string = vertexlabel + "_v = Generator.of{"
			string += "\n\t[identifier: it]}.count(num_" + vertexlabel + "_vertices)"
			# write to file
			self.mapper_file.write(string + "\n\n")

	def create_vertex_loaders(self):
		self.mapper_file.write("// Loading of vertex data\n")
		for vertexlabel in self.vertexlabel_map:
			string = "load(" + vertexlabel + "_v).asVertices {"
			string += '\n\tlabel "' + vertexlabel + '"'
			string += '\n\tkey "identifier"'
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
		self.create_edge_data_generators()
		self.create_edge_loaders()
		self.mapper_file.close()
