# Bird Watcher
# Search terms

# -- Basic groups

climate_change = ["climate change"]
pseudorandom = ["a", "an", "the"]
soccer = ["#manchesterunited", "#mufc"]
healthcare = ["#ahca"]

ascii_sad_faces = [
			  u':(', u';(', u':[', u';[',            # eyes and frown
			  u':-(', u';-(', u':-[', u';-[',       # eyes,nose and frown
			  u":'(", u":'-(", # :'(   :'-(       # eyes (apostrophe for tears) with frown
			  u'-.-', u'-_-',				        # closed eyes
			  u'D:', u'D;',						# eyes and open mouth frown
			  u'D-:', u'D-;',                    # eyes nose and open mouth frown
			  u':c', u':C', u';c', u';C',       # eyes and C frown
			  u'>_<', u'(>_<)', u'>.<', u'(>.<)' ]              # squeezed eyes

unicode_sad_faces = [
# ** Note: Commented out because often used to indicate laughter or crying-happiness **
#	u"\U0001F62D", # LOUDLY CRYING FACE
	u"\U0001F622", # CRYING FACE
	u"\U0001F63F", # CRYING CAT FACE
	u"\u2639",     # FROWNING FACE
	u"\U0001F641", # SLIGHTLY FROWNING FACE
	u"\U0001F61E", # DISAPPOINTED FACE
	u"\U0001F629", # WEARY FACE
	u"\U0001F494"] # BROKEN HEART

ascii_happy_faces = [
	u':)', u';)', u'x)',
	u'<3',
	u':D', u'xD',
	u'c:', u'C:']
unicode_happy_faces = [
	u"\U0001F601", # GRINNING FACE WITH SMILING EYES
	u"\U0001F602", # FACE WITH TEARS OF JOY
	u"\U0001F604", # SMILING FACE WITH OPEN MOUTH AND SMILING EYES
	u"\U0001F606", # SMILING FACE WITH OPEN MOUTH AND TIGHTLY CLOSED EYES (><)
	u"\U0001F609", # WINKING FACE
	u"\U0001F60A", # SMILING FACE WITH SMILING EYES (blush)
	u"\U0001F60B", # FACE SAVOURING DELICIOUS FOOD
	u"\U0001F60E", # SMILING FACE WITH SUNGLASSES
	u"\U0001F60D", # SMILING FACE WITH HEART-SHAPED EYES"
	u"\U0001F618", # FACE THROWING A KISS
	u"\u263A",     # WHITE SMILING FACE (blush)
	u"\U0001F60C", # RELIEVED FACE
	u"\u2764"    ] # RED HEART

# -- Combined groups
happy = ascii_happy_faces + unicode_happy_faces
sad = ascii_sad_faces + unicode_sad_faces
happysad = happy + sad
