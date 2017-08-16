# -*- coding: utf-8 -*-

import re


def sanitize_text(text):

# Convert all to lower case
	text = text.lower()

	text = text.replace('á', 'a')
	text = text.replace('é', 'e')
	text = text.replace('í', 'i')
	text = text.replace('ó', 'o')
	text = text.replace('ú', 'u')

	text = text.replace('ã', 'a')
	text = text.replace('õ', 'o')

	text = text.replace('â', 'a')
	text = text.replace('ô', 'o')

	text = text.replace('ç', 'c')

	text = text.replace(',', '')
	text = text.replace('.', '')

	text = re.sub( '\s+', ' ', text ).strip()

	return text


text = '   Olá tuDo, bem ã ô           çççç.     X'
print sanitize_text(text)

