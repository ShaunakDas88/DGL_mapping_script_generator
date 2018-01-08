import json
from optparse import OptionParser
from schema_processor.SchemaProcessor import SchemaProcessor
from element_generator.MapperGenerator import MapperGenerator

parser = OptionParser()
parser.add_option("--schema_file_path", dest="schema_file_path", help="Where the schema file is located")
parser.add_option("--edge_distribution", dest="edge_distribution", default="point_mass", help="How we want the edge data to be distributed between different vertexLabels")
parser.add_option("--mapping_script_file_name", dest="mapping_script_file", default="mapping-script.groovy", help="Where to create DGL mapping script file")
(options, args) = parser.parse_args()

if not options.schema_file_path:
	print "\nPlease provide path to an existing valid schema file.\n"
	exit()	

schema_processor = SchemaProcessor(options.schema_file_path)
propertykey_map, vertexlabel_map, edgelabel_map = schema_processor.build_schema_maps()
mapper_generator = MapperGenerator(options.mapping_script_file, vertexlabel_map, edgelabel_map, propertykey_map, options.edge_distribution)
mapper_generator.generate_mapping_script()
