from PropertyKeyGenerator import PropertyKeyGenerator

class EdgeDistributionUtility():
	propertykeys_generator = None
	vertexlabel_map = None

	@classmethod
	def __init__(cls, propertykey_map, vertexlabel_map):
		cls.propertykey_generator = PropertyKeyGenerator(propertykey_map)
		cls.vertexlabel_map = vertexlabel_map

	def create_point_mass_distribution(self, edgelabel, edgelabel_map):
		"""
		This method is for making sure that each vertex has exactly num_edges edges, for
		each relevant edgeLabel, i.e.

			Prob(any given vertex has num_edges of a given relevant label) = 1

		@param edgelabel:	which edgelabel we are currently dealing with
		@type edgelabel:	str
		@param edgelabel_map:	
		@type edgelabel_map:	dict	
		"""
		num_v = "num_" + edgelabel_map[edgelabel]["to"] + "_vertices"
		num_e = "num_{l}_edges".format(l=edgelabel.lower())
		groovy = "num_{e}_edges = Integer.valueOf({v})".format(e=edgelabel, v=num_e)
		groovy += "\n\n" + edgelabel + "_e = Generator.of {"
		groovy += "\n\tdef neighbours_numeric = []"
		# want to handle variable names
		groovy += "\n\tfor (int i = 1; i <= " + "num_{e}_edges".format(e=edgelabel) + "; i++) {"
		groovy += "\n\t\tneighbours_numeric << ((it+i)%{l})".format(l=num_v)
		groovy += "\n\t}"
		# need to determine the type of the custom id key for the outgoing vertex
		from_label = edgelabel_map[edgelabel]["from"]
		from_label_id_key = self.vertexlabel_map[from_label]["custom_id_key"]
		from_label_id_type = self.propertykey_generator.propertykey_map[from_label_id_key]["type"]
		from_v_groovy = "it." + self.propertykey_generator.propertykey_type_map[from_label_id_type]
		# need to determine types of the custom id key for the incoming vertices
		to_label = edgelabel_map[edgelabel]["to"]
		to_label_id_key = self.vertexlabel_map[to_label]["custom_id_key"]
                to_label_id_type = self.propertykey_generator.propertykey_map[to_label_id_key]["type"]
		groovy += "\n\tdef neighbours = []"
		groovy += "\n\tfor (int i : neighbours_numeric) {"
		groovy += "\n\t\tneighbours << i.{c}".format(c=self.propertykey_generator.propertykey_type_map[to_label_id_type])
		groovy += "\n\t}"
		groovy += "\n\t[\"out\": {o}, \"neighbours\": neighbours]".format(o=from_v_groovy)
		groovy += "\n}"
		groovy += "\n.count(" + num_v + ").flatMap {"
		groovy += "\n\toutVertex = it[\"out\"]"
		groovy += "\n\tit[\"neighbours\"].collect {"
		groovy += "\n\t\tinVertex=it"
		groovy += "\n\t\tit = [\"out\": outVertex, \"in\": inVertex]"
		groovy += "\n\t}"
		groovy += "\n}"
		return groovy

	def create_uniform_distribution(vertexlabel_map, edgelabel_map, lower, upper):
		"""
		This method is for making sure that each edgeLabel has a distribution that follows
		the uniform distribution, i.e. 

			Prob(any given vertex has N edges of a given relevant label) = 1/(upper - lower)

		for all x in the range [lower, upper] and 0 otherwise, where:
			- upper = the largest number of edges of a given (relevant) label a vertex can have
			- lower	= the smallest number of edges of a given (relevant) label a vertex can have	
		"""
		
	
	def create_Gaussian_distribution(vertexlabel_map, edgelabel_map, mean, variance):
		"""
		This method is for making sure that each edgeLabel has a distribution that follows a Gaussian/normal
		distribution, i.e.
			
			Prob(any given vertex has N edges of a given relevant label) = [1/(2*pi*variance)]*exp[-(N-mean)^2/(2*variance)]
		"""
		return

	def create_power_law_distribution():
		"""
		This method 

		groovy_string

		return groovy_string
		"""
		return
