# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from collections import OrderedDict
import os
import unicodecsv as csv, sys

# Load spreadsheet API
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/spreadsheets']
credentials = ServiceAccountCredentials.from_json_keyfile_name(path_to_creds + 'service_account_creds.json', scope)
gc = gspread.authorize(credentials)

sheet_ids = [
]

# Set up youtube-dl

import youtube_dl

class MyLogger(object):
	def debug(self, msg):
		pass

	def warning(self, msg):
		pass

	def error(self, msg):
		print(msg)

ydl_opts = {
	'format': 'bestaudio/best',
	'outtmpl': 'dl/%(id)s.%(ext)s',
	'postprocessors': [{
		'key': 'FFmpegExtractAudio',
		'preferredcodec': 'mp3',
		'preferredquality': '192',
	}],
	# 'logger': MyLogger(),
}
ydl = youtube_dl.YoutubeDL(ydl_opts)


# import pydub
import subprocess
snippet_tmpl = 'snippets/%(youtube_id)s_%(start)s_%(length)s.mp3'
stitch_tmpl = '%(dir)s/%(question_number)02d_%(difficulty)s.mp3'


def update_scoresheet(spreadsheet_id):
	worksheet = get_worksheet(spreadsheet_id)
	meta_worksheet = get_meta_worksheet(spreadsheet_id)

	youtube_ids = list(set(worksheet.col_values(3)[1:]))
	if u'' in youtube_ids:
		youtube_ids.remove(u'')
	for youtube_id in youtube_ids:
		try:
			path = ydl_opts['outtmpl'] % {'id': youtube_id, 'ext': 'mp3'}
			if os.path.exists(path):
				print 'Already downloaded %s' % path
			else:
				ydl.download([youtube_id])
		except youtube_dl.utils.DownloadError as e:
			print e

	values = worksheet.get_all_values()[1:]
	for row in values:
		if row[2] != '':
			create_snippet(row)

	meta_values = [question for question in meta_worksheet.get_all_values()[1:] if question[0] != '' and question[1] != '']
	create_answer_doc(meta_values, values)

	for question in meta_values:
		question_clips = [clip for clip in values if clip[0] == question[0]]
		# print '\t'.join(question[:4])
		# print '\t'.join(['.'.join(f[:2]) for f in question_clips])
		question[1] = meta_values[0][1] # use author of first question for all questions

		create_stitch(question, question_clips)
		print

	print 'Done'

def create_answer_doc(meta_values, values):
	names = meta_values[0][1]
	answer_doc_path = u'../answers/packets/%(names)s.txt' % {'names': names.replace(' ', '_')}
	answer_doc = u'Guerilla Imaginary Landscape\nQuestions submitted by %(names)s\n\n' % {'names': names}
	for row in meta_values:
		answer_doc += u'%(num)s. %(prompt)s\n' % {'num': row[0], 'prompt': row[3]}
		answer_doc += u'ANSWER: %(answer)s\n\n' % {'answer': row[4]}

	print 'Writing %s' % answer_doc_path
	f = open(answer_doc_path, 'w')
	f.write(answer_doc.encode('utf-8'))
	f.close()

	clip_doc_path = u'../clip_descriptions/packets/%(names)s.txt' % {'names': names.replace(' ', '_')}
	clip_header = ['Question','Clip','YouTube video ID','Start (sec)','Length (sec)','Link','Description']
	print 'Writing %s' % clip_doc_path
	ljustf = lambda x: x[:5]+[x[5].ljust(66) if x[5].startswith('http') else x[5]]+x[6:7]
	values_clips = [ljustf(row) for row in values]
	write_tsv(values_clips, clip_header, clip_doc_path)

def write_tsv(rows, header, path):
    with open(path, 'w') as f:
        writer = csv.writer(f, dialect=csv.excel_tab, lineterminator='\n', quoting=csv.QUOTE_NONE, quotechar=str('|'))
        writer.writerow(header)
        writer.writerows(rows)

def create_snippet(row):
	try:
		youtube_id = row[2]
		start = float(row[3])
		length = float(row[4])

		assert len(youtube_id) == 11 or len(youtube_id) == 17
		assert start >= 0
		assert length >= 0

		full_path = ydl_opts['outtmpl'] % {'id': youtube_id, 'ext': 'mp3'}
		snippet_path = snippet_tmpl % {'youtube_id': youtube_id, 'start': row[3], 'length': row[4]}

		if os.path.exists(snippet_path):
			print 'Already created %s' % snippet_path
			return

		print 'Creating %s' % snippet_path
		subprocess.call(['ffmpeg', '-v', 'warning', '-ss', '%s' % start, '-t', '%s' % length, '-i', full_path, snippet_path])

		# full_segment = pydub.AudioSegment.from_mp3(full_path)
		# snippet_segment = full_segment[start * 1000 : (start + length) * 1000]

		# snippet_segment.export(snippet_path)

	except AssertionError as e:
		raise
	except Exception as e:
		print e

def create_stitch(meta_row, rows):
	try:
		snippet_paths = []

		assert len(rows) == int(meta_row[5])

		for row in rows:
			youtube_id = row[2]
			start = float(row[3])
			length = float(row[4])

			assert len(youtube_id) == 11 or len(youtube_id) == 17
			assert start >= 0
			assert length >= 0

			snippet_path = snippet_tmpl % {'youtube_id': youtube_id, 'start': row[3], 'length': row[4]}
			if not os.path.exists(snippet_path):
				raise IOError

			snippet_paths.append(snippet_path)

		name = meta_row[1].replace(' ', '_')
		question_number = meta_row[0]
		difficulty = meta_row[2]

		stitch_dir = os.path.join('../packets', name)
		if not os.path.exists(stitch_dir):
			os.makedirs(stitch_dir)
		stitch_path = stitch_tmpl % {'dir': stitch_dir, 'question_number': int(question_number), 'difficulty': difficulty}

		concat_protocol = 'concat:%s' % '|snippets/silence.mp3|'.join(snippet_paths)

		if os.path.exists(stitch_path):
			print 'Already stitched %s' % stitch_path
			return

		print 'Creating %s' % stitch_path
		args = ['ffmpeg', '-v', 'fatal', '-i', concat_protocol, '-q:a', '2', stitch_path]
		subprocess.call(args)


		# full_segment = pydub.AudioSegment.from_mp3(full_path)
		# snippet_segment = full_segment[start * 1000 : (start + length) * 1000]

		# snippet_segment.export(snippet_path)

	except AssertionError as e:
		raise
	except Exception as e:
		print e
		print meta_row


def get_worksheet(spreadsheet_id):
	print 'Opening ' + spreadsheet_id
	spreadsheet = gc.open_by_key(spreadsheet_id)
	worksheet = spreadsheet.worksheet('Clips')
	return worksheet

def get_meta_worksheet(spreadsheet_id):
	spreadsheet = gc.open_by_key(spreadsheet_id)
	worksheet = spreadsheet.worksheet('Meta')
	return worksheet
	
for sheet_id in sheet_ids:
	try:
		update_scoresheet(sheet_id)
	except gspread.exceptions.APIError as e:
		print e
