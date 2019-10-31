import requests, re, string, os, sys
from bs4 import BeautifulSoup

class EmptySentenceError(Exception):
	pass

def reportFileSaveError(path, errorString):
	print('Failed to save %s: %s' % (path, errorString))

def main():
	result = requests.get('https://www.cs.columbia.edu/~hgs/audio/harvard.html')
	content = result.content
	soup = BeautifulSoup(content)
	ols = soup.find_all('ol')
	baseDir = 'HarvardSentences'
	pattern = re.compile('[\W_]+')

	if not os.path.isdir(baseDir):
		os.makedirs(baseDir)

	os.chdir(baseDir)

	i = 1
	olsDigitCount = len(str(len(ols)))
	for ol in ols:
		lis = ol.find_all('li')

		olDir = str(i).zfill(olsDigitCount)
		i = i + 1

		if not os.path.isdir(olDir):
			os.makedirs(olDir)

		os.chdir(olDir)

		j = 1
		lisDigitCount = len(str(len(lis)))
		for li in lis:
			filename = str(j).zfill(lisDigitCount) + '.txt'
			j = j + 1

			errorString = ''
			try:
				with open(filename, 'w+') as file:
					# Some of the <li> tags have a new line at the end, which seems to cause BeautifulSoup to get subsequent <li> tag(s).
					# This ensures that only the first line is retrieved.
					# Each sentence from this set is a single line.
					sentence = li.text.partition('\n')[0].strip()
					if sentence == '':
						raise EmptySentenceError

					file.write(sentence)
					file.close()
			except OSError as err:
				errorString = 'OS error: {0}'.format(err)
			except IndexError as err:
				errorString = 'Index error: {0}'.format(err)
			except EmptySentenceError as err:
				errorString = 'Empty sentence.'
			except:
				errorString = 'Unexpected error, ' + str(sys.exc_info()[0])

			if errorString != '':
				path = os.path.join(os.getcwd(), filename)
				reportFileSaveError(path, errorString)

		os.chdir('../')

if __name__ == '__main__':
	main()