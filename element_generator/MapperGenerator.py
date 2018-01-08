from VertexGenerator import VertexGenerator
from EdgeGenerator import EdgeGenerator
from EdgeDistributionUtility import EdgeDistributionUtility

class MapperGenerator():
	mapper_file = None
	variables_file = None
	vertexlabel_map = None
	vertex_generator = None
	edge_distribution = None
	edge_generator = None
	groovy_variables = None
	
	@classmethod
	def __init__(cls, mapper_file, vertexlabel_map, edgelabel_map, propertykey_map, edge_distribution):
		cls.mapper_file = open(mapper_file + ".groovy", "w")
		cls.variables_file = open(mapper_file + "_variables", "w")
		cls.vertex_generator = VertexGenerator(vertexlabel_map, propertykey_map)
		cls.edge_distribution = edge_distribution
		cls.edge_generator = EdgeGenerator(edgelabel_map, vertexlabel_map, propertykey_map)
		cls.vertex_count_variables = {}
		cls.groovy_variables = []

	def generate_mapping_script(self):
		# creating variables for vertex counts
		groovy, groovy_variables = self.vertex_generator.create_vertex_count_variables()
		self.mapper_file.write(groovy)
		self.groovy_variables += groovy_variables
		# creating vertex generators
		self.mapper_file.write(self.vertex_generator.create_vertex_data_generators())
		# creating vertex loader
		self.mapper_file.write(self.vertex_generator.create_vertex_loaders())
		# creating edge data generators
		groovy, groovy_variables = self.edge_generator.create_edge_data_generators(self.edge_distribution)
		self.mapper_file.write(groovy)
		self.groovy_variables += groovy_variables
		# creating edge loaders
		self.mapper_file.write(self.edge_generator.create_edge_loaders())
		self.mapper_file.close()
		# write the variables for our mapping script to their own file
		for variable in self.groovy_variables:
			self.variables_file.write(variable + "\n")
		self.variables_file.close()
