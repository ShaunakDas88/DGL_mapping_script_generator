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
		num_v = "num_" + edgelabel_map[edgelabel]["to"].lower() + "_vertices"
		num_e = "num_{l}_edges".format(l=edgelabel.lower())
		# these are variables in the groovy script that the user will need to specify on the command line
		groovy_variables = [num_e]
		groovy = "{e} = Integer.valueOf({e})".format(e=num_e)
		groovy += "\n\n" + edgelabel.lower() + "_e = Generator.of {"
		groovy += "\n\tdef neighbours_numeric = []"
		# want to handle variable names
		groovy += "\n\tfor (int i = 1; i <= " + "{e}".format(e=num_e) + "; i++) {"
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
		groovy += "\n\t["
		groovy += "\n\t\t\"out\" : {o}, ".format(o=from_v_groovy)
		groovy += "\n\t\t\"neighbours\" : neighbours,"
		# need this 'index' field for generating propertyKeys for the edge
		groovy += "\n\t\t\"index\" : it"
		groovy += "\n\t]"
		groovy += "\n}"
		groovy += "\n.count(" + num_v + ")"
		return groovy, groovy_variables

	def create_uniform_distribution(self, edgelabel, edgelabel_map):
		"""
		This method is for making sure that each edgeLabel has a distribution that follows
		the uniform distribution, i.e. 

			Prob(any given vertex has N edges of a given relevant label) = 1/(upper - lower)

		for all N in the range [lower, upper] and 0 otherwise, where:
			- upper = the largest number of edges of a given (relevant) label a vertex can have
			- lower	= the smallest number of edges of a given (relevant) label a vertex can have	
		"""
		return

	def create_Gaussian_distribution(self, edgelabel, edgelabel_map):
		"""
		This method is for making sure that each edgeLabel has a distribution that follows a Gaussian/normal
		distribution, i.e.
			
			Prob(any given vertex has N edges of a given relevant label) = [1/(2*pi*variance)]*exp[-(N-mean)^2/(2*variance)]
		"""
		num_v = "num_" + edgelabel_map[edgelabel]["to"] + "_vertices"
		#edge_degree_mean = 
		#edge_degree_variance = 
		return

	def create_power_law_distribution(self, edgelabel, edgelabel_map):
		"""
		This method is for making sure that each edgeLabel has a distributrion that follows a power law, i.e.
	
			Prob(any vertex has N edges of a given relevant label) = CN^{-k}

		return groovy_string
		"""
		num_v = "num_" + edgelabel_map[edgelabel]["to"].lower() + "_vertices"
		edge_degree_coefficient = "{e}_coefficient".format(e=edgelabel.lower())
		edge_degree_decay_constant = "{e}_decay_constant".format(e=edgelabel.lower())
		# these are variables in the groovy script that the user will need to specify on the command line 
		groovy_variables = [edge_degree_coefficient, edge_degree_decay_constant]
		groovy = "{e} = Integer.valueOf({e})".format(e=edge_degree_coefficient)
		groovy += "\n{e} = Integer.valueOf({e})".format(e=edge_degree_decay_constant)
		groovy += "\n\n" + edgelabel.lower() + "_e = Generator.of {"
		groovy += "\n\tdef neighbours_numeric = []"
		groovy += "\n\tdef num_{e}_edges = ({e}_coefficient/(it+1).power({e}_decay_constant)).intValue()".format(e=edgelabel.lower())
		# want to handle variable names
		groovy += "\n\tfor (int i = 1; i <= " + "num_{e}_edges".format(e=edgelabel.lower()) + "; i++) {"
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
		groovy += "\n\t["
		groovy += "\n\t\t\"out\" : {o}, ".format(o=from_v_groovy)
		groovy += "\n\t\t\"neighbours\" : neighbours,"
		# need this 'index' field for generating propertyKeys for the edge
		groovy += "\n\t\t\"index\" : it"
		groovy += "\n\t]"
		groovy += "\n}"
		groovy += "\n.count(" + num_v + ")"
		return groovy, groovy_variables
