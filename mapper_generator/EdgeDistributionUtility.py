from PropertyKeysGenerator import PropertyKeysGenerator

class EdgeDistributionUtility():
	propertykeys_generator = None

	@classmethod
	def __init__(cls, propertykeys_map):
		cls.propertykeys_generator = PropertyKeysGenerator(propertykeys_map)

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
		num_v = "num_"+edgelabel_map[edgelabel]["to"]+"_vertices"
		num_e = "num_{l}_edges".format(l=edgelabel.lower())
		string = "num_{e}_edges = Integer.valueOf({v})".format(e=edgelabel, v=num_e)
		string += "\n\n" + edgelabel + "_e = Generator.of {"
		string += "\n\tdef neighbours = []"
		string += "\n\tfor (int i = 1; i <= " + "num_{e}_edges".format(e=edgelabel) + "; i++) {"
		string += "\n\t\tneighbours << ((it+i)%{l})".format(l=num_v)
		string += "\n\t}"
		string += "\n\t[\"out\": it, \"neighbours\": neighbours]"
		string += "}.count(" + num_v + ").flatMap {"
		string += "\n\toutVertex = it[\"out\"]"
		string += "\n\tit[\"neighbours\"].collect {"
		string += "\n\t\tinVertex=it"
		string += "\n\t\tit = [\"out\": outVertex, \"in\": inVertex]"
		string += "\n\t}"
		string += "\n}"
		return string

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
