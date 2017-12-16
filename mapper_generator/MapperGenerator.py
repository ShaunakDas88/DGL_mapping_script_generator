from VertexGenerator import VertexGenerator
from EdgeGenerator import EdgeGenerator
from EdgeDistributionUtility import EdgeDistributionUtility

class MapperGenerator():
	mapper_file = None
	vertexlabel_map = None
	vertex_generator = None
	edge_generator = None
	
	@classmethod
	def __init__(cls, mapper_file, vertexlabel_map, edgelabel_map, propertykey_map):
		cls.mapper_file = open(mapper_file, "w")
		cls.vertex_generator = VertexGenerator(vertexlabel_map, propertykey_map)
		cls.edge_generator = EdgeGenerator(edgelabel_map, vertexlabel_map, propertykey_map)
		cls.vertex_count_variables = {}

	def generate_mapping_script(self):
		self.mapper_file.write(self.vertex_generator.create_vertex_count_variables())
		self.mapper_file.write(self.vertex_generator.create_vertex_data_generators())
		self.mapper_file.write(self.vertex_generator.create_vertex_loaders())
		self.mapper_file.write(self.edge_generator.create_edge_data_generators())
		self.mapper_file.write(self.edge_generator.create_edge_loaders())
		self.mapper_file.close()
