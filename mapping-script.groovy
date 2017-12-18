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
num_belongs_in_category_edges = Integer.valueOf(num_belongs_in_category_edges)

belongs_in_category_e = Generator.of {
	def neighbours_numeric = []
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

num_purchased_with_edges = Integer.valueOf(num_purchased_with_edges)

purchased_with_e = Generator.of {
	def neighbours_numeric = []
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

num_bought_after_viewing_edges = Integer.valueOf(num_bought_after_viewing_edges)

bought_after_viewing_e = Generator.of {
	def neighbours_numeric = []
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

num_reviewed_edges = Integer.valueOf(num_reviewed_edges)

reviewed_e = Generator.of {
	def neighbours_numeric = []
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

num_also_bought_edges = Integer.valueOf(num_also_bought_edges)

also_bought_e = Generator.of {
	def neighbours_numeric = []
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

num_viewed_with_edges = Integer.valueOf(num_viewed_with_edges)

viewed_with_e = Generator.of {
	def neighbours_numeric = []
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

num_has_salesRank_edges = Integer.valueOf(num_has_salesrank_edges)

has_salesRank_e = Generator.of {
	def neighbours_numeric = []
	for (int i = 1; i <= num_has_salesRank_edges; i++) {
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

