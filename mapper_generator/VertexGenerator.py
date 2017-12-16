from PropertyKeyGenerator import PropertyKeyGenerator

class VertexGenerator():
	vertexlabel_map = None
	propertykey_generator = None
	vertex_count_variable_map = None
	
	@classmethod
	def __init__(cls, vertexlabel_map, propertykey_map):
		cls.vertexlabel_map = vertexlabel_map
		cls.propertykey_generator = PropertyKeyGenerator(propertykey_map)
		cls.vertex_count_variable_map = {}

	def create_vertex_count_variables(self):
		groovy = "// Define vertex count variables\n"
		for vertexlabel in self.vertexlabel_map:
			curr_variable = "num_{l}_vertices".format(l=vertexlabel)
			self.vertex_count_variable_map[vertexlabel] = curr_variable
			groovy += "{x} = Integer.valueOf({y})\n".format(x=curr_variable, y=curr_variable.lower())
		# write count variables to mapping script
		groovy += "\n"
		return groovy

	def create_vertex_data_generators(self):
		groovy = "// Data generation for different vertices\n"
		for vertexlabel in self.vertexlabel_map:
			custom_id = False
			n = "num_" + vertexlabel + "_vertices"
			# start the string for data generation
			groovy += vertexlabel + "_v = Generator.of {"
			# generate custom ids and propertykeys
			groovy += self.propertykey_generator.form_propertykey_groovy_map(vertexlabel, self.vertexlabel_map)
			# close out the data generator
			groovy += "\n}.count(" + n + ")\n\n"
		return groovy

	def create_vertex_loaders(self):
		groovy = "// Loading of vertex data\n"
		for vertexlabel in self.vertexlabel_map:
			groovy += "load(" + vertexlabel + "_v).asVertices {"
			groovy += '\n\tlabel "' + vertexlabel + '"'
			groovy += '\n\tkey "id"'
			groovy += "\n}\n\n"
		return groovy
