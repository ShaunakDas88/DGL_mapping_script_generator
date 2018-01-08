// Define vertex count variables
num_Category_vertices = Integer.valueOf(num_category_vertices)
num_Item_vertices = Integer.valueOf(num_item_vertices)
num_Customer_vertices = Integer.valueOf(num_customer_vertices)

// Data generation for different vertices
Category_v = Generator.of {
	[
		id : it.toString()
	]
}.count(num_Category_vertices)

Item_v = Generator.of {
	[
		id : it.toString(),
		price : it.toDouble(),
		title : it.toString(),
		imUrl : it.toString(),
		description : it.toString(),
		brand : it.toString()
	]
}.count(num_Item_vertices)

Customer_v = Generator.of {
	[
		id : it.toString(),
		name : it.toString()
	]
}.count(num_Customer_vertices)

// Loading of vertex data
load(Category_v).asVertices {
	label "Category"
	key "id"
}

load(Item_v).asVertices {
	label "Item"
	key "id"
}

load(Customer_v).asVertices {
	label "Customer"
	key "id"
}

// Data generation for different edges
belongs_in_category_coefficient = Integer.valueOf(belongs_in_category_coefficient)
belongs_in_category_decay_constant = Integer.valueOf(belongs_in_category_decay_constant)

belongs_in_category_e = Generator.of {
	def neighbours_numeric = []
	def num_belongs_in_category_edges = belongs_in_category_coefficient*(it+1).power(-belongs_in_category_decay_constant).intValue()
	for (int i = 1; i <= num_belongs_in_category_edges; i++) {
		neighbours_numeric << ((it+i)%num_Category_vertices)
	}
	def neighbours = []
	for (int i : neighbours_numeric) {
		neighbours << i.toString()
	}
	[
		"out" : it.toString(), 
		"neighbours" : neighbours,
		"index" : it
	]
}
.count(num_Category_vertices)
.flatMap {
	outVertex = it["out"]
	index = it["index"]
	it.remove("index")
	it["neighbours"].collect {
		inVertex=it
		it = 
		[
			"out": outVertex,
			"in" : inVertex
		]
	}
}

purchased_with_coefficient = Integer.valueOf(purchased_with_coefficient)
purchased_with_decay_constant = Integer.valueOf(purchased_with_decay_constant)

purchased_with_e = Generator.of {
	def neighbours_numeric = []
	def num_purchased_with_edges = purchased_with_coefficient*(it+1).power(-purchased_with_decay_constant).intValue()
	for (int i = 1; i <= num_purchased_with_edges; i++) {
		neighbours_numeric << ((it+i)%num_Item_vertices)
	}
	def neighbours = []
	for (int i : neighbours_numeric) {
		neighbours << i.toString()
	}
	[
		"out" : it.toString(), 
		"neighbours" : neighbours,
		"index" : it
	]
}
.count(num_Item_vertices)
.flatMap {
	outVertex = it["out"]
	index = it["index"]
	it.remove("index")
	it["neighbours"].collect {
		inVertex=it
		it = 
		[
			"out": outVertex,
			"in" : inVertex
		]
	}
}

bought_after_viewing_coefficient = Integer.valueOf(bought_after_viewing_coefficient)
bought_after_viewing_decay_constant = Integer.valueOf(bought_after_viewing_decay_constant)

bought_after_viewing_e = Generator.of {
	def neighbours_numeric = []
	def num_bought_after_viewing_edges = bought_after_viewing_coefficient*(it+1).power(-bought_after_viewing_decay_constant).intValue()
	for (int i = 1; i <= num_bought_after_viewing_edges; i++) {
		neighbours_numeric << ((it+i)%num_Item_vertices)
	}
	def neighbours = []
	for (int i : neighbours_numeric) {
		neighbours << i.toString()
	}
	[
		"out" : it.toString(), 
		"neighbours" : neighbours,
		"index" : it
	]
}
.count(num_Item_vertices)
.flatMap {
	outVertex = it["out"]
	index = it["index"]
	it.remove("index")
	it["neighbours"].collect {
		inVertex=it
		it = 
		[
			"out": outVertex,
			"in" : inVertex
		]
	}
}

reviewed_coefficient = Integer.valueOf(reviewed_coefficient)
reviewed_decay_constant = Integer.valueOf(reviewed_decay_constant)

reviewed_e = Generator.of {
	def neighbours_numeric = []
	def num_reviewed_edges = reviewed_coefficient*(it+1).power(-reviewed_decay_constant).intValue()
	for (int i = 1; i <= num_reviewed_edges; i++) {
		neighbours_numeric << ((it+i)%num_Item_vertices)
	}
	def neighbours = []
	for (int i : neighbours_numeric) {
		neighbours << i.toString()
	}
	[
		"out" : it.toString(), 
		"neighbours" : neighbours,
		"index" : it
	]
}
.count(num_Item_vertices)
.flatMap {
	outVertex = it["out"]
	index = it["index"]
	it.remove("index")
	it["neighbours"].collect {
		inVertex=it
		it = 
		[
			"out": outVertex,
			"in" : inVertex,
			"summary" : index.toString(),
			"reviewText" : index.toString(),
			"timestampAsText" : index.toString(),
			"timestamp" : index.toInteger(),
			"helpful" : index.toDouble(),
			"rating" : index.toDouble()
		]
	}
}

also_bought_coefficient = Integer.valueOf(also_bought_coefficient)
also_bought_decay_constant = Integer.valueOf(also_bought_decay_constant)

also_bought_e = Generator.of {
	def neighbours_numeric = []
	def num_also_bought_edges = also_bought_coefficient*(it+1).power(-also_bought_decay_constant).intValue()
	for (int i = 1; i <= num_also_bought_edges; i++) {
		neighbours_numeric << ((it+i)%num_Item_vertices)
	}
	def neighbours = []
	for (int i : neighbours_numeric) {
		neighbours << i.toString()
	}
	[
		"out" : it.toString(), 
		"neighbours" : neighbours,
		"index" : it
	]
}
.count(num_Item_vertices)
.flatMap {
	outVertex = it["out"]
	index = it["index"]
	it.remove("index")
	it["neighbours"].collect {
		inVertex=it
		it = 
		[
			"out": outVertex,
			"in" : inVertex
		]
	}
}

viewed_with_coefficient = Integer.valueOf(viewed_with_coefficient)
viewed_with_decay_constant = Integer.valueOf(viewed_with_decay_constant)

viewed_with_e = Generator.of {
	def neighbours_numeric = []
	def num_viewed_with_edges = viewed_with_coefficient*(it+1).power(-viewed_with_decay_constant).intValue()
	for (int i = 1; i <= num_viewed_with_edges; i++) {
		neighbours_numeric << ((it+i)%num_Item_vertices)
	}
	def neighbours = []
	for (int i : neighbours_numeric) {
		neighbours << i.toString()
	}
	[
		"out" : it.toString(), 
		"neighbours" : neighbours,
		"index" : it
	]
}
.count(num_Item_vertices)
.flatMap {
	outVertex = it["out"]
	index = it["index"]
	it.remove("index")
	it["neighbours"].collect {
		inVertex=it
		it = 
		[
			"out": outVertex,
			"in" : inVertex
		]
	}
}

has_salesrank_coefficient = Integer.valueOf(has_salesrank_coefficient)
has_salesrank_decay_constant = Integer.valueOf(has_salesrank_decay_constant)

has_salesRank_e = Generator.of {
	def neighbours_numeric = []
	def num_has_salesrank_edges = has_salesrank_coefficient*(it+1).power(-has_salesrank_decay_constant).intValue()
	for (int i = 1; i <= num_has_salesrank_edges; i++) {
		neighbours_numeric << ((it+i)%num_Category_vertices)
	}
	def neighbours = []
	for (int i : neighbours_numeric) {
		neighbours << i.toString()
	}
	[
		"out" : it.toString(), 
		"neighbours" : neighbours,
		"index" : it
	]
}
.count(num_Category_vertices)
.flatMap {
	outVertex = it["out"]
	index = it["index"]
	it.remove("index")
	it["neighbours"].collect {
		inVertex=it
		it = 
		[
			"out": outVertex,
			"in" : inVertex,
			"rank" : index.toInteger()
		]
	}
}

// Loading of edge data
load(belongs_in_category_e).asEdges {
	label "belongs_in_category"
	outV "out", {
		label "Item"
		key "id"
	}
	inV "in", {
		label "Category"
		key "id"
	}
}

load(purchased_with_e).asEdges {
	label "purchased_with"
	outV "out", {
		label "Item"
		key "id"
	}
	inV "in", {
		label "Item"
		key "id"
	}
}

load(bought_after_viewing_e).asEdges {
	label "bought_after_viewing"
	outV "out", {
		label "Item"
		key "id"
	}
	inV "in", {
		label "Item"
		key "id"
	}
}

load(reviewed_e).asEdges {
	label "reviewed"
	outV "out", {
		label "Customer"
		key "id"
	}
	inV "in", {
		label "Item"
		key "id"
	}
}

load(also_bought_e).asEdges {
	label "also_bought"
	outV "out", {
		label "Item"
		key "id"
	}
	inV "in", {
		label "Item"
		key "id"
	}
}

load(viewed_with_e).asEdges {
	label "viewed_with"
	outV "out", {
		label "Item"
		key "id"
	}
	inV "in", {
		label "Item"
		key "id"
	}
}

load(has_salesRank_e).asEdges {
	label "has_salesRank"
	outV "out", {
		label "Item"
		key "id"
	}
	inV "in", {
		label "Category"
		key "id"
	}
}

