import json
import random

QUOTES_SOURCE='quotes.json'

class Quotes():
	def __init__(self, source = QUOTES_SOURCE):
		self.source = source
		
		with open(self.source, 'r') as f:
			self.quotes = json.load(f)['quotes']

	def get_random(self):
		q = random.choice(self.quotes)
		return self.format_quote(q)

	# TODO: find a better way to do this, it's hideous
	def format_dialogue(self, dial):
		dialogue = []
		for c in dial:
			quote = ""
			if c['person'] is not None:
				quote += f"{c['person']}"
			if c['notes'] is not None:
				quote += f" [{c['notes']}]"
			if c['sentence'] is not None:
				quote += f": {c['sentence']}"
			if quote != "":
				dialogue.append(quote)
		return "\n".join(dialogue)

	def format_quote(self, q):
		result = [
			q['context'],
			self.format_dialogue(q['dialogue']),
			q['notes']
		]

		return "\n".join(filter(bool, result))

def main():
	quotes = Quotes()
	print(quotes.get_random())

if __name__ == '__main__':
	main()