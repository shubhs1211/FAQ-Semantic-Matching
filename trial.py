mydict = {'carl':40,
          'alan':2,
          'bob':1,
          'danny':3}

# for key, value in sorted(mydict.iteritems(), key = lambda (k,v): (v,k)):
#     print "%s: %s" % (key, value)

for key, value in sorted(mydict.items(), key = lambda x: x[1], reverse = True):
	print(key, value)