import sys

def orderonly(round, accumulator, a, b, c, d):
	#print "orderonly pageCount=%d round=%d accumulator=%s a=%s b=%s c=%s d=%s" %  (pageCount, round, accumulator, a, b, c, d)

	if round == 0:
		return [a, b, c, d]

	accumulator += [ "%d" % a, "%d" % b, "%d" % c, "%d" % d]

	orderonly(round - 1, accumulator, a-2, b+2, c-2, d+2)
	return accumulator

def order4(round, accumulator, a, b, c, d):
	#print "order4 pageCount=%d round=%d accumulator=%s a=%s b=%s c=%s d=%s" %  (pageCount, round, accumulator, a, b, c, d)

	if round == 0:
		return [a, b, c, d]

	accumulator += [ "%d" % a, "%d" % b, "%dS" % c, "%dS" % d]

	order4(round - 1, accumulator, a-2, b+2, c+2, d-2)

	return accumulator

def blank4(folioList):
	accumulator = [] 

	# Postprocess the result list and substitute blank.pdf for pages that don't exist
	for folio in folioList:
		if int(folio) > pageCount:
			accumulator += ["B1"]
		else:
			accumulator += ["A%s" % folio]
	return accumulator


def flip4(folioList):
	accumulator = []
	for i in range(0, len(folioList)):
		if ((i + 2) % 4) == 0 or ((i + 1) % 4) == 0:
			accumulator += [ "%sS" % folioList[i]]
		else:
			accumulator += [ "%s" % folioList[i]]
	return accumulator

#
# Usage python order.py file.pdf pagecount
#
if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Reorder the pages in a PDF document to print it in pamphlet order."
		print "Usage: order.py filename pagecount"
		sys.exit(1)

	filename = sys.argv[1]
	pageCount= int(sys.argv[2])
	folioCount = int((pageCount + 3) / 4) * 4
	rounds = folioCount / 4
	residue = pageCount % 4
	accumulator = [] 

	result = orderonly(rounds, accumulator, folioCount, 1, folioCount-1, 2)

	accumulator = blank4(result)

	accumulator = flip4(accumulator)

	#print accumulator	

	print "pdftk ",
	print "'A=%s' " % filename, "B=blank.pdf ",
	print "cat ", " ".join(accumulator),
	print "output ", "\"/Users/glennscott/Downloads/pamphlet.pdf\""
