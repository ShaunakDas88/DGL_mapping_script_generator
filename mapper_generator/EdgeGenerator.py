from EdgeDistributionUtility import EdgeDistributionUtility
from PropertyKeyGenerator import PropertyKeyGenerator

class EdgeGenerator():
	edge_distribution_utility = None
	propertykey_generator = None
	edgelabel_map = None
	vertexlabel_map = None

	@classmethod
	def __init__(cls, edgelabel_map, vertexlabel_map, propertykey_map):
		cls.edgelabel_map = edgelabel_map
		cls.vertexlabel_map = vertexlabel_map
		cls.edge_distribution_utility = EdgeDistributionUtility(propertykey_map, vertexlabel_map)
		cls.propertykey_generator = PropertyKeyGenerator(propertykey_map)

	def create_edge_data_generators(self):
		groovy = "// Data generation for different edges\n"
		for edgelabel in self.edgelabel_map:
			groovy += self.edge_distribution_utility.create_point_mass_distribution(edgelabel, self.edgelabel_map)
			# add in propertyKeys
			groovy += "\n.flatMap {"
			groovy += "\n\toutVertex = it[\"out\"]"
			groovy += "\n\tindex = it[\"index\"]"
			groovy += "\n\tit.remove(\"index\")"
			groovy += "\n\tit[\"neighbours\"].collect {"
			groovy += "\n\t\tinVertex=it"
			groovy += "\n\t\tit = "
			# need to handle in and out vertex information first
			groovy += "\n\t\t["
			groovy += "\n\t\t\t\"out\": outVertex,"
			groovy += "\n\t\t\t\"in\" : inVertex,"
			# add in propertyKeys
			if self.edgelabel_map[edgelabel]["propertykeys"]:
				for propertykey in self.edgelabel_map[edgelabel]["propertykeys"]:
					groovy += "\n\t\t\t\"{k}\" : {v},".format(k=propertykey, v=self.propertykey_generator.generate_propertykey(propertykey, "index"))
			# remove lagging comma, close up the map
			groovy = groovy[:-1] + "\n\t\t]"
			groovy += "\n\t}"
			groovy += "\n}\n\n"
		return groovy

	def create_edge_loaders(self):
		groovy = "// Loading of edge data\n"
		for edgelabel in self.edgelabel_map:
			from_label = self.edgelabel_map[edgelabel]["from"]
			to_label = self.edgelabel_map[edgelabel]["to"]
			from_label_id = self.vertexlabel_map[from_label]["custom_id_key"]
			to_label_id = self.vertexlabel_map[to_label]["custom_id_key"]
			groovy += 'load(' + edgelabel + '_e).asEdges {'
			groovy += '\n\tlabel "' + edgelabel + '"'
			groovy += '\n\toutV "out", {'
			groovy += '\n\t\tlabel "{l}"'.format(l=from_label)
			groovy += '\n\t\tkey "{i}"'.format(i=from_label_id)
			groovy += '\n\t}'
			groovy += '\n\tinV "in", {'
			groovy += '\n\t\tlabel "{l}"'.format(l=to_label)
			groovy += '\n\t\tkey "{i}"'.format(i=to_label_id)
			groovy += "\n\t}"
			groovy += "\n}\n\n"
		return groovy
